from flask import Flask, json, jsonify
from datetime import datetime, timedelta
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from helpers import DatabaseHelpers
import ModelTransformer

class BaseModel(db.Model):
    __abstract__ = True

    transformer = ModelTransformer.GenericTransformer()

    def transform(self, method='transform'):
        attr = getattr(self.transformer, method)
        return attr(self)

    def transform_many(self, models, method='transform'):
        data = []
        for model in models:
            attr = getattr(model.transformer, method)
            data.append(attr(model))
        return data
        
class Customer(BaseModel):
    __tablename__ = 'customers'

    id = db.Column(db.BigInteger, primary_key=True)
    display_name = db.Column(db.String(70))
    first_name = db.Column(db.String(70))
    last_name = db.Column(db.String(70))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(60))
    logo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    wallet = relationship('CustomerWallet', uselist=False)

    transformer = ModelTransformer.CustomerTransformer()


class CustomerToken(BaseModel):
    __tablename__ = 'customer_tokens'

    id = db.Column(db.String, primary_key=True)
    customer_id = db.Column(db.ForeignKey(u'customers.id', ondelete=u'CASCADE'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False,  default=DatabaseHelpers.expires_at)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    customer = relationship(u'Customer')

    transformer = ModelTransformer.CustomerTokenTransformer()


class CustomerWallet(BaseModel):
    __tablename__ = 'customer_wallets'

    id = db.Column(db.String, primary_key=True)
    customer_id = db.Column(db.ForeignKey(u'customers.id', ondelete=u'CASCADE'), nullable=False)
    current_balance = db.Column(db.BigInteger, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    last_transaction_date = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    transactions = relationship('Transaction', order_by="desc(Transaction.transaction_date)", backref='wallet')

    transformer = ModelTransformer.CustomerWalletTransformer()


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    id = db.Column(db.String(100), primary_key=True)
    wallet_id = db.Column(db.ForeignKey(u'customer_wallets.id', ondelete=u'CASCADE'), nullable=False)
    transaction_type = db.Column(db.String(100), nullable=False)
    transaction_amount = db.Column(db.Integer, nullable=False)
    remaining_amount = db.Column(db.Integer, nullable=True)
    transaction_date = db.Column(db.DateTime, nullable=False, default=func.now())
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    cancellation_date = db.Column(db.DateTime, nullable=True)
    cancelled_transaction_id = db.Column(db.ForeignKey(u'transactions.id'), nullable=True)

    cacelled_transaction = relationship(u'Transaction', uselist=False)

    transformer = ModelTransformer.TransactionTransformer()

