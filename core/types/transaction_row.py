from pydantic import BaseModel, Field
from typing import Optional, List

from core.database import Database
from core.models import TransactionRowOrm
from core.enums import TransactionStatus, TransactionType


class TransactionRow(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: Optional[str] = None
    status: TransactionStatus = Field(default=TransactionStatus.UNKNOWN)
    type: TransactionType = Field(default=TransactionType.UNKNOWN)

    @classmethod
    def get(cls, transaction_id: int) -> "TransactionRow":
        db = Database()
        transaction = db.get(
            TransactionRowOrm,
            transaction_id,
            columns=["id", "user_id", "name", "status", "type"],
        )
        return cls(**transaction.to_dict())

    @classmethod
    def batch_get(cls, transaction_ids: List[int]) -> List["TransactionRow"]:
        db = Database()
        transactions = db.batch_query(
            TransactionRowOrm,
            transaction_ids,
            columns=["id", "user_id", "name", "status", "type"],
        )
        return [cls(**transaction.to_dict()) for transaction in transactions]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "property_id": self.property_id,
            "name": self.name,
            "status": self.status,
            "type": self.type,
        }
