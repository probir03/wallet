from flask import Flask, session, redirect, request
from Exceptions.ExceptionHandler import WalletException
from Auth.AuthRepository import CustomerTokenRepository
from wallet.WalletRepository import CustomerWalletRepository
from models import CustomerToken
from app import app

'''
Decorator for token based authentication 
'''
def api_login_required(func):
	def wraps(*args, **kwargs):
		if request.headers.has_key('access-token'):
			repo = CustomerTokenRepository()
			token = request.headers['access-token']
			tokenObj = repo.check_valid_token(token)
			if hasattr(tokenObj, 'token'):
				request.__setattr__('customer', tokenObj.transform()['customer'])
			 	return func(*args, **kwargs)
		raise WalletException('Unauthorized request', 401)
	wraps.func_name = func.func_name
	return wraps

'''
decorator for validate transaction debit amount
'''
def check_wallet_amount_status(func):
	def wraps(wallet_id, *args, **kwargs):
		wallet = CustomerWalletRepository().filter_attribute({'id' : wallet_id})
		if request.json['transactionType'] == 'DEBIT' and request.json['transactionAmount'] > wallet.current_balance:
			raise WalletException("Insufficent Fund for the Debit transaction")
		return func(wallet_id, *args, **kwargs)
	wraps.func_name = func.func_name
	return wraps
