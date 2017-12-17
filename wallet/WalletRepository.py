from App.Repository import Repository
from models import CustomerWallet, Transaction
import datetime

'''
CustomerWalletRepository
'''
class CustomerWalletRepository():
    # CustomerTokenRepository cunstructor
    def __init__(self):
        self.model = CustomerWallet

    '''
    ' To Store the data
    '''
    def store(self, data):
        result = Repository.store(self.model, data)
        return result

    '''
    filter by the model attribute
    '''
    def filter_attribute(self, findBy):
        result = Repository.filter_attribute(self.model, findBy).first()
        return result



##
# TransactionRepository - For all database transactions
##
class TransactionRepository():

    #TransactionRepository constructor
    def __init__(self):
        self.model = Transaction

    ##
    # To Store the data
    ##
    def store(self, data):
        result = Repository.store(self.model, data)
        return result

    def update(self, filterBy, data):
        result = Repository.update(self.model, filterBy, data)
        return result

    def paginate_filter_attribute(self, filter_keys, item, page):
        return Repository.filer_by_paginated(self.model ,filter_keys, item=item, page=page)

    def filter_attribute(self, findBy):
        result = Repository.filter_attribute(self.model, findBy).first()
        return result

    def fetch_all_filter_attribute(self, findBy):
        result = Repository.filter_attribute(self.model, findBy).order_by(self.model.transaction_date.desc()).all()
        return result

    def delete(self, findBy):
        result = Repository.delete(self.model, findBy)
        return result