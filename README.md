# wallet
Create env.py file ($ touch env.py) and add keys

	APP_ENV = 'local'

	DEBUG = True/Flase

	SQLALCHEMY_DATABASE_URI = 
	'postgresql://<database-username>:<password>@localhost/<database-name>'

	SQLALCHEMY_TRACK_MODIFICATIONS = False

	SECRET_KEY='yuiop3fcvbnoiuy4hgfdc4vbnbvcx23456vbnmkjhgf3456bnmkjhc34'

Run Command
	
	```
	$ pip install -r requirements.txt

	$ python manage.py db upgrade

	$ python manage.py runserver
	```

Go to Browser and hit

	```
	 http://127.0.0.1:5000/

	 Register and login
	 ```

also can use postman to check API's

	```
	[Postman Link] (https://www.getpostman.com/collections/57fd12944f05d998c996)

	For all request except Signup and Login need to pass access-token(will get after login) in headers.

	access-token is using for customer authentication and no need of adding customer id for the API's
	```
