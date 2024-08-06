import requests
from flask import Flask,render_template,request,redirect,session,url_for
from DB import Database
from PIL import Image
from os import path

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
@app.route("/Weather")
def Weather():
    return render_template('Weather.html')
@app.route("/m")
def m():
    return render_template('m.html')

# SEP

@app.route("/upload", methods=['post'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the file to the desired location
        file.save(f'C:\\Users\HI\\Desktop\\render-demo\\static\\{file.filename}')
        jugad_Path = '.\static\\'+file.filename
        with Image.open('.\static\\'+file.filename) as img:
            type = img.format
            filepath = img.filename
            width, height = img.size
            mode = img.mode
            file_size = path.getsize(jugad_Path)
            file_name = path.basename(jugad_Path)
        return render_template('m.html',type_=type,width_=width,height_=height,mode_=mode,jugad_Path_=jugad_Path,file_name=file_name,file_size=file_size)


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

@app.route("/weather-forecast",methods=['post'])
def wetherForecast():
    city = request.form.get('city')
    api_key = '2f67c4bbcea52d586720123f8eb08ee3'    

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")

    mainWeather = weather_data.json()['weather'][0]['main']
    weatherDescription = weather_data.json()['weather'][0]['description']
    temp =  weather_data.json()['main']['temp']
    feelsLike = weather_data.json()['main']['feels_like']
    humidity = weather_data.json()['main']['humidity']

    return render_template('present.html',mainWeather_=mainWeather,weatherDescription_=weatherDescription,temp_=temp,feelsLike_=feelsLike,humidity_=humidity,city_=city) 
    
app.run(debug=True)

