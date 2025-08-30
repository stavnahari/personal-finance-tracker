from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import relationship
from backend.db.database import Base

# Declares a new table
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True) # Primary key (unique identifier)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Foreign key linking the transaction to a user
    date = Column(Date, nullable=False) # Date of the transaction
    amount = Column(DECIMAL(12, 2), nullable=False) # Money value (decimal with precision)
    merchant = Column(String(100)) # Store/vendor name
    description = Column(String(255)) # Free text about the transaction
    category = Column(String(50)) # Spending category (e.g., Food, Transport)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Auto-set timestamp when the record is created

    # Relationships
    # lets you access the User object directly from a transaction
    user = relationship("User", back_populates="transactions")

    # speeds up queries filtering by the following given
    __table_args__ = (
        Index("idx_user_date", "user_id", "date"),
        Index("idx_user_category", "user_id", "category"),
        Index("idx_user_amount", "user_id", "amount"),
    )
