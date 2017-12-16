from flask import Flask
from AuthRepository import CustomerRepository
from Exceptions.ExceptionHandler import WalletException

class CustomerValidator(object):
	"""docstring for CustomerValidator"""
		
	def create_customer_rule(self, inputs):
		if 'email' in inputs and 'password' in inputs and 'displayName' in inputs and 'rePassword' in inputs :
			existing_customer = CustomerRepository().filter_attribute({'email': inputs['email']})
			if existing_customer:
				raise WalletException('Email already Exists', 422)
			if inputs['password'] == inputs['rePassword'] : 
				return True
		raise WalletException('Invalid Inputs', 422)
