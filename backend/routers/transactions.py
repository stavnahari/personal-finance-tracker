from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from backend.db.database import SessionLocal
from backend.models.transaction import Transaction
from backend.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Endpoints

# Creates a transaction
@router.post("/", response_model=TransactionResponse)
def create_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    new_tx = Transaction(**tx.model_dump(), user_id=1)  # TODO: replace 1 with current_user.id
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx

# Lists transactions with filters (from_date, to_date, category, search q, pagination)
@router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    db: Session = Depends(get_db),
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    category: Optional[str] = None,
    q: Optional[str] = None,
    page: int = 1,
    limit: int = 50
):
    query = db.query(Transaction)

    if from_date:
        query = query.filter(Transaction.date >= from_date)
    if to_date:
        query = query.filter(Transaction.date <= to_date)
    if category:
        query = query.filter(Transaction.category == category)
    if q:
        query = query.filter(Transaction.description.ilike(f"%{q}%"))

    return query.offset((page - 1) * limit).limit(limit).all()

# Fetch a single transaction by ID (404 if not found)
@router.get("/{tx_id}", response_model=TransactionResponse)
def get_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

# Updates an existing transaction (404 if not found)
@router.put("/{tx_id}", response_model=TransactionResponse)
def update_transaction(tx_id: int, tx_data: TransactionCreate, db: Session = Depends(get_db)):
    tx = db.query(Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in tx_data.model_dump().items():
        setattr(tx, key, value)

    db.commit()
    db.refresh(tx)
    return tx

# Deletes a transaction
@router.delete("/{tx_id}")
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(tx)
    db.commit()
    return {"detail": "Transaction deleted"}
