from flask import Flask, json
from WalletRepository import CustomerWalletRepository, TransactionRepository
from helpers import Helpers
from WalletValidator import TransactionValidator
from Exceptions.ExceptionHandler import WalletException
from datetime import datetime
from app import db

class WalletViews(object):
	"""docstring for WalletViews"""
	
	'''
	create wallet
	'''
	def create_wallet(self, customer_id):
		return CustomerWalletRepository().store({
			'id' : Helpers.generate_unique_code(),
			'customer_id' : customer_id,
			'current_balance' : 0
		})

	'''
	get wallet balance
	'''
	def get_wallet(self, request):
		pass

	'''
	get all transaction of a wallet
	'''
	def fetch_all_wallet_transaction(self, wallet_id, request):
		data = request.args
		if 'type' in data and data['type'] == 'passbook':
			return TransactionRepository().fetch_all_filter_attribute({'wallet_id':wallet_id})
			
		is_active = True if 'type' in data and data['type'] == 'active' else False
		return TransactionRepository().paginate_filter_attribute({'wallet_id':wallet_id, 'is_active' : is_active},\
				data['item'] if 'item' in data else 10, data['page'] if 'page' in data else 1)
		
	'''
	add a transaction
	'''
	def request_transaction(self, wallet_id, data):
		TransactionValidator().add_transaction_rule(data)
		wallet = CustomerWalletRepository().filter_attribute({'id':wallet_id})
		transaction_repo = TransactionRepository()
		transaction = transaction_repo.store(
		{
			'id' : Helpers.generate_unique_numeric_code('string'),
			'wallet_id' : wallet_id,
			'transaction_type' : data['transactionType'],
			'transaction_amount' : data['transactionAmount'],
			'is_active' : True,
		})
		if transaction.transaction_type == 'CREDIT':
			#action for adding amount 
			wallet.current_balance += transaction.transaction_amount
		else : 
			#action of deduction of amount
			wallet.current_balance -= transaction.transaction_amount

		transaction.remaining_amount = wallet.current_balance
		db.session.commit()
		#return transaction object
		return transaction

	'''
	cancel a transaction
	'''
	def cancel_transaction(self, wallet_id, transaction_id):
		wallet = CustomerWalletRepository().filter_attribute({'id':wallet_id})
		transaction = TransactionRepository().filter_attribute({'id':transaction_id})
		if transaction:
			if not transaction.is_active:
				raise WalletException('Transaction already Cancelled', 422)
			elif transaction.transaction_type == 'CREDIT' and transaction.transaction_amount > wallet.current_balance:
				raise WalletException('This Transaction can not be cacelled due to insufficient balance', 422)

			transaction.cancellation_date = datetime.now()
			transaction.is_active = False
			db.session.commit()
			return self.transaction_due_to_cancelation(transaction, wallet)
		raise WalletException('Invalid Transaction Id', 422)

	'''
	after cancellation transaction
	'''
	def transaction_due_to_cancelation(self, transaction, wallet):
		if transaction.transaction_type == 'CREDIT':
			#action for adding amount 
			new_transaction_type = 'DEBIT'
		else : 
			#action of deduction of amount
			new_transaction_type = 'CREDIT'
		
		new_transaction = self.request_transaction(wallet.id, {
				'transactionType' : new_transaction_type,
				'transactionAmount' : transaction.transaction_amount
			})
		new_transaction.cancelled_transaction_id = transaction.id
		db.session.commit()
		return new_transaction


