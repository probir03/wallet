from flask import Flask
from AuthRepository import CustomerRepository
from Exceptions.ExceptionHandler import WalletException
import re

class CustomerValidator(object):
	"""docstring for CustomerValidator"""
		
	def create_customer_rule(self, inputs):
		reg = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
		if 'email' in inputs and 'password' in inputs and 'displayName' in inputs and 'rePassword' in inputs :
			if re.match(reg, inputs['email']) == None:
				raise WalletException('Invalid Email', 422)
			existing_customer = CustomerRepository().filter_attribute({'email': inputs['email']})
			if existing_customer:
				raise WalletException('Email already Exists', 422)
			if inputs['password'] == inputs['rePassword'] : 
				return True
		raise WalletException('Invalid Inputs', 422)
