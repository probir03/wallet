from flask import Flask, Blueprint, request, json
from views import WalletViews
from decorators import login_required, api_login_required, check_wallet_amount_status
from App.Response import Response

wallet = Blueprint('wallet', __name__, template_folder='templates')

'''
Get Wallet balance
'''
@wallet.route('/wallet', methods=['GET'])
@api_login_required
def wallet_data():
	response = WalletViews().get_wallet(request)
	pass

'''
route for a transaction request
'''
@wallet.route('/wallet/<wallet_id>/transactions', methods=['GET', 'POST'])
@api_login_required
@check_wallet_amount_status
def wallet_transactions(wallet_id):
	if request.method == 'GET':
		response = WalletViews.fetch_all_wallet_transaction(wallet_id)
		return Response.respondWithPaginatedCollection(response, hint='Transactions')
	
	response = WalletViews().request_transaction(wallet_id, request.json)
	return Response.respondWithItem(response, statusCode=201)

'''
route for a cancellation of transaction
'''
@wallet.route('/wallet/<wallet_id>/transactions/<transaction_id>', methods=['DELETE'])
@api_login_required
def transactions_actions(wallet_id, transaction_id):
	response = WalletViews().cancel_transaction(wallet_id, transaction_id)
	return Response.respondWithItem(response)
