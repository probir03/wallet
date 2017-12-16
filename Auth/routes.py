from flask import Flask, Blueprint, request, json, session
from views import AuthViews
from decorators import login_required, api_login_required
from App.Response import Response

auth = Blueprint('auth', __name__, template_folder='templates')

'''
Customer registration
'''
@auth.route('/register', methods=['POST'])
def register_user():
	response = AuthViews().create_customer(request.json)
	return Response.respondOk("Successfully Registerd", statusCode=201)

'''
Customer social signin
'''
@auth.route('/signin', methods=['GET'])
def signin():
    return AuthViews().social_signin(request.args.get('provider'))

'''
Social callback Url
'''
@auth.route('/auth', methods=['GET'])
def app_auth():
    response = AuthViews().social_app_login(request)
    return Response.respondWithItem(response)

'''
Customer legacy login
'''
@auth.route('/login/legacy', methods=['POST'])
def legacy():
    response = AuthViews().legacy_login(request)
    return Response.respondWithItem(response)
 
'''
Customer Logout
'''   
@auth.route('/logout', methods=['GET'])
@api_login_required
def app_logout():
    token = request.headers['access-token']
    response = AuthViews().logout(token)
    return Response.respondOk("Successfully Logged out")
