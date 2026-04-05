from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Borrower(Base):
    __tablename__ = "borrowers"
    id = Column(String, primary_key=True, index=True)

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(String, primary_key=True, index=True)
    borrower_id = Column(String, index=True)
    amount = Column(Float)
    direction = Column(String)
    category = Column(String)

class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, autoincrement=True)
    borrower_id = Column(String, index=True)
    liquidity_buffer = Column(Float)
    expense_income_ratio = Column(Float)

class GCIScore(Base):
    __tablename__ = "gci_scores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    borrower_id = Column(String, index=True)
    final_gci_score = Column(Integer)

class ManipulationFlag(Base):
    __tablename__ = "manipulation_flags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    borrower_id = Column(String, index=True)
    manipulation_label = Column(String)
    anomaly_score = Column(Float)