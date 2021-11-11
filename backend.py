import mysql.connector
from datetime import datetime
import os
import sys
from flask import Flask, redirect, url_for, render_template, request
from faces import login_system
from face_capture import faceCapture
from train import train
app = Flask(__name__)

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        result = request.form
        username = result['name']

        faceCapture(username, 100)
        train()

        myconn = mysql.connector.connect(host="localhost", user="root", passwd="7/2Roopnagar", database="facerecognition")
        date = datetime.utcnow().strftime('%Y-%m-%d')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        cursor = myconn.cursor()

        insert_command = f"INSERT INTO `Customer` VALUES (3, '{username}' , NOW(), '{date}');"
        cursor.execute(insert_command)
        myconn.commit()

        return redirect(url_for('index', message = "Signed Up successfully"))

    return render_template('signup.html')

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        login_string = login_system()
        if(login_string == 'Successful Login'):
            return render_template('profile.html')
        else:
            return render_template('index.html', message = login_string)

    if request.args:
        message = request.args['message']
        return render_template('index.html', message = message)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)