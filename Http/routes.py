from flask import Flask, Blueprint, render_template

base = Blueprint('base', __name__, template_folder='templates')

@base.route('/', methods=['GET'])
def login_page():
	return render_template('index.html')

@base.route('/register', methods=['GET'])
def registration_page():
	return render_template('register.html')