from flask import Flask
from flask_mysqldb import MySQL
import mysql.connector
from config import Config
#for tunnelling online my local server
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config.from_object(Config)
conn=mysql.connector.connect(host="remotemysql.com",user="HdI94neOEI",password="nVzQiDhvFE",database="HdI94neOEI")
cursor=conn.cursor()
#for tunnelling online my local server
run_with_ngrok(app)



from application import routes
