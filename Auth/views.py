from flask import Flask, json
from Auth.AuthRepository import CustomerRepository, CustomerTokenRepository
from helpers import Helpers
from AuthValidator import CustomerValidator
from wrapper import GoogleAuthentication
from Exceptions.ExceptionHandler import WalletException
from wallet.views import WalletViews
from app import db

class AuthViews(object):

	#create an customer
	def create_customer(self, data):
		CustomerValidator().create_customer_rule(data)
		repo = CustomerRepository()
		inputs = {
			'id' : Helpers.generate_unique_numeric_code(),
			'email' : data['email'],
			'password' : Helpers.hash_password(data['password']), 
			'display_name' : data['displayName'],
			'logo' : data['logo'] if 'logo' in data else None,
			'first_name' : data['firstName'] if 'firstName' in data else None,
			'last_name' : data['lastName'] if 'lastName' in data else None
		}
		customer = repo.store(inputs)
		WalletViews().create_wallet(customer.id)
		return customer

	#social signin or login
	def social_signin(self, provider):
		return getattr(self, Helpers.get_redirect_resolver(provider))()

	#redirecting to social auth page
	def google_redirect(self):
		return GoogleAuthentication.redirectTo()

	#after callback from social oauth
	def social_app_login(self, request):
		return getattr(self, Helpers.get_authrize_resolver(request.args.get('provider')))(request)

	#authorize the request
	def google_authorize(self, request):
		res = GoogleAuthentication.authorize(request)
		return self.google_login(res)

	#login via google OAuth
	def google_login(self, token):
		customer_info = GoogleAuthentication.get_customer_details(token)
		customer = CustomerRepository().filter_attribute({'email' : customer_info['email']})
		if customer is None:
			data = {
				'email' : customer_info['email'],
				'password' : None,
				'rePassword' : None,
				'displayName' : customer_info['display_name'],
				'firstName' : customer_info['first_name'],
				'lastName' : customer_info['last_name'],
				'is_password_change_required' : False,
				'logo' : customer_info['logo']
			}
			customer = self.create_customer(data)
		elif customer.logo is None :
			customer.logo = customer_info['logo']
			db.session.commit()
		token_repo = CustomerTokenRepository()
		customer_token = Helpers.access_token()
		return token_repo.store(
			{
				'id' : Helpers.generate_unique_code().__str__(),
				'token' : customer_token, 
				'customer_id' : customer.id
			})

	#legacy customer login
	def legacy_login(self, request):
		data = request.json
		customer = CustomerRepository().filter_attribute({'email': data['email']})
		if customer :
			validate = Helpers.validate_hash_password(data['password'], customer.password)
			if validate:
				token_repo = CustomerTokenRepository()
				customer_token = Helpers.access_token()
				return token_repo.store(
				{
					'id' : Helpers.generate_unique_code().__str__(),
					'token' : customer_token, 
					'customer_id' : customer.id
				})
		raise WalletException('Invalid credentials', 422)

	#Logout a customer
	def logout(self, token):
		token_repo = CustomerTokenRepository()
		return token_repo.deleteToken(token)
