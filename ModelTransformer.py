from helpers import Helpers

class GenericTransformer(object):
    """docstring for GenericTransformer"""
    def transform(self, model):
        return model.__dict__

class CustomerTransformer(object):
    """docstring for TransactionTransformer"""
    def transform(self, model):
    	return {
            'id' : model.id,
            'displayName' : model.display_name,
            'firstName' : model.first_name,
            'lastName' : model.last_name,
            'email' : model.email,
            'logo' : model.logo,
            'wallet' : model.wallet.transform()
        }

    def mini_transform(self, model):
    	return {
            'id' : model.id,
            'displayName' : model.display_name,
            'firstName' : model.first_name,
            'lastName' : model.last_name,
            'email' : model.email,
            'logo' : model.logo,
            'wallet' : model.wallet.transform('mini_transform')
        }

class CustomerTokenTransformer(object):
    """docstring for CustomerTokenransformer"""
    def transform(self, model):
    	return {
            'id' : model.id,
            'access-token' : model.token,
            'expiresAt' : Helpers.datetime_to_epoch(model.expires_at),
            'customer' : model.customer.transform('mini_transform')
        }

class CustomerWalletTransformer(object):
    """docstring for CustomerWalletTransformer"""
    def transform(self, model):
         return {
            'id' : model.id,
            'currentBalance' : model.current_balance,
            'lastTransactionDate' : Helpers.datetime_to_epoch(model.last_transaction_date),
            'transactions' : model.transform_many(model.transactions)
        }

    def mini_transform(self, model):
        return {
            'id' : model.id,
            'currentBalance' : model.current_balance,
            'lastTransactionDate' : Helpers.datetime_to_epoch(model.last_transaction_date),
        }

class TransactionTransformer(object):
    """docstring for TransactionTransformer"""
    def transform(self, model):
        return {
            'id' : model.id,
            'transactionType' : model.transaction_type,
            'transactionAmount' : model.transaction_amount,
            'transactionDate' : model.transaction_date,
            'isActive' : model.is_active,
            'cancellation_date' : model.cancellation_date,
            'cancelled_transaction' : model.cacelled_transaction.transform()\
                 if model.cacelled_transaction is not None else None,
            'wallet' : model.wallet.transform('mini_transform')
        }