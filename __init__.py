from app import app, db
from Exceptions.ExceptionHandler import WalletException

from Http.routes import base
from Auth.routes import auth
from wallet.routes import wallet

app.register_blueprint(base)
app.register_blueprint(auth, url_prefix = '/api/v1')
app.register_blueprint(wallet, url_prefix = '/api/v1')

if __name__=='__main__':
	app.run(debug=True)

# custome handler
@app.errorhandler(WalletException)
def handle_invalid_usage(error):
    response = error.to_dict()
    response.status_code = error.status_code
    return response