import os, datetime
from App.Repository import Repository
from models import Customer, CustomerToken

##
# CustomerRepository - For all database transactions
##
class CustomerRepository():
    #CustomerRepository constructor
    def __init__(self):
        self.model = Customer

    ##
    # To Store the data
    ##
    def store(self, data):
        result = Repository.store(self.model, data)
        return result

    def update(self, filterBy, data):
        result = Repository.update(self.model, filterBy, data)
        return result

    def fetch_all(self):
        result = Repository.fetchAll(self.model)
        return result

    def filter_attribute(self, findBy):
        result = Repository.filter_attribute(self.model, findBy).first()
        return result

    def delete(self, findBy):
        result = Repository.delete(self.model, findBy)
        return result


class CustomerTokenRepository():
    # CustomerTokenRepository cunstructor
    def __init__(self):
        self.model = CustomerToken

    '''
    ' To Store the data
    '''
    def store(self, data):
        result = Repository.store(self.model, data)
        return result

    '''
    check valid token
    '''
    def check_valid_token(self, token):
        findBy = {
            'token' : token,
        }
        result = Repository.filter_attribute(self.model, findBy).filter(self.model.expires_at > datetime.datetime.now()).first()
        return result

    '''
    delete token
    '''
    def deleteToken(self, token):
        return Repository.delete(self.model, {'token' : token})

