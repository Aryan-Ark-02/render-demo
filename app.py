import requests
from flask import Flask,render_template,request,redirect,session,url_for,flash
from DB import Database
from PIL import Image
import os
import nltk
from werkzeug.utils import secure_filename

obj = Database()

UPLOAD_FOLDER = 'C:\\Users\\HI\Desktop\\render-demo\\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
@app.route("/pos")
def POS():
    return render_template('POS.html')

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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with Image.open(file) as img:
            mode = img.mode
            Type = img.format
            width, height = img.size
            file_size = os.path.getsize('C:\\Users\\HI\Desktop\\render-demo\\uploads\\'+filename)
            file_name = os.path.basename('C:\\Users\\HI\Desktop\\render-demo\\uploads\\'+filename)

        return render_template('m.html',mode_=mode,type_=Type,width_=width,height_=height,filename=filename,file_name=file_name,file_size=file_size,file=file)


@app.route("/analyze", methods=['post'])
def analyze():
    textInput = request.form.get('textInput')
    listed = nltk.word_tokenize(textInput)
    usd = nltk.pos_tag(listed)
    dictionary = {'NN':[],'PRP':[],'VV':[],'RB':[],'JJ':[],'CC':[],'UH':[],'IN':[],}
    for i in usd:
        if i[-1] == 'NN': #or i[-1] == 'NNS' or i[-1] == 'NNP' or i[-1] == 'NNPS':
            if i[0] not in dictionary['NN']:
                dictionary['NN'].append(i[0])
        elif i[-1] == 'PRP' or i[-1] == 'PRP$':
            if i[0] not in dictionary['PRP']:
                dictionary['PRP'].append(i[0])
        elif i[-1].startswith('V'):
            if i[0] not in dictionary['VV']:
                dictionary['VV'].append(i[0]) 
        elif i[-1] == 'RB' or i[-1] == 'WRB' or i[-1] == 'RBR' or i[-1] == 'RBS' :
            if i[0] not in dictionary['RB']:
                dictionary['RB'].append(i[0])
        elif i[-1].startswith('J'):
            if i[0] not in dictionary['JJ']:
                dictionary['JJ'].append(i[0])
        elif i[-1] == 'CC':
            if i[0] not in dictionary['CC']:
                dictionary['CC'].append(i[0])
        elif i[-1] == 'UH':
            if i[0] not in dictionary['UH']:
                dictionary['UH'].append(i[0])
        elif i[-1] == 'IN':
            if i[0] not in dictionary['IN']:
                dictionary['IN'].append(i[0])
        else: continue

    return render_template('POS.html',textInput=textInput,dictionary=dictionary)
    
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

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}")

    mainWeather = weather_data.json()['weather'][0]['main']
    weatherDescription = weather_data.json()['weather'][0]['description']
    temp =  weather_data.json()['main']['temp']
    feelsLike = weather_data.json()['main']['feels_like']
    humidity = weather_data.json()['main']['humidity']

    return render_template('present.html',mainWeather_=mainWeather,weatherDescription_=weatherDescription,temp_=temp,feelsLike_=feelsLike,humidity_=humidity,city_=city) 
    
app.run(host="0.0.0.0", port=5000, debug=True)
