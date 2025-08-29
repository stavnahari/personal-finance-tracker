from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_transactions():
    return [{"id": 1, "amount": 100}, {"id": 2, "amount": -50}]
