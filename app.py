from flask import Flask,render_template,request,redirect,session,url_for
from DB import Database
import json

obj = Database()

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/Signup")
def Signup():
    return render_template('Signup.html')
@app.route("/Login")
def Login():
    return render_template('Login.html')

# SEP

@app.route("/do-login", methods=['post'])
def doLogin():
    email = request.form.get('email')
    password = request.form.get('password')
    response = obj.search(email,password)
    if response :
        return render_template('index.html')
    else:
        return render_template('Login.html')
@app.route("/do-signup",methods=['post'])
def doSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    response = obj.insert(name,email,password)
    if response:
        return render_template('Login.html') 
    else:
        return render_template('Login.html',msg ='Sign up successful' )

app.run(debug=True)

