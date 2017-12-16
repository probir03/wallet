from flask import Flask
from Exceptions.ExceptionHandler import WalletException

class TransactionValidator(object):
	"""docstring for CustomerValidator"""
	
	'''
	validate inputs for a transaction
	'''
	def add_transaction_rule(self, inputs):
		valid = True
		try : 
			valid = isinstance(inputs['transactionType'], str) and (inputs['transactionType'] == 'CREDIT' or inputs['transactionType'] == 'DEBIT')
			valid = isinstance(inputs['transactionAmount'], int)
			if valid:
				return True
			raise WalletException('Invalid Inputs', 422)
		except Exception as e:
			raise WalletException('Invalid Inputs', 422)
