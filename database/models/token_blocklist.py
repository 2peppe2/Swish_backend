from sqlalchemy import Column, String, Integer, DateTime

from ..base import db

class TokenBlocklist(db.Model):
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)