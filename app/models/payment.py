from sqlalchemy import Column, String, Integer, DateTime
from ..extensions import db


class Payment(db.Model):
    id = Column(String(36), nullable=False, primary_key=True)
    payee_payment_reference = Column(String(36), nullable=True)
    payment_reference = Column(String(36), nullable=True)  # From bank
    payee_alias = Column(Integer, nullable=True)
    payer_alias = Column(Integer, nullable=True)
    currency = Column(String(5), nullable=False)
    message = Column(String(50), nullable=True)
    status = Column(String(15), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    paid_at = Column(DateTime, nullable=True)

    def __init__(
        self,
        id: str,
        payee_payment_reference: str,
        payment_reference: str,
        payee_alias: int,
        payer_alias: int,
        currency: str,
        message: str,
        status: str,
        amount: int,
        created_at: DateTime,
        paid_at: DateTime
    ):
        self.id = id
        self.payee_payment_reference = payee_payment_reference
        self.payment_reference = payment_reference
        self.payee_alias = payee_alias
        self.payer_alias = payer_alias
        self.currency = currency
        self.message = message
        self.status = status
        self.amount = amount
        self.created_at = created_at
        self.paid_at = paid_at

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "payee_payment_reference": self.payee_payment_reference,
            "payment_reference": self.payment_reference,
            "payee_alias": self.payee_alias,
            "payer_alias": self.payer_alias,
            "currency": self.currency,
            "message": self.message,
            "status": self.status,
            "amount": self.amount,
            "created_at": self.created_at,
            "paid_at": self.paid_at,
        }
