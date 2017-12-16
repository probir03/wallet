from flask import jsonify

class WalletException(Exception):

    def __init__(self, message, status_code=500, payload=None, hint=None):
        Exception.__init__(self)
        self.message = message
        self.hint = hint
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error = dict(self.payload or ())
        error['data'] = []
        error['code'] = self.status_code
        error['notification'] = {
            'feedCode' : 'WALLET_'+str(self.status_code),
            'message' : self.message,
            'hint' : self.hint,
            'type' : 'error'
        }
        error['version'] = 1
        return jsonify(error)