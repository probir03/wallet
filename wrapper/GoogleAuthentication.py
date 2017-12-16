# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests
from flask import redirect
from Exceptions.ExceptionHandler import WalletException
import requests, json
from helpers import Helpers
from app import app



# (Receive token by HTTPS POST)
# ...

# def authenticate_token(token, device):
#     try:
#         if device == 'web':
#             idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), app.config['WEB_GOOGLE_CLIENT_ID'])
#         elif device == 'android' :
#             idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), app.config['ANDROID_GOOGLE_CLIENT_ID'])
#         else :
#             idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), app.config['IOS_GOOGLE_CLIENT_ID'])
            
#         # Or, if multiple clients access the backend server:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#         #     raise ValueError('Could not verify audience.')

#         if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#             raise ValueError('Wrong issuer.')

#         # If auth request is from a G Suite domain:
#         # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#         #     raise ValueError('Wrong hosted domain.')

#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         userid = idinfo['sub']
#         return create_user_data(json.loads(requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+token).content))
#     except ValueError:
#         raise DDTException("invalid google auth token")

def googleDefaults():
    default = {}
    default['token_request_uri'] = "https://accounts.google.com/o/oauth2/auth"
    default['response_type'] = "code"
    default['user_redirect_uri'] = Helpers.get_local_server_url()+"/api/v1/auth?provider=google"
    default['scope'] = "email"
    default['login_failed_url'] = '/'
    default['access_token_uri'] = 'https://accounts.google.com/o/oauth2/token'
    default['grant_type'] = 'authorization_code'
    return default


def redirectTo():
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri = googleDefaults()['token_request_uri'],
        response_type = googleDefaults()['response_type'],
        client_id = app.config['GOOGLE_CLIENT_ID'],
        redirect_uri = googleDefaults()['user_redirect_uri'],
        scope = googleDefaults()['scope']
        )
    return redirect(url)

# To Authorize the user with google signin
def authorize(request):
    params = {
        'code':request.args.get('code'),
        'redirect_uri': googleDefaults()['user_redirect_uri'],
        'client_id': app.config['GOOGLE_CLIENT_ID'],
        'client_secret': app.config['GOOGLE_CLIENT_SECRET'],
        'grant_type': googleDefaults()['grant_type']
    }
    resp = requests.post(googleDefaults()['access_token_uri'], data=params)
    token_data = resp.json()
    return token_data['access_token']

def get_customer_details(token):
    headers = {
        'Authorization': 'Bearer '+token
    }
    customer_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    customer_info = json.loads(customer_info.content)
    if 'email' not in customer_info:
        raise DDTException("invalid google auth token")
    return create_customer_data(customer_info)

def create_customer_data(customer_info):
    if 'verified_email' in customer_info and bool(customer_info['verified_email']) is not True:
        raise DDTException('Email is not verified')
    elif 'email_verified' in customer_info and bool(customer_info['email_verified']) is not True:
        raise DDTException('Email is not verified')
    return {
        'email' : customer_info['email'],
        'display_name' : customer_info['email'].split('@')[0],
        'first_name' : customer_info['name'].split(' ')[0],
        'last_name' : customer_info['family_name'],
        'logo' :  customer_info['picture'] if 'picture' in customer_info else None
    }