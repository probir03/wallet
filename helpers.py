from flask import Flask, request, url_for
import bcrypt, uuid, random, requests
import time
from datetime import datetime, timedelta
from app import app

class Helpers(object):
    """docstring for Helpers"""
    '''
    return epoch date
    '''
    @staticmethod
    def datetime_to_epoch(date):
        return time.mktime(date.timetuple())*1000
    '''
    To hash the password
    '''
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(str(password), bcrypt.gensalt())

    '''
    To hash the access-token
    '''
    @staticmethod
    def access_token():
        return bcrypt.hashpw(str(random.random()), bcrypt.gensalt())

    '''
    To validate/comapre the hash password
    @param present - user's account present password
    @param requested - password requested for verification
    '''
    @staticmethod
    def validate_hash_password(requested, present):
        return bcrypt.checkpw(str(requested), str(present))

    '''
    To create url for pagination 
    '''
    @staticmethod
    def url_for_other_page(page):
        args = dict(request.args)
        args['page'] = page
        return url_for(request.endpoint, _external=True, **args)
    '''
    To generate unique code
    uuid package
    '''
    @staticmethod
    def generate_unique_code():
        return uuid.uuid4().__str__()

    '''
    To generate unique big integer code of length 10
    '''
    @staticmethod
    def generate_unique_numeric_code():
        return int((uuid.uuid4().int.__str__())[:10])
    '''
    error message
    '''
    @staticmethod
    def error(message):
        return {
            'message' : message, 
            'tags' : 'error'
        }

    '''
    Get redirect function 
    '''
    @staticmethod
    def get_redirect_resolver(provider):
        if provider == 'google':
            return 'google_redirect'
        if provider == 'facebook':
            return 'facebook_redirect'
        if provider == 'github':
            return 'github_redirect'

    '''
    get authrization function
    '''
    @staticmethod
    def get_authrize_resolver(provider):
        if provider == 'google':
            return 'google_authorize'
        if provider == 'facebook':
            return 'facebook_authorize'
        if provider == 'github':
            return 'github_authorize'

    '''
    get respective api server url
    '''
    @staticmethod
    def get_local_server_url():
        if app.config['APP_ENV'] == 'production':
            return "http://(ip-address/domain)"
        return "http://localhost:5000"

    '''
    success message
    '''
    @staticmethod
    def success(message):
        return {
            'message' : message, 
            'tags' : 'success'
        }

class DatabaseHelpers(object):
    """docstring for DatabaseHelpers"""
    @staticmethod
    def expires_at():
        return datetime.utcnow() + timedelta(days=7)
        