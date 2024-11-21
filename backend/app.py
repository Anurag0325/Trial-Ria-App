import psycopg2
import csv
from flask import Flask, jsonify, request, send_file
from models import *
from flask_cors import CORS
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from io import BytesIO
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd
from werkzeug.security import generate_password_hash
import jwt
from sqlalchemy import func
from dotenv import load_dotenv
import time
import psutil
import gc
from flask_caching import Cache
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import threading
from time import sleep
from sqlalchemy.orm import load_only

load_dotenv()

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'  # In-memory cache
cache = Cache(app)

CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = "anuragiitmadras"

DATABASE_URL = 'sqlite:///database.sqlite3'  # Replace with your actual DB URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#     'DATABASE_URL')  # Use full URL from Render
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwerty@localhost:5432/kvqadatabase"
# app.config['SECRET_KEY'] = "anuragiitmadras"


db.init_app(app)


# def create_database():
#     connection = psycopg2.connect(
#     user="postgres", password="qwerty", host="127.0.0.1", port="5432")
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute("CREATE DATABASE kvqadatabase")
#         print("Database created successfully")
#     except psycopg2.errors.DuplicateDatabase:
#         print("Database already exists")
#     finally:
#         cursor.close()
#         connection.close()


def insert_dummy_data():
    colleagues_data = [
        # {"name": "Alice Johnson", "email": "22dp1000105@ds.study.iitm.ac.in",
        #     "department": "IT", "designation": "Analyst"},
        {"name": "Anurag Kumar", "email": "akanuragkumar75@gmail.com",
            "department": "Developer", "designation": "Developer"},
        {"name": "Sethi", "email": "tech@kvqaindia.com",
            "department": "Developer", "designation": "Frontend Developer"},
        # {"name": "Anurag Gmail", "email": "akanuragkumar4@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Ritika", "email": "training@kvqaindia.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "lav@kvqaindia.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Ritika GMAIL", "email": "ritzgupta998@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Ritika Fashion", "email": "ritzfashiononline@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Lav Kaushik_temp", "email": "somag89556@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "kafay34325@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "hafebom642@exoular.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "hasej86977@gitated.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "pecepi9521@cashbn.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "namax29728@gitated.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "tixiy15582@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "yolenif475@gitated.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "jowis58296@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "kehot22123@cpaurl.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "tomacob234@cpaurl.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "dogif17943@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "yinonoj630@kazvi.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "selofo8026@merotx.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "xison17512@kazvi.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "citeji5554@kimasoft.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Lav Kaushik_temp", "email": "kixit64836@gitated.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "fakewi8084@cashbn.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "behawi2407@cpaurl.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "powog89677@cashbn.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "lijojid877@cpaurl.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "mokob12207@cashbn.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "gamek16395@gitated.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "kecit61211@cashbn.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "veraye2238@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "rofac89385@exoular.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "mogiled377@cashbn.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "yaboba4269@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "sakos22466@cashbn.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "hanahir357@exoular.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "hisasog163@exoular.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "hogihen707@cashbn.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Krishna Chaudhari", "email": "krishna.chaudhari@riaadvisory.com",
        #     "department": "Internal IT and Cloud Ops", "designation": "Associate Consultant"},
        # {"name": "Krishna Chaudhari GMAIL", "email": "krish.chaudhari2018@gmail.com",
        #     "department": "Internal IT and Cloud Ops", "designation": "Associate Consultant"},
        # {"name": "Jibin Sebastian", "email": "jibin.sebastian@riaadvisory.com",
        #     "department": "Operations", "designation": "Consultant - Admin"},
        # {"name": "Salman Ansari", "email": "salman.ansari@riaadvisory.com",
        #     "department": "Internal IT and Cloud Ops", "designation": "Director - CISO"},
        # {"name": "Deepak Nichani", "email": "deepak.nichani@riaadvisory.com",
        #     "department": "Operations", "designation": "Senior Consultant - Admin"},
        # {"name": "Suraj Kamble", "email": "suraj.kambale@riaadvisory.com",
        #     "department": "Developer", "designation": "Consultant"},
        # {"name": "Eva Adams", "email": "eva.adams@bing.com", "designation": "HR"},

        # {"name": "Ritika", "email": "tosopeg490@cpaurl.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "dojel51420@exoular.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun", "email": "wenayir754@gitated.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG", "email": "lapec18115@cpaurl.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales", "email": "tisopa4652@cashbn.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO", "email": "cajoki9143@cashbn.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby", "email": "peway67109@gitated.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli", "email": "libadef322@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha", "email": "xepesic916@gitated.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan", "email": "gociy10751@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info", "email": "livamex757@exoular.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali", "email": "xovijoh828@gitated.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha", "email": "xexeke6928@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR", "email": "gimejob509@gitated.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi", "email": "goxasa1124@exoular.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun", "email": "lihiy72683@cpaurl.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS", "email": "jahep63024@cpaurl.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Himanshi", "email": "xoloko1077@cpaurl.com",
        #     "department": "Data Analyzer", "designation" : "Data Analyst"},
        # {"name": "Lav Kaushik_temp", "email": "halonim833@cashbn.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "negono6293@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "lawiy24270@exoular.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "tahige1177@exoular.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "kococeh740@gitated.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "nived34325@exoular.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "xexobos196@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "sales56612@gitated.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "micedat270@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "tekixi5647@cpaurl.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "momila1721@exoular.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "pahayis503@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "kapeli3117@gitated.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "meroyeh366@gitated.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "kobelah642@exoular.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "lahif62317@cpaurl.com",
        #     "department": "OPS", "designation": "OPS"},


        {'name': 'name_1', 'email': '0-mail.com', 'department': 'department_1', 'designation': 'designation_1'},
        {'name': 'name_2', 'email': '027168.com', 'department': 'department_2', 'designation': 'designation_2'},
        {'name': 'name_3', 'email': '0815.ru', 'department': 'department_3', 'designation': 'designation_3'},   
        {'name': 'name_4', 'email': '0815.ry', 'department': 'department_4', 'designation': 'designation_4'},   
        {'name': 'name_5', 'email': '0815.su', 'department': 'department_5', 'designation': 'designation_5'},   
        {'name': 'name_6', 'email': '0845.ru', 'department': 'department_6', 'designation': 'designation_6'},   
        {'name': 'name_7', 'email': '0box.eu', 'department': 'department_7', 'designation': 'designation_7'},   
        {'name': 'name_8', 'email': '0clickemail.com', 'department': 'department_8', 'designation': 'designation_8'},
        {'name': 'name_9', 'email': '0n0ff.net', 'department': 'department_9', 'designation': 'designation_9'},
        {'name': 'name_10', 'email': '0nelce.com', 'department': 'department_10', 'designation': 'designation_10'},
        {'name': 'name_11', 'email': '0v.ro', 'department': 'department_11', 'designation': 'designation_11'},
        {'name': 'name_12', 'email': '0w.ro', 'department': 'department_12', 'designation': 'designation_12'},
        {'name': 'name_13', 'email': '0wnd.net', 'department': 'department_13', 'designation': 'designation_13'},
        {'name': 'name_14', 'email': '0wnd.org', 'department': 'department_14', 'designation': 'designation_14'},
        {'name': 'name_15', 'email': '0x207.info', 'department': 'department_15', 'designation': 'designation_15'},
        {'name': 'name_16', 'email': '1-8.biz', 'department': 'department_16', 'designation': 'designation_16'},
        {'name': 'name_17', 'email': '1-tm.com', 'department': 'department_17', 'designation': 'designation_17'},
        {'name': 'name_18', 'email': '10-minute-mail.com', 'department': 'department_18', 'designation': 'designation_18'},
        {'name': 'name_19', 'email': '1000rebates.stream', 'department': 'department_19', 'designation': 'designation_19'},
        {'name': 'name_20', 'email': '100likers.com', 'department': 'department_20', 'designation': 'designation_20'},
        {'name': 'name_21', 'email': '105kg.ru', 'department': 'department_21', 'designation': 'designation_21'},
        {'name': 'name_22', 'email': '10dk.email', 'department': 'department_22', 'designation': 'designation_22'},
        {'name': 'name_23', 'email': '10mail.com', 'department': 'department_23', 'designation': 'designation_23'},
        {'name': 'name_24', 'email': '10mail.org', 'department': 'department_24', 'designation': 'designation_24'},
        {'name': 'name_25', 'email': '10mail.tk', 'department': 'department_25', 'designation': 'designation_25'},
        {'name': 'name_26', 'email': '10mail.xyz', 'department': 'department_26', 'designation': 'designation_26'},
        {'name': 'name_27', 'email': '10minmail.de', 'department': 'department_27', 'designation': 'designation_27'},
        {'name': 'name_28', 'email': '10minut.com.pl', 'department': 'department_28', 'designation': 'designation_28'},
        {'name': 'name_29', 'email': '10minut.xyz', 'department': 'department_29', 'designation': 'designation_29'},
        {'name': 'name_30', 'email': '10minutemail.be', 'department': 'department_30', 'designation': 'designation_30'},
        {'name': 'name_31', 'email': '10minutemail.cf', 'department': 'department_31', 'designation': 'designation_31'},
        {'name': 'name_32', 'email': '10minutemail.co.uk', 'department': 'department_32', 'designation': 'designation_32'},
        {'name': 'name_33', 'email': '10minutemail.co.za', 'department': 'department_33', 'designation': 'designation_33'},
        {'name': 'name_34', 'email': '10minutemail.com', 'department': 'department_34', 'designation': 'designation_34'},
        {'name': 'name_35', 'email': '10minutemail.de', 'department': 'department_35', 'designation': 'designation_35'},
        {'name': 'name_36', 'email': '10minutemail.ga', 'department': 'department_36', 'designation': 'designation_36'},
        {'name': 'name_37', 'email': '10minutemail.gq', 'department': 'department_37', 'designation': 'designation_37'},
        {'name': 'name_38', 'email': '10minutemail.ml', 'department': 'department_38', 'designation': 'designation_38'},
        {'name': 'name_39', 'email': '10minutemail.net', 'department': 'department_39', 'designation': 'designation_39'},
        {'name': 'name_40', 'email': '10minutemail.nl', 'department': 'department_40', 'designation': 'designation_40'},
        {'name': 'name_41', 'email': '10minutemail.pro', 'department': 'department_41', 'designation': 'designation_41'},
        {'name': 'name_42', 'email': '10minutemail.us', 'department': 'department_42', 'designation': 'designation_42'},
        {'name': 'name_43', 'email': '10minutemailbox.com', 'department': 'department_43', 'designation': 'designation_43'},
        {'name': 'name_44', 'email': '10minutemails.in', 'department': 'department_44', 'designation': 'designation_44'},
        {'name': 'name_45', 'email': '10minutenemail.de', 'department': 'department_45', 'designation': 'designation_45'},
        {'name': 'name_46', 'email': '10minutenmail.xyz', 'department': 'department_46', 'designation': 'designation_46'},
        {'name': 'name_47', 'email': '10minutesmail.com', 'department': 'department_47', 'designation': 'designation_47'},
        {'name': 'name_48', 'email': '10minutesmail.fr', 'department': 'department_48', 'designation': 'designation_48'},
        {'name': 'name_49', 'email': '10minutmail.pl', 'department': 'department_49', 'designation': 'designation_49'},
        {'name': 'name_50', 'email': '10x9.com', 'department': 'department_50', 'designation': 'designation_50'},
        {'name': 'name_51', 'email': '11163.com', 'department': 'department_51', 'designation': 'designation_51'},
        {'name': 'name_52', 'email': '123-m.com', 'department': 'department_52', 'designation': 'designation_52'},
        {'name': 'name_53', 'email': '12hosting.net', 'department': 'department_53', 'designation': 'designation_53'},
        {'name': 'name_54', 'email': '12houremail.com', 'department': 'department_54', 'designation': 'designation_54'},
        {'name': 'name_55', 'email': '12minutemail.com', 'department': 'department_55', 'designation': 'designation_55'},
        {'name': 'name_56', 'email': '12minutemail.net', 'department': 'department_56', 'designation': 'designation_56'},
        {'name': 'name_57', 'email': '12storage.com', 'department': 'department_57', 'designation': 'designation_57'},
        {'name': 'name_58', 'email': '140unichars.com', 'department': 'department_58', 'designation': 'designation_58'},
        {'name': 'name_59', 'email': '147.cl', 'department': 'department_59', 'designation': 'designation_59'},
        {'name': 'name_60', 'email': '14n.co.uk', 'department': 'department_60', 'designation': 'designation_60'},
        {'name': 'name_61', 'email': '15qm.com', 'department': 'department_61', 'designation': 'designation_61'},
        {'name': 'name_62', 'email': '1blackmoon.com', 'department': 'department_62', 'designation': 'designation_62'},
        {'name': 'name_63', 'email': '1ce.us', 'department': 'department_63', 'designation': 'designation_63'},
        {'name': 'name_64', 'email': '1chuan.com', 'department': 'department_64', 'designation': 'designation_64'},
        {'name': 'name_65', 'email': '1clck2.com', 'department': 'department_65', 'designation': 'designation_65'},
        {'name': 'name_66', 'email': '1fsdfdsfsdf.tk', 'department': 'department_66', 'designation': 'designation_66'},
        {'name': 'name_67', 'email': '1mail.ml', 'department': 'department_67', 'designation': 'designation_67'},
        {'name': 'name_68', 'email': '1pad.de', 'department': 'department_68', 'designation': 'designation_68'},
        {'name': 'name_69', 'email': '1s.fr', 'department': 'department_69', 'designation': 'designation_69'},
        {'name': 'name_70', 'email': '1secmail.com', 'department': 'department_70', 'designation': 'designation_70'},
        {'name': 'name_71', 'email': '1secmail.net', 'department': 'department_71', 'designation': 'designation_71'},
        {'name': 'name_72', 'email': '1secmail.org', 'department': 'department_72', 'designation': 'designation_72'},
        {'name': 'name_73', 'email': '1st-forms.com', 'department': 'department_73', 'designation': 'designation_73'},
        {'name': 'name_74', 'email': '1to1mail.org', 'department': 'department_74', 'designation': 'designation_74'},
        {'name': 'name_75', 'email': '1usemail.com', 'department': 'department_75', 'designation': 'designation_75'},
        {'name': 'name_76', 'email': '1webmail.info', 'department': 'department_76', 'designation': 'designation_76'},
        {'name': 'name_77', 'email': '1zhuan.com', 'department': 'department_77', 'designation': 'designation_77'},
        {'name': 'name_78', 'email': '2012-2016.ru', 'department': 'department_78', 'designation': 'designation_78'},
        {'name': 'name_79', 'email': '20email.eu', 'department': 'department_79', 'designation': 'designation_79'},
        {'name': 'name_80', 'email': '20email.it', 'department': 'department_80', 'designation': 'designation_80'},
        {'name': 'name_81', 'email': '20mail.eu', 'department': 'department_81', 'designation': 'designation_81'},
        {'name': 'name_82', 'email': '20mail.in', 'department': 'department_82', 'designation': 'designation_82'},
        {'name': 'name_83', 'email': '20mail.it', 'department': 'department_83', 'designation': 'designation_83'},
        {'name': 'name_84', 'email': '20minutemail.com', 'department': 'department_84', 'designation': 'designation_84'},
        {'name': 'name_85', 'email': '20minutemail.it', 'department': 'department_85', 'designation': 'designation_85'},
        {'name': 'name_86', 'email': '20mm.eu', 'department': 'department_86', 'designation': 'designation_86'},
        {'name': 'name_87', 'email': '2120001.net', 'department': 'department_87', 'designation': 'designation_87'},
        {'name': 'name_88', 'email': '21cn.com', 'department': 'department_88', 'designation': 'designation_88'},
        {'name': 'name_89', 'email': '247web.net', 'department': 'department_89', 'designation': 'designation_89'},
        {'name': 'name_90', 'email': '24hinbox.com', 'department': 'department_90', 'designation': 'designation_90'},
        {'name': 'name_91', 'email': '24hourmail.com', 'department': 'department_91', 'designation': 'designation_91'},
        {'name': 'name_92', 'email': '24hourmail.net', 'department': 'department_92', 'designation': 'designation_92'},
        {'name': 'name_93', 'email': '2anom.com', 'department': 'department_93', 'designation': 'designation_93'},
        {'name': 'name_94', 'email': '2chmail.net', 'department': 'department_94', 'designation': 'designation_94'},
        {'name': 'name_95', 'email': '2ether.net', 'department': 'department_95', 'designation': 'designation_95'},
        {'name': 'name_96', 'email': '2fdgdfgdfgdf.tk', 'department': 'department_96', 'designation': 'designation_96'},
        {'name': 'name_97', 'email': '2odem.com', 'department': 'department_97', 'designation': 'designation_97'},
        {'name': 'name_98', 'email': '2prong.com', 'department': 'department_98', 'designation': 'designation_98'},
        {'name': 'name_99', 'email': '2wc.info', 'department': 'department_99', 'designation': 'designation_99'},
        {'name': 'name_100', 'email': '300book.info', 'department': 'department_100', 'designation': 'designation_100'},
        {'name': 'name_101', 'email': '30mail.ir', 'department': 'department_101', 'designation': 'designation_101'},
        {'name': 'name_102', 'email': '30minutemail.com', 'department': 'department_102', 'designation': 'designation_102'},
        {'name': 'name_103', 'email': '30wave.com', 'department': 'department_103', 'designation': 'designation_103'},
        {'name': 'name_104', 'email': '3202.com', 'department': 'department_104', 'designation': 'designation_104'},
        {'name': 'name_105', 'email': '36ru.com', 'department': 'department_105', 'designation': 'designation_105'},
        {'name': 'name_106', 'email': '3d-painting.com', 'department': 'department_106', 'designation': 'designation_106'},
        {'name': 'name_107', 'email': '3l6.com', 'department': 'department_107', 'designation': 'designation_107'},
        {'name': 'name_108', 'email': '3mail.ga', 'department': 'department_108', 'designation': 'designation_108'},
        {'name': 'name_109', 'email': '3trtretgfrfe.tk', 'department': 'department_109', 'designation': 'designation_109'},
        {'name': 'name_110', 'email': '4-n.us', 'department': 'department_110', 'designation': 'designation_110'},
        {'name': 'name_111', 'email': '4057.com', 'department': 'department_111', 'designation': 'designation_111'},
        {'name': 'name_112', 'email': '418.dk', 'department': 'department_112', 'designation': 'designation_112'},
        {'name': 'name_113', 'email': '42o.org', 'department': 'department_113', 'designation': 'designation_113'},
        {'name': 'name_114', 'email': '4gfdsgfdgfd.tk', 'department': 'department_114', 'designation': 'designation_114'},
        {'name': 'name_115', 'email': '4k5.net', 'department': 'department_115', 'designation': 'designation_115'},
        {'name': 'name_116', 'email': '4mail.cf', 'department': 'department_116', 'designation': 'designation_116'},
        {'name': 'name_117', 'email': '4mail.ga', 'department': 'department_117', 'designation': 'designation_117'},
        {'name': 'name_118', 'email': '4nextmail.com', 'department': 'department_118', 'designation': 'designation_118'},
        {'name': 'name_119', 'email': '4nmv.ru', 'department': 'department_119', 'designation': 'designation_119'},
        {'name': 'name_120', 'email': '4tb.host', 'department': 'department_120', 'designation': 'designation_120'},
        {'name': 'name_121', 'email': '4warding.com', 'department': 'department_121', 'designation': 'designation_121'},
        {'name': 'name_122', 'email': '4warding.net', 'department': 'department_122', 'designation': 'designation_122'},
        {'name': 'name_123', 'email': '4warding.org', 'department': 'department_123', 'designation': 'designation_123'},
        {'name': 'name_124', 'email': '50set.ru', 'department': 'department_124', 'designation': 'designation_124'},
        {'name': 'name_125', 'email': '55hosting.net', 'department': 'department_125', 'designation': 'designation_125'},
        {'name': 'name_126', 'email': '5ghgfhfghfgh.tk', 'department': 'department_126', 'designation': 'designation_126'},
        {'name': 'name_127', 'email': '5gramos.com', 'department': 'department_127', 'designation': 'designation_127'},
        {'name': 'name_128', 'email': '5july.org', 'department': 'department_128', 'designation': 'designation_128'},
        {'name': 'name_129', 'email': '5mail.cf', 'department': 'department_129', 'designation': 'designation_129'},
        {'name': 'name_130', 'email': '5mail.ga', 'department': 'department_130', 'designation': 'designation_130'},
        {'name': 'name_131', 'email': '5minutemail.net', 'department': 'department_131', 'designation': 'designation_131'},
        {'name': 'name_132', 'email': '5oz.ru', 'department': 'department_132', 'designation': 'designation_132'},
        {'name': 'name_133', 'email': '5tb.in', 'department': 'department_133', 'designation': 'designation_133'},
        {'name': 'name_134', 'email': '5x25.com', 'department': 'department_134', 'designation': 'designation_134'},
        {'name': 'name_135', 'email': '5ymail.com', 'department': 'department_135', 'designation': 'designation_135'},
        {'name': 'name_136', 'email': '60minutemail.com', 'department': 'department_136', 'designation': 'designation_136'},
        {'name': 'name_137', 'email': '672643.net', 'department': 'department_137', 'designation': 'designation_137'},
        {'name': 'name_138', 'email': '675hosting.com', 'department': 'department_138', 'designation': 'designation_138'},
        {'name': 'name_139', 'email': '675hosting.net', 'department': 'department_139', 'designation': 'designation_139'},
        {'name': 'name_140', 'email': '675hosting.org', 'department': 'department_140', 'designation': 'designation_140'},
        {'name': 'name_141', 'email': '6hjgjhgkilkj.tk', 'department': 'department_141', 'designation': 'designation_141'},
        {'name': 'name_142', 'email': '6ip.us', 'department': 'department_142', 'designation': 'designation_142'},
        {'name': 'name_143', 'email': '6mail.cf', 'department': 'department_143', 'designation': 'designation_143'},
        {'name': 'name_144', 'email': '6mail.ga', 'department': 'department_144', 'designation': 'designation_144'},
        {'name': 'name_145', 'email': '6mail.ml', 'department': 'department_145', 'designation': 'designation_145'},
        {'name': 'name_146', 'email': '6paq.com', 'department': 'department_146', 'designation': 'designation_146'},
        {'name': 'name_147', 'email': '6somok.ru', 'department': 'department_147', 'designation': 'designation_147'},
        {'name': 'name_148', 'email': '6url.com', 'department': 'department_148', 'designation': 'designation_148'},
        {'name': 'name_149', 'email': '75hosting.com', 'department': 'department_149', 'designation': 'designation_149'},
        {'name': 'name_150', 'email': '75hosting.net', 'department': 'department_150', 'designation': 'designation_150'},
        {'name': 'name_151', 'email': '75hosting.org', 'department': 'department_151', 'designation': 'designation_151'},
        {'name': 'name_152', 'email': '7days-printing.com', 'department': 'department_152', 'designation': 'designation_152'},
        {'name': 'name_153', 'email': '7mail.ga', 'department': 'department_153', 'designation': 'designation_153'},
        {'name': 'name_154', 'email': '7mail.ml', 'department': 'department_154', 'designation': 'designation_154'},
        {'name': 'name_155', 'email': '7tags.com', 'department': 'department_155', 'designation': 'designation_155'},
        {'name': 'name_156', 'email': '80665.com', 'department': 'department_156', 'designation': 'designation_156'},
        {'name': 'name_157', 'email': '8127ep.com', 'department': 'department_157', 'designation': 'designation_157'},
        {'name': 'name_158', 'email': '8mail.cf', 'department': 'department_158', 'designation': 'designation_158'},
        {'name': 'name_159', 'email': '8mail.ga', 'department': 'department_159', 'designation': 'designation_159'},
        {'name': 'name_160', 'email': '8mail.ml', 'department': 'department_160', 'designation': 'designation_160'},
        {'name': 'name_161', 'email': '99.com', 'department': 'department_161', 'designation': 'designation_161'},
        {'name': 'name_162', 'email': '99cows.com', 'department': 'department_162', 'designation': 'designation_162'},
        {'name': 'name_163', 'email': '99experts.com', 'department': 'department_163', 'designation': 'designation_163'},
        {'name': 'name_164', 'email': '9mail.cf', 'department': 'department_164', 'designation': 'designation_164'},
        {'name': 'name_165', 'email': '9me.site', 'department': 'department_165', 'designation': 'designation_165'},
        {'name': 'name_166', 'email': '9mot.ru', 'department': 'department_166', 'designation': 'designation_166'},
        {'name': 'name_167', 'email': '9ox.net', 'department': 'department_167', 'designation': 'designation_167'},
        {'name': 'name_168', 'email': '9q.ro', 'department': 'department_168', 'designation': 'designation_168'},
        {'name': 'name_169', 'email': 'a-bc.net', 'department': 'department_169', 'designation': 'designation_169'},
        {'name': 'name_170', 'email': 'a45.in', 'department': 'department_170', 'designation': 'designation_170'},
        {'name': 'name_171', 'email': 'a7996.com', 'department': 'department_171', 'designation': 'designation_171'},
        {'name': 'name_172', 'email': 'aa5zy64.com', 'department': 'department_172', 'designation': 'designation_172'},
        {'name': 'name_173', 'email': 'aaqwe.ru', 'department': 'department_173', 'designation': 'designation_173'},
        {'name': 'name_174', 'email': 'aaqwe.store', 'department': 'department_174', 'designation': 'designation_174'},
        {'name': 'name_175', 'email': 'abacuswe.us', 'department': 'department_175', 'designation': 'designation_175'},
        {'name': 'name_176', 'email': 'abakiss.com', 'department': 'department_176', 'designation': 'designation_176'},
        {'name': 'name_177', 'email': 'abatido.com', 'department': 'department_177', 'designation': 'designation_177'},
        {'name': 'name_178', 'email': 'abcmail.email', 'department': 'department_178', 'designation': 'designation_178'},
        {'name': 'name_179', 'email': 'abevw.com', 'department': 'department_179', 'designation': 'designation_179'},
        {'name': 'name_180', 'email': 'abilitywe.us', 'department': 'department_180', 'designation': 'designation_180'},
        {'name': 'name_181', 'email': 'abovewe.us', 'department': 'department_181', 'designation': 'designation_181'},
        {'name': 'name_182', 'email': 'absolutewe.us', 'department': 'department_182', 'designation': 'designation_182'},
        {'name': 'name_183', 'email': 'abundantwe.us', 'department': 'department_183', 'designation': 'designation_183'},
        {'name': 'name_184', 'email': 'abusemail.de', 'department': 'department_184', 'designation': 'designation_184'},
        {'name': 'name_185', 'email': 'abuser.eu', 'department': 'department_185', 'designation': 'designation_185'},
        {'name': 'name_186', 'email': 'abyssmail.com', 'department': 'department_186', 'designation': 'designation_186'},
        {'name': 'name_187', 'email': 'ac20mail.in', 'department': 'department_187', 'designation': 'designation_187'},
        {'name': 'name_188', 'email': 'academiccommunity.com', 'department': 'department_188', 'designation': 'designation_188'},
        {'name': 'name_189', 'email': 'academywe.us', 'department': 'department_189', 'designation': 'designation_189'},
        {'name': 'name_190', 'email': 'acceleratewe.us', 'department': 'department_190', 'designation': 'designation_190'},
        {'name': 'name_191', 'email': 'accentwe.us', 'department': 'department_191', 'designation': 'designation_191'},
        {'name': 'name_192', 'email': 'acceptwe.us', 'department': 'department_192', 'designation': 'designation_192'},
        {'name': 'name_193', 'email': 'acclaimwe.us', 'department': 'department_193', 'designation': 'designation_193'},
        {'name': 'name_194', 'email': 'accordwe.us', 'department': 'department_194', 'designation': 'designation_194'},
        {'name': 'name_195', 'email': 'accreditedwe.us', 'department': 'department_195', 'designation': 'designation_195'},
        {'name': 'name_196', 'email': 'achievementwe.us', 'department': 'department_196', 'designation': 'designation_196'},
        {'name': 'name_197', 'email': 'achievewe.us', 'department': 'department_197', 'designation': 'designation_197'},
        {'name': 'name_198', 'email': 'acornwe.us', 'department': 'department_198', 'designation': 'designation_198'},
        {'name': 'name_199', 'email': 'acrossgracealley.com', 'department': 'department_199', 'designation': 'designation_199'},
        {'name': 'name_200', 'email': 'acrylicwe.us', 'department': 'department_200', 'designation': 'designation_200'},
        {'name': 'name_201', 'email': 'activatewe.us', 'department': 'department_201', 'designation': 'designation_201'},
        {'name': 'name_202', 'email': 'activitywe.us', 'department': 'department_202', 'designation': 'designation_202'},
        {'name': 'name_203', 'email': 'acucre.com', 'department': 'department_203', 'designation': 'designation_203'},
        {'name': 'name_204', 'email': 'acuitywe.us', 'department': 'department_204', 'designation': 'designation_204'},
        {'name': 'name_205', 'email': 'acumenwe.us', 'department': 'department_205', 'designation': 'designation_205'},
        {'name': 'name_206', 'email': 'adaptivewe.us', 'department': 'department_206', 'designation': 'designation_206'},
        {'name': 'name_207', 'email': 'adaptwe.us', 'department': 'department_207', 'designation': 'designation_207'},
        {'name': 'name_208', 'email': 'add3000.pp.ua', 'department': 'department_208', 'designation': 'designation_208'},
        {'name': 'name_209', 'email': 'addictingtrailers.com', 'department': 'department_209', 'designation': 'designation_209'},
        {'name': 'name_210', 'email': 'adeptwe.us', 'department': 'department_210', 'designation': 'designation_210'},
        {'name': 'name_211', 'email': 'adfskj.com', 'department': 'department_211', 'designation': 'designation_211'},
        {'name': 'name_212', 'email': 'adios.email', 'department': 'department_212', 'designation': 'designation_212'},
        {'name': 'name_213', 'email': 'adiq.eu', 'department': 'department_213', 'designation': 'designation_213'},
        {'name': 'name_214', 'email': 'aditus.info', 'department': 'department_214', 'designation': 'designation_214'},
        {'name': 'name_215', 'email': 'admiralwe.us', 'department': 'department_215', 'designation': 'designation_215'},
        {'name': 'name_216', 'email': 'ado888.biz', 'department': 'department_216', 'designation': 'designation_216'},
        {'name': 'name_217', 'email': 'adobeccepdm.com', 'department': 'department_217', 'designation': 'designation_217'},
        {'name': 'name_218', 'email': 'adoniswe.us', 'department': 'department_218', 'designation': 'designation_218'},
        {'name': 'name_219', 'email': 'adpugh.org', 'department': 'department_219', 'designation': 'designation_219'},
        {'name': 'name_220', 'email': 'adroh.com', 'department': 'department_220', 'designation': 'designation_220'},
        {'name': 'name_221', 'email': 'adsd.org', 'department': 'department_221', 'designation': 'designation_221'},
        {'name': 'name_222', 'email': 'adubiz.info', 'department': 'department_222', 'designation': 'designation_222'},
        {'name': 'name_223', 'email': 'adult-work.info', 'department': 'department_223', 'designation': 'designation_223'},
        {'name': 'name_224', 'email': 'advantagewe.us', 'department': 'department_224', 'designation': 'designation_224'},
        {'name': 'name_225', 'email': 'advantimo.com', 'department': 'department_225', 'designation': 'designation_225'},
        {'name': 'name_226', 'email': 'adventurewe.us', 'department': 'department_226', 'designation': 'designation_226'},
        {'name': 'name_227', 'email': 'adventwe.us', 'department': 'department_227', 'designation': 'designation_227'},
        {'name': 'name_228', 'email': 'advisorwe.us', 'department': 'department_228', 'designation': 'designation_228'},
        {'name': 'name_229', 'email': 'advocatewe.us', 'department': 'department_229', 'designation': 'designation_229'},
        {'name': 'name_230', 'email': 'adwaterandstir.com', 'department': 'department_230', 'designation': 'designation_230'},
        {'name': 'name_231', 'email': 'aegde.com', 'department': 'department_231', 'designation': 'designation_231'},
        {'name': 'name_232', 'email': 'aegia.net', 'department': 'department_232', 'designation': 'designation_232'},
        {'name': 'name_233', 'email': 'aegiscorp.net', 'department': 'department_233', 'designation': 'designation_233'},
        {'name': 'name_234', 'email': 'aegiswe.us', 'department': 'department_234', 'designation': 'designation_234'},
        {'name': 'name_235', 'email': 'aelo.es', 'department': 'department_235', 'designation': 'designation_235'},
        {'name': 'name_236', 'email': 'aeonpsi.com', 'department': 'department_236', 'designation': 'designation_236'},
        {'name': 'name_237', 'email': 'afarek.com', 'department': 'department_237', 'designation': 'designation_237'},
        {'name': 'name_238', 'email': 'affiliate-nebenjob.info', 'department': 'department_238', 'designation': 'designation_238'},
        {'name': 'name_239', 'email': 'affiliatedwe.us', 'department': 'department_239', 'designation': 'designation_239'},
        {'name': 'name_240', 'email': 'affilikingz.de', 'department': 'department_240', 'designation': 'designation_240'},
        {'name': 'name_241', 'email': 'affinitywe.us', 'department': 'department_241', 'designation': 'designation_241'},
        {'name': 'name_242', 'email': 'affluentwe.us', 'department': 'department_242', 'designation': 'designation_242'},
        {'name': 'name_243', 'email': 'affordablewe.us', 'department': 'department_243', 'designation': 'designation_243'},
        {'name': 'name_244', 'email': 'afia.pro', 'department': 'department_244', 'designation': 'designation_244'},
        {'name': 'name_245', 'email': 'afrobacon.com', 'department': 'department_245', 'designation': 'designation_245'},
        {'name': 'name_246', 'email': 'afterhourswe.us', 'department': 'department_246', 'designation': 'designation_246'},
        {'name': 'name_247', 'email': 'agedmail.com', 'department': 'department_247', 'designation': 'designation_247'},
        {'name': 'name_248', 'email': 'agendawe.us', 'department': 'department_248', 'designation': 'designation_248'},
        {'name': 'name_249', 'email': 'agger.ro', 'department': 'department_249', 'designation': 'designation_249'},
        {'name': 'name_250', 'email': 'agilewe.us', 'department': 'department_250', 'designation': 'designation_250'},
        {'name': 'name_251', 'email': 'agorawe.us', 'department': 'department_251', 'designation': 'designation_251'},
        {'name': 'name_252', 'email': 'agtx.net', 'department': 'department_252', 'designation': 'designation_252'},
        {'name': 'name_253', 'email': 'aheadwe.us', 'department': 'department_253', 'designation': 'designation_253'},
        {'name': 'name_254', 'email': 'ahem.email', 'department': 'department_254', 'designation': 'designation_254'},
        {'name': 'name_255', 'email': 'ahk.jp', 'department': 'department_255', 'designation': 'designation_255'},
        {'name': 'name_256', 'email': 'ahmedkhlef.com', 'department': 'department_256', 'designation': 'designation_256'},
        {'name': 'name_257', 'email': 'air2token.com', 'department': 'department_257', 'designation': 'designation_257'},
        {'name': 'name_258', 'email': 'airmailbox.website', 'department': 'department_258', 'designation': 'designation_258'},
        {'name': 'name_259', 'email': 'airsi.de', 'department': 'department_259', 'designation': 'designation_259'},
        {'name': 'name_260', 'email': 'aiworldx.com', 'department': 'department_260', 'designation': 'designation_260'},
        {'name': 'name_261', 'email': 'ajaxapp.net', 'department': 'department_261', 'designation': 'designation_261'},
        {'name': 'name_262', 'email': 'akapost.com', 'department': 'department_262', 'designation': 'designation_262'},
        {'name': 'name_263', 'email': 'akerd.com', 'department': 'department_263', 'designation': 'designation_263'},
        {'name': 'name_264', 'email': 'akgq701.com', 'department': 'department_264', 'designation': 'designation_264'},
        {'name': 'name_265', 'email': 'akmail.in', 'department': 'department_265', 'designation': 'designation_265'},
        {'name': 'name_266', 'email': 'akugu.com', 'department': 'department_266', 'designation': 'designation_266'},
        {'name': 'name_267', 'email': 'al-qaeda.us', 'department': 'department_267', 'designation': 'designation_267'},
        {'name': 'name_268', 'email': 'albionwe.us', 'department': 'department_268', 'designation': 'designation_268'},
        {'name': 'name_269', 'email': 'alchemywe.us', 'department': 'department_269', 'designation': 'designation_269'},
        {'name': 'name_270', 'email': 'alfaceti.com', 'department': 'department_270', 'designation': 'designation_270'},
        {'name': 'name_271', 'email': 'aliaswe.us', 'department': 'department_271', 'designation': 'designation_271'},
        {'name': 'name_272', 'email': 'alienware13.com', 'department': 'department_272', 'designation': 'designation_272'},
        {'name': 'name_273', 'email': 'aligamel.com', 'department': 'department_273', 'designation': 'designation_273'},
        {'name': 'name_274', 'email': 'alina-schiesser.ch', 'department': 'department_274', 'designation': 'designation_274'},
        {'name': 'name_275', 'email': 'alisongamel.com', 'department': 'department_275', 'designation': 'designation_275'},
        {'name': 'name_276', 'email': 'alivance.com', 'department': 'department_276', 'designation': 'designation_276'},
        {'name': 'name_277', 'email': 'alivewe.us', 'department': 'department_277', 'designation': 'designation_277'},
        {'name': 'name_278', 'email': 'all-cats.ru', 'department': 'department_278', 'designation': 'designation_278'},
        {'name': 'name_279', 'email': 'allaccesswe.us', 'department': 'department_279', 'designation': 'designation_279'},
        {'name': 'name_280', 'email': 'allamericanwe.us', 'department': 'department_280', 'designation': 'designation_280'},
        {'name': 'name_281', 'email': 'allaroundwe.us', 'department': 'department_281', 'designation': 'designation_281'},
        {'name': 'name_282', 'email': 'alldirectbuy.com', 'department': 'department_282', 'designation': 'designation_282'},
        {'name': 'name_283', 'email': 'allegiancewe.us', 'department': 'department_283', 'designation': 'designation_283'},
        {'name': 'name_284', 'email': 'allegrowe.us', 'department': 'department_284', 'designation': 'designation_284'},
        {'name': 'name_285', 'email': 'allemojikeyboard.com', 'department': 'department_285', 'designation': 'designation_285'},
        {'name': 'name_286', 'email': 'allgoodwe.us', 'department': 'department_286', 'designation': 'designation_286'},
        {'name': 'name_287', 'email': 'alliancewe.us', 'department': 'department_287', 'designation': 'designation_287'},
        {'name': 'name_288', 'email': 'allinonewe.us', 'department': 'department_288', 'designation': 'designation_288'},
        {'name': 'name_289', 'email': 'allofthem.net', 'department': 'department_289', 'designation': 'designation_289'},
        {'name': 'name_290', 'email': 'alloutwe.us', 'department': 'department_290', 'designation': 'designation_290'},
        {'name': 'name_291', 'email': 'allowed.org', 'department': 'department_291', 'designation': 'designation_291'},
        {'name': 'name_292', 'email': 'alloywe.us', 'department': 'department_292', 'designation': 'designation_292'},
        {'name': 'name_293', 'email': 'allprowe.us', 'department': 'department_293', 'designation': 'designation_293'},
        {'name': 'name_294', 'email': 'allseasonswe.us', 'department': 'department_294', 'designation': 'designation_294'},
        {'name': 'name_295', 'email': 'allstarwe.us', 'department': 'department_295', 'designation': 'designation_295'},
        {'name': 'name_296', 'email': 'allthegoodnamesaretaken.org', 'department': 'department_296', 'designation': 'designation_296'},
        {'name': 'name_297', 'email': 'allurewe.us', 'department': 'department_297', 'designation': 'designation_297'},
        {'name': 'name_298', 'email': 'almondwe.us', 'department': 'department_298', 'designation': 'designation_298'},
        {'name': 'name_299', 'email': 'alph.wtf', 'department': 'department_299', 'designation': 'designation_299'},
        {'name': 'name_300', 'email': 'alpha-web.net', 'department': 'department_300', 'designation': 'designation_300'},
        {'name': 'name_301', 'email': 'alphaomegawe.us', 'department': 'department_301', 'designation': 'designation_301'},
        {'name': 'name_302', 'email': 'alpinewe.us', 'department': 'department_302', 'designation': 'designation_302'},
        {'name': 'name_303', 'email': 'altairwe.us', 'department': 'department_303', 'designation': 'designation_303'},
        {'name': 'name_304', 'email': 'altitudewe.us', 'department': 'department_304', 'designation': 'designation_304'},
        {'name': 'name_305', 'email': 'altuswe.us', 'department': 'department_305', 'designation': 'designation_305'},
        {'name': 'name_306', 'email': 'ama-trade.de', 'department': 'department_306', 'designation': 'designation_306'},
        {'name': 'name_307', 'email': 'ama-trans.de', 'department': 'department_307', 'designation': 'designation_307'},
        {'name': 'name_308', 'email': 'amadeuswe.us', 'department': 'department_308', 'designation': 'designation_308'},
        {'name': 'name_309', 'email': 'amail.club', 'department': 'department_309', 'designation': 'designation_309'},
        {'name': 'name_310', 'email': 'amail.com', 'department': 'department_310', 'designation': 'designation_310'},
        {'name': 'name_311', 'email': 'amail1.com', 'department': 'department_311', 'designation': 'designation_311'},
        {'name': 'name_312', 'email': 'amail4.me', 'department': 'department_312', 'designation': 'designation_312'},
        {'name': 'name_313', 'email': 'amazon-aws.org', 'department': 'department_313', 'designation': 'designation_313'},
        {'name': 'name_314', 'email': 'amberwe.us', 'department': 'department_314', 'designation': 'designation_314'},
        {'name': 'name_315', 'email': 'ambiancewe.us', 'department': 'department_315', 'designation': 'designation_315'},
        {'name': 'name_316', 'email': 'ambitiouswe.us', 'department': 'department_316', 'designation': 'designation_316'},
        {'name': 'name_317', 'email': 'amelabs.com', 'department': 'department_317', 'designation': 'designation_317'},
        {'name': 'name_318', 'email': 'americanawe.us', 'department': 'department_318', 'designation': 'designation_318'},
        {'name': 'name_319', 'email': 'americasbestwe.us', 'department': 'department_319', 'designation': 'designation_319'},
        {'name': 'name_320', 'email': 'americaswe.us', 'department': 'department_320', 'designation': 'designation_320'},
        {'name': 'name_321', 'email': 'amicuswe.us', 'department': 'department_321', 'designation': 'designation_321'},
        {'name': 'name_322', 'email': 'amilegit.com', 'department': 'department_322', 'designation': 'designation_322'},
        {'name': 'name_323', 'email': 'amiri.net', 'department': 'department_323', 'designation': 'designation_323'},
        {'name': 'name_324', 'email': 'amiriindustries.com', 'department': 'department_324', 'designation': 'designation_324'},
        {'name': 'name_325', 'email': 'amplewe.us', 'department': 'department_325', 'designation': 'designation_325'},
        {'name': 'name_326', 'email': 'amplifiedwe.us', 'department': 'department_326', 'designation': 'designation_326'},
        {'name': 'name_327', 'email': 'amplifywe.us', 'department': 'department_327', 'designation': 'designation_327'},
        {'name': 'name_328', 'email': 'ampsylike.com', 'department': 'department_328', 'designation': 'designation_328'},
        {'name': 'name_329', 'email': 'analogwe.us', 'department': 'department_329', 'designation': 'designation_329'},
        {'name': 'name_330', 'email': 'analysiswe.us', 'department': 'department_330', 'designation': 'designation_330'},
        {'name': 'name_331', 'email': 'analyticalwe.us', 'department': 'department_331', 'designation': 'designation_331'},
        {'name': 'name_332', 'email': 'analyticswe.us', 'department': 'department_332', 'designation': 'designation_332'},
        {'name': 'name_333', 'email': 'analyticwe.us', 'department': 'department_333', 'designation': 'designation_333'},
        {'name': 'name_334', 'email': 'anappfor.com', 'department': 'department_334', 'designation': 'designation_334'},
        {'name': 'name_335', 'email': 'anappthat.com', 'department': 'department_335', 'designation': 'designation_335'},
        {'name': 'name_336', 'email': 'andreihusanu.ro', 'department': 'department_336', 'designation': 'designation_336'},
        {'name': 'name_337', 'email': 'andthen.us', 'department': 'department_337', 'designation': 'designation_337'},
        {'name': 'name_338', 'email': 'animesos.com', 'department': 'department_338', 'designation': 'designation_338'},
        {'name': 'name_339', 'email': 'anit.ro', 'department': 'department_339', 'designation': 'designation_339'},
        {'name': 'name_340', 'email': 'ano-mail.net', 'department': 'department_340', 'designation': 'designation_340'},
        {'name': 'name_341', 'email': 'anon-mail.de', 'department': 'department_341', 'designation': 'designation_341'},
        {'name': 'name_342', 'email': 'anonbox.net', 'department': 'department_342', 'designation': 'designation_342'},
        {'name': 'name_343', 'email': 'anonmail.top', 'department': 'department_343', 'designation': 'designation_343'},
        {'name': 'name_344', 'email': 'anonmails.de', 'department': 'department_344', 'designation': 'designation_344'},
        {'name': 'name_345', 'email': 'anonymail.dk', 'department': 'department_345', 'designation': 'designation_345'},
        {'name': 'name_346', 'email': 'anonymbox.com', 'department': 'department_346', 'designation': 'designation_346'},
        {'name': 'name_347', 'email': 'anonymized.org', 'department': 'department_347', 'designation': 'designation_347'},
        {'name': 'name_348', 'email': 'anonymousness.com', 'department': 'department_348', 'designation': 'designation_348'},
        {'name': 'name_349', 'email': 'anotherdomaincyka.tk', 'department': 'department_349', 'designation': 'designation_349'},
        {'name': 'name_350', 'email': 'ansibleemail.com', 'department': 'department_350', 'designation': 'designation_350'},
        {'name': 'name_351', 'email': 'anthony-junkmail.com', 'department': 'department_351', 'designation': 'designation_351'},
        {'name': 'name_352', 'email': 'antireg.com', 'department': 'department_352', 'designation': 'designation_352'},
        {'name': 'name_353', 'email': 'antireg.ru', 'department': 'department_353', 'designation': 'designation_353'},
        {'name': 'name_354', 'email': 'antispam.de', 'department': 'department_354', 'designation': 'designation_354'},
        {'name': 'name_355', 'email': 'antispam24.de', 'department': 'department_355', 'designation': 'designation_355'},
        {'name': 'name_356', 'email': 'antispammail.de', 'department': 'department_356', 'designation': 'designation_356'},
        {'name': 'name_357', 'email': 'any.pink', 'department': 'department_357', 'designation': 'designation_357'},
        {'name': 'name_358', 'email': 'anyalias.com', 'department': 'department_358', 'designation': 'designation_358'},
        {'name': 'name_359', 'email': 'aoeuhtns.com', 'department': 'department_359', 'designation': 'designation_359'},
        {'name': 'name_360', 'email': 'apfelkorps.de', 'department': 'department_360', 'designation': 'designation_360'},
        {'name': 'name_361', 'email': 'aphlog.com', 'department': 'department_361', 'designation': 'designation_361'},
        {'name': 'name_362', 'email': 'apkmd.com', 'department': 'department_362', 'designation': 'designation_362'},
        {'name': 'name_363', 'email': 'appc.se', 'department': 'department_363', 'designation': 'designation_363'},
        {'name': 'name_364', 'email': 'appinventor.nl', 'department': 'department_364', 'designation': 'designation_364'},
        {'name': 'name_365', 'email': 'appixie.com', 'department': 'department_365', 'designation': 'designation_365'},
        {'name': 'name_366', 'email': 'apps.dj', 'department': 'department_366', 'designation': 'designation_366'},
        {'name': 'name_367', 'email': 'appzily.com', 'department': 'department_367', 'designation': 'designation_367'},
        {'name': 'name_368', 'email': 'arduino.hk', 'department': 'department_368', 'designation': 'designation_368'},
        {'name': 'name_369', 'email': 'ariaz.jetzt', 'department': 'department_369', 'designation': 'designation_369'},
        {'name': 'name_370', 'email': 'armyspy.com', 'department': 'department_370', 'designation': 'designation_370'},
        {'name': 'name_371', 'email': 'aron.us', 'department': 'department_371', 'designation': 'designation_371'},
        {'name': 'name_372', 'email': 'arroisijewellery.com', 'department': 'department_372', 'designation': 'designation_372'},
        {'name': 'name_373', 'email': 'art-en-ligne.pro', 'department': 'department_373', 'designation': 'designation_373'},
        {'name': 'name_374', 'email': 'artman-conception.com', 'department': 'department_374', 'designation': 'designation_374'},
        {'name': 'name_375', 'email': 'arur01.tk', 'department': 'department_375', 'designation': 'designation_375'},
        {'name': 'name_376', 'email': 'arurgitu.gq', 'department': 'department_376', 'designation': 'designation_376'},
        {'name': 'name_377', 'email': 'arvato-community.de', 'department': 'department_377', 'designation': 'designation_377'},
        {'name': 'name_378', 'email': 'aschenbrandt.net', 'department': 'department_378', 'designation': 'designation_378'},
        {'name': 'name_379', 'email': 'asdasd.nl', 'department': 'department_379', 'designation': 'designation_379'},
        {'name': 'name_380', 'email': 'asdasd.ru', 'department': 'department_380', 'designation': 'designation_380'},
        {'name': 'name_381', 'email': 'ashleyandrew.com', 'department': 'department_381', 'designation': 'designation_381'},
        {'name': 'name_382', 'email': 'ask-mail.com', 'department': 'department_382', 'designation': 'designation_382'},
        {'name': 'name_383', 'email': 'asorent.com', 'department': 'department_383', 'designation': 'designation_383'},
        {'name': 'name_384', 'email': 'ass.pp.ua', 'department': 'department_384', 'designation': 'designation_384'},
        {'name': 'name_385', 'email': 'astonut.tk', 'department': 'department_385', 'designation': 'designation_385'},
        {'name': 'name_386', 'email': 'astroempires.info', 'department': 'department_386', 'designation': 'designation_386'},
        {'name': 'name_387', 'email': 'asu.mx', 'department': 'department_387', 'designation': 'designation_387'},
        {'name': 'name_388', 'email': 'asu.su', 'department': 'department_388', 'designation': 'designation_388'},
        {'name': 'name_389', 'email': 'at.hm', 'department': 'department_389', 'designation': 'designation_389'},
        {'name': 'name_390', 'email': 'at0mik.org', 'department': 'department_390', 'designation': 'designation_390'},
        {'name': 'name_391', 'email': 'atnextmail.com', 'department': 'department_391', 'designation': 'designation_391'},
        {'name': 'name_392', 'email': 'attnetwork.com', 'department': 'department_392', 'designation': 'designation_392'},
        {'name': 'name_393', 'email': 'augmentationtechnology.com', 'department': 'department_393', 'designation': 'designation_393'},
        {'name': 'name_394', 'email': 'ausgefallen.info', 'department': 'department_394', 'designation': 'designation_394'},
        {'name': 'name_395', 'email': 'auti.st', 'department': 'department_395', 'designation': 'designation_395'},
        {'name': 'name_396', 'email': 'autorobotica.com', 'department': 'department_396', 'designation': 'designation_396'},
        {'name': 'name_397', 'email': 'autosouvenir39.ru', 'department': 'department_397', 'designation': 'designation_397'},
        {'name': 'name_398', 'email': 'autotwollow.com', 'department': 'department_398', 'designation': 'designation_398'},
        {'name': 'name_399', 'email': 'autowb.com', 'department': 'department_399', 'designation': 'designation_399'},
        {'name': 'name_400', 'email': 'averdov.com', 'department': 'department_400', 'designation': 'designation_400'},
        {'name': 'name_401', 'email': 'avia-tonic.fr', 'department': 'department_401', 'designation': 'designation_401'},
        {'name': 'name_402', 'email': 'avls.pt', 'department': 'department_402', 'designation': 'designation_402'},
        {'name': 'name_403', 'email': 'awatum.de', 'department': 'department_403', 'designation': 'designation_403'},
        {'name': 'name_404', 'email': 'awdrt.org', 'department': 'department_404', 'designation': 'designation_404'},
        {'name': 'name_405', 'email': 'awiki.org', 'department': 'department_405', 'designation': 'designation_405'},
        {'name': 'name_406', 'email': 'awsoo.com', 'department': 'department_406', 'designation': 'designation_406'},
        {'name': 'name_407', 'email': 'axiz.org', 'department': 'department_407', 'designation': 'designation_407'},
        {'name': 'name_408', 'email': 'axon7zte.com', 'department': 'department_408', 'designation': 'designation_408'},
        {'name': 'name_409', 'email': 'axsup.net', 'department': 'department_409', 'designation': 'designation_409'},
        {'name': 'name_410', 'email': 'ayakamail.cf', 'department': 'department_410', 'designation': 'designation_410'},
        {'name': 'name_411', 'email': 'azazazatashkent.tk', 'department': 'department_411', 'designation': 'designation_411'},
        {'name': 'name_412', 'email': 'azcomputerworks.com', 'department': 'department_412', 'designation': 'designation_412'},
        {'name': 'name_413', 'email': 'azmeil.tk', 'department': 'department_413', 'designation': 'designation_413'},
        {'name': 'name_414', 'email': 'b1of96u.com', 'department': 'department_414', 'designation': 'designation_414'},
        {'name': 'name_415', 'email': 'b2bx.net', 'department': 'department_415', 'designation': 'designation_415'},
        {'name': 'name_416', 'email': 'b2cmail.de', 'department': 'department_416', 'designation': 'designation_416'},
        {'name': 'name_417', 'email': 'badgerland.eu', 'department': 'department_417', 'designation': 'designation_417'},
        {'name': 'name_418', 'email': 'badoop.com', 'department': 'department_418', 'designation': 'designation_418'},
        {'name': 'name_419', 'email': 'badpotato.tk', 'department': 'department_419', 'designation': 'designation_419'},
        {'name': 'name_420', 'email': 'balaket.com', 'department': 'department_420', 'designation': 'designation_420'},
        {'name': 'name_421', 'email': 'bangban.uk', 'department': 'department_421', 'designation': 'designation_421'},
        {'name': 'name_422', 'email': 'banit.club', 'department': 'department_422', 'designation': 'designation_422'},
        {'name': 'name_423', 'email': 'banit.me', 'department': 'department_423', 'designation': 'designation_423'},
        {'name': 'name_424', 'email': 'bank-opros1.ru', 'department': 'department_424', 'designation': 'designation_424'},
        {'name': 'name_425', 'email': 'bareed.ws', 'department': 'department_425', 'designation': 'designation_425'},
        {'name': 'name_426', 'email': 'barooko.com', 'department': 'department_426', 'designation': 'designation_426'},
        {'name': 'name_427', 'email': 'barryogorman.com', 'department': 'department_427', 'designation': 'designation_427'},
        {'name': 'name_428', 'email': 'bartdevos.be', 'department': 'department_428', 'designation': 'designation_428'},
        {'name': 'name_429', 'email': 'basscode.org', 'department': 'department_429', 'designation': 'designation_429'},
        {'name': 'name_430', 'email': 'bauwerke-online.com', 'department': 'department_430', 'designation': 'designation_430'},
        {'name': 'name_431', 'email': 'bazaaboom.com', 'department': 'department_431', 'designation': 'designation_431'},
        {'name': 'name_432', 'email': 'bbbbyyzz.info', 'department': 'department_432', 'designation': 'designation_432'},
        {'name': 'name_433', 'email': 'bbhost.us', 'department': 'department_433', 'designation': 'designation_433'},
        {'name': 'name_434', 'email': 'bbitf.com', 'department': 'department_434', 'designation': 'designation_434'},
        {'name': 'name_435', 'email': 'bbitj.com', 'department': 'department_435', 'designation': 'designation_435'},
        {'name': 'name_436', 'email': 'bbitq.com', 'department': 'department_436', 'designation': 'designation_436'},
        {'name': 'name_437', 'email': 'bcaoo.com', 'department': 'department_437', 'designation': 'designation_437'},
        {'name': 'name_438', 'email': 'bcast.ws', 'department': 'department_438', 'designation': 'designation_438'},
        {'name': 'name_439', 'email': 'bcb.ro', 'department': 'department_439', 'designation': 'designation_439'},
        {'name': 'name_440', 'email': 'bccto.me', 'department': 'department_440', 'designation': 'designation_440'},
        {'name': 'name_441', 'email': 'bdmuzic.pw', 'department': 'department_441', 'designation': 'designation_441'},
        {'name': 'name_442', 'email': 'beaconmessenger.com', 'department': 'department_442', 'designation': 'designation_442'},
        {'name': 'name_443', 'email': 'bearsarefuzzy.com', 'department': 'department_443', 'designation': 'designation_443'},
        {'name': 'name_444', 'email': 'beddly.com', 'department': 'department_444', 'designation': 'designation_444'},
        {'name': 'name_445', 'email': 'beefmilk.com', 'department': 'department_445', 'designation': 'designation_445'},
        {'name': 'name_446', 'email': 'belamail.org', 'department': 'department_446', 'designation': 'designation_446'},
        {'name': 'name_447', 'email': 'belgianairways.com', 'department': 'department_447', 'designation': 'designation_447'},
        {'name': 'name_448', 'email': 'belljonestax.com', 'department': 'department_448', 'designation': 'designation_448'},
        {'name': 'name_449', 'email': 'beluckygame.com', 'department': 'department_449', 'designation': 'designation_449'},
        {'name': 'name_450', 'email': 'benipaula.org', 'department': 'department_450', 'designation': 'designation_450'},
        {'name': 'name_451', 'email': 'bepureme.com', 'department': 'department_451', 'designation': 'designation_451'},
        {'name': 'name_452', 'email': 'beribase.ru', 'department': 'department_452', 'designation': 'designation_452'},
        {'name': 'name_453', 'email': 'beribaza.ru', 'department': 'department_453', 'designation': 'designation_453'},
        {'name': 'name_454', 'email': 'berirabotay.ru', 'department': 'department_454', 'designation': 'designation_454'},
        {'name': 'name_455', 'email': 'best-john-boats.com', 'department': 'department_455', 'designation': 'designation_455'},
        {'name': 'name_456', 'email': 'bestchoiceusedcar.com', 'department': 'department_456', 'designation': 'designation_456'},
        {'name': 'name_457', 'email': 'bestlistbase.com', 'department': 'department_457', 'designation': 'designation_457'},
        {'name': 'name_458', 'email': 'bestoption25.club', 'department': 'department_458', 'designation': 'designation_458'},
        {'name': 'name_459', 'email': 'bestparadize.com', 'department': 'department_459', 'designation': 'designation_459'},
        {'name': 'name_460', 'email': 'bestsoundeffects.com', 'department': 'department_460', 'designation': 'designation_460'},
        {'name': 'name_461', 'email': 'besttempmail.com', 'department': 'department_461', 'designation': 'designation_461'},
        {'name': 'name_462', 'email': 'betr.co', 'department': 'department_462', 'designation': 'designation_462'},
        {'name': 'name_463', 'email': 'bgtmail.com', 'department': 'department_463', 'designation': 'designation_463'},
        {'name': 'name_464', 'email': 'bgx.ro', 'department': 'department_464', 'designation': 'designation_464'},
        {'name': 'name_465', 'email': 'bheps.com', 'department': 'department_465', 'designation': 'designation_465'},
        {'name': 'name_466', 'email': 'bidourlnks.com', 'department': 'department_466', 'designation': 'designation_466'},
        {'name': 'name_467', 'email': 'big1.us', 'department': 'department_467', 'designation': 'designation_467'},
        {'name': 'name_468', 'email': 'bigprofessor.so', 'department': 'department_468', 'designation': 'designation_468'},
        {'name': 'name_469', 'email': 'bigstring.com', 'department': 'department_469', 'designation': 'designation_469'},
        {'name': 'name_470', 'email': 'bigwhoop.co.za', 'department': 'department_470', 'designation': 'designation_470'},
        {'name': 'name_471', 'email': 'bij.pl', 'department': 'department_471', 'designation': 'designation_471'},
        {'name': 'name_472', 'email': 'binka.me', 'department': 'department_472', 'designation': 'designation_472'},
        {'name': 'name_473', 'email': 'binkmail.com', 'department': 'department_473', 'designation': 'designation_473'},
        {'name': 'name_474', 'email': 'binnary.com', 'department': 'department_474', 'designation': 'designation_474'},
        {'name': 'name_475', 'email': 'bio-muesli.info', 'department': 'department_475', 'designation': 'designation_475'},
        {'name': 'name_476', 'email': 'bio-muesli.net', 'department': 'department_476', 'designation': 'designation_476'},
        {'name': 'name_477', 'email': 'bione.co', 'department': 'department_477', 'designation': 'designation_477'},
        {'name': 'name_478', 'email': 'bitwhites.top', 'department': 'department_478', 'designation': 'designation_478'},
        {'name': 'name_479', 'email': 'bitymails.us', 'department': 'department_479', 'designation': 'designation_479'},
        {'name': 'name_480', 'email': 'blackgoldagency.ru', 'department': 'department_480', 'designation': 'designation_480'},
        {'name': 'name_481', 'email': 'blackmarket.to', 'department': 'department_481', 'designation': 'designation_481'},
        {'name': 'name_482', 'email': 'bladesmail.net', 'department': 'department_482', 'designation': 'designation_482'},
        {'name': 'name_483', 'email': 'blip.ch', 'department': 'department_483', 'designation': 'designation_483'},
        {'name': 'name_484', 'email': 'blnkt.net', 'department': 'department_484', 'designation': 'designation_484'},
        {'name': 'name_485', 'email': 'block521.com', 'department': 'department_485', 'designation': 'designation_485'},
        {'name': 'name_486', 'email': 'blogmyway.org', 'department': 'department_486', 'designation': 'designation_486'},
        {'name': 'name_487', 'email': 'blogos.net', 'department': 'department_487', 'designation': 'designation_487'},
        {'name': 'name_488', 'email': 'blogspam.ro', 'department': 'department_488', 'designation': 'designation_488'},
        {'name': 'name_489', 'email': 'blondemorkin.com', 'department': 'department_489', 'designation': 'designation_489'},
        {'name': 'name_490', 'email': 'blondmail.com', 'department': 'department_490', 'designation': 'designation_490'},
        {'name': 'name_491', 'email': 'bluedumpling.info', 'department': 'department_491', 'designation': 'designation_491'},
        {'name': 'name_492', 'email': 'bluewerks.com', 'department': 'department_492', 'designation': 'designation_492'},
        {'name': 'name_493', 'email': 'bnote.com', 'department': 'department_493', 'designation': 'designation_493'},
        {'name': 'name_494', 'email': 'boatmail.us', 'department': 'department_494', 'designation': 'designation_494'},
        {'name': 'name_495', 'email': 'bobgf.ru', 'department': 'department_495', 'designation': 'designation_495'},
        {'name': 'name_496', 'email': 'bobgf.store', 'department': 'department_496', 'designation': 'designation_496'},
        {'name': 'name_497', 'email': 'bobmail.info', 'department': 'department_497', 'designation': 'designation_497'},
        {'name': 'name_498', 'email': 'bobmurchison.com', 'department': 'department_498', 'designation': 'designation_498'},
        {'name': 'name_499', 'email': 'bofthew.com', 'department': 'department_499', 'designation': 'designation_499'},
        {'name': 'name_500', 'email': 'bonobo.email', 'department': 'department_500', 'designation': 'designation_500'},
        {'name': 'name_501', 'email': 'boofx.com', 'department': 'department_501', 'designation': 'designation_501'},
        {'name': 'name_502', 'email': 'bookthemmore.com', 'department': 'department_502', 'designation': 'designation_502'},
        {'name': 'name_503', 'email': 'bootybay.de', 'department': 'department_503', 'designation': 'designation_503'},
        {'name': 'name_504', 'email': 'borged.com', 'department': 'department_504', 'designation': 'designation_504'},
        {'name': 'name_505', 'email': 'borged.net', 'department': 'department_505', 'designation': 'designation_505'},
        {'name': 'name_506', 'email': 'borged.org', 'department': 'department_506', 'designation': 'designation_506'},
        {'name': 'name_507', 'email': 'bot.nu', 'department': 'department_507', 'designation': 'designation_507'},
        {'name': 'name_508', 'email': 'boun.cr', 'department': 'department_508', 'designation': 'designation_508'},
        {'name': 'name_509', 'email': 'bouncr.com', 'department': 'department_509', 'designation': 'designation_509'},
        {'name': 'name_510', 'email': 'box-mail.ru', 'department': 'department_510', 'designation': 'designation_510'},
        {'name': 'name_511', 'email': 'box-mail.store', 'department': 'department_511', 'designation': 'designation_511'},
        {'name': 'name_512', 'email': 'boxem.ru', 'department': 'department_512', 'designation': 'designation_512'},
        {'name': 'name_513', 'email': 'boxem.store', 'department': 'department_513', 'designation': 'designation_513'},
        {'name': 'name_514', 'email': 'boxformail.in', 'department': 'department_514', 'designation': 'designation_514'},
        {'name': 'name_515', 'email': 'boximail.com', 'department': 'department_515', 'designation': 'designation_515'},
        {'name': 'name_516', 'email': 'boxlet.ru', 'department': 'department_516', 'designation': 'designation_516'},
        {'name': 'name_517', 'email': 'boxlet.store', 'department': 'department_517', 'designation': 'designation_517'},
        {'name': 'name_518', 'email': 'boxmail.lol', 'department': 'department_518', 'designation': 'designation_518'},
        {'name': 'name_519', 'email': 'boxomail.live', 'department': 'department_519', 'designation': 'designation_519'},
        {'name': 'name_520', 'email': 'boxtemp.com.br', 'department': 'department_520', 'designation': 'designation_520'},
        {'name': 'name_521', 'email': 'bptfp.net', 'department': 'department_521', 'designation': 'designation_521'},
        {'name': 'name_522', 'email': 'brand-app.biz', 'department': 'department_522', 'designation': 'designation_522'},
        {'name': 'name_523', 'email': 'brandallday.net', 'department': 'department_523', 'designation': 'designation_523'},
        {'name': 'name_524', 'email': 'brasx.org', 'department': 'department_524', 'designation': 'designation_524'},
        {'name': 'name_525', 'email': 'breakthru.com', 'department': 'department_525', 'designation': 'designation_525'},
        {'name': 'name_526', 'email': 'brefmail.com', 'department': 'department_526', 'designation': 'designation_526'},
        {'name': 'name_527', 'email': 'brennendesreich.de', 'department': 'department_527', 'designation': 'designation_527'},
        {'name': 'name_528', 'email': 'briggsmarcus.com', 'department': 'department_528', 'designation': 'designation_528'},
        {'name': 'name_529', 'email': 'broadbandninja.com', 'department': 'department_529', 'designation': 'designation_529'},
        {'name': 'name_530', 'email': 'bsnow.net', 'department': 'department_530', 'designation': 'designation_530'},
        {'name': 'name_531', 'email': 'bspamfree.org', 'department': 'department_531', 'designation': 'designation_531'},
        {'name': 'name_532', 'email': 'bspooky.com', 'department': 'department_532', 'designation': 'designation_532'},
        {'name': 'name_533', 'email': 'bst-72.com', 'department': 'department_533', 'designation': 'designation_533'},
        {'name': 'name_534', 'email': 'btb-notes.com', 'department': 'department_534', 'designation': 'designation_534'},
        {'name': 'name_535', 'email': 'btc.email', 'department': 'department_535', 'designation': 'designation_535'},
        {'name': 'name_536', 'email': 'btcmail.pw', 'department': 'department_536', 'designation': 'designation_536'},
        {'name': 'name_537', 'email': 'btcmod.com', 'department': 'department_537', 'designation': 'designation_537'},
        {'name': 'name_538', 'email': 'btizet.pl', 'department': 'department_538', 'designation': 'designation_538'},
        {'name': 'name_539', 'email': 'buccalmassage.ru', 'department': 'department_539', 'designation': 'designation_539'},
        {'name': 'name_540', 'email': 'budaya-tionghoa.com', 'department': 'department_540', 'designation': 'designation_540'},
        {'name': 'name_541', 'email': 'budayationghoa.com', 'department': 'department_541', 'designation': 'designation_541'},
        {'name': 'name_542', 'email': 'buffemail.com', 'department': 'department_542', 'designation': 'designation_542'},
        {'name': 'name_543', 'email': 'bugfoo.com', 'department': 'department_543', 'designation': 'designation_543'},
        {'name': 'name_544', 'email': 'bugmenever.com', 'department': 'department_544', 'designation': 'designation_544'},
        {'name': 'name_545', 'email': 'bugmenot.com', 'department': 'department_545', 'designation': 'designation_545'},
        {'name': 'name_546', 'email': 'bukhariansiddur.com', 'department': 'department_546', 'designation': 'designation_546'},
        {'name': 'name_547', 'email': 'bulrushpress.com', 'department': 'department_547', 'designation': 'designation_547'},
        {'name': 'name_548', 'email': 'bum.net', 'department': 'department_548', 'designation': 'designation_548'},
        {'name': 'name_549', 'email': 'bumpymail.com', 'department': 'department_549', 'designation': 'designation_549'},
        {'name': 'name_550', 'email': 'bunchofidiots.com', 'department': 'department_550', 'designation': 'designation_550'},
        {'name': 'name_551', 'email': 'bund.us', 'department': 'department_551', 'designation': 'designation_551'},
        {'name': 'name_552', 'email': 'bundes-li.ga', 'department': 'department_552', 'designation': 'designation_552'},
        {'name': 'name_553', 'email': 'bunsenhoneydew.com', 'department': 'department_553', 'designation': 'designation_553'},
        {'name': 'name_554', 'email': 'burnthespam.info', 'department': 'department_554', 'designation': 'designation_554'},
        {'name': 'name_555', 'email': 'burstmail.info', 'department': 'department_555', 'designation': 'designation_555'},
        {'name': 'name_556', 'email': 'businessbackend.com', 'department': 'department_556', 'designation': 'designation_556'},
        {'name': 'name_557', 'email': 'businesssuccessislifesuccess.com', 'department': 'department_557', 'designation': 'designation_557'},
        {'name': 'name_558', 'email': 'buspad.org', 'department': 'department_558', 'designation': 'designation_558'},
        {'name': 'name_559', 'email': 'bussitussi.com', 'department': 'department_559', 'designation': 'designation_559'},
        {'name': 'name_560', 'email': 'buymoreplays.com', 'department': 'department_560', 'designation': 'designation_560'},
        {'name': 'name_561', 'email': 'buyordie.info', 'department': 'department_561', 'designation': 'designation_561'},
        {'name': 'name_562', 'email': 'buyusdomain.com', 'department': 'department_562', 'designation': 'designation_562'},
        {'name': 'name_563', 'email': 'buyusedlibrarybooks.org', 'department': 'department_563', 'designation': 'designation_563'},
        {'name': 'name_564', 'email': 'buzzcluby.com', 'department': 'department_564', 'designation': 'designation_564'},
        {'name': 'name_565', 'email': 'byebyemail.com', 'department': 'department_565', 'designation': 'designation_565'},
        {'name': 'name_566', 'email': 'byespm.com', 'department': 'department_566', 'designation': 'designation_566'},
        {'name': 'name_567', 'email': 'byom.de', 'department': 'department_567', 'designation': 'designation_567'},
        {'name': 'name_568', 'email': 'c01.kr', 'department': 'department_568', 'designation': 'designation_568'},
        {'name': 'name_569', 'email': 'c51vsgq.com', 'department': 'department_569', 'designation': 'designation_569'},
        {'name': 'name_570', 'email': 'cachedot.net', 'department': 'department_570', 'designation': 'designation_570'},
        {'name': 'name_571', 'email': 'californiafitnessdeals.com', 'department': 'department_571', 'designation': 'designation_571'},
        {'name': 'name_572', 'email': 'cam4you.cc', 'department': 'department_572', 'designation': 'designation_572'},
        {'name': 'name_573', 'email': 'camping-grill.info', 'department': 'department_573', 'designation': 'designation_573'},
        {'name': 'name_574', 'email': 'candymail.de', 'department': 'department_574', 'designation': 'designation_574'},
        {'name': 'name_575', 'email': 'cane.pw', 'department': 'department_575', 'designation': 'designation_575'},
        {'name': 'name_576', 'email': 'capitalistdilemma.com', 'department': 'department_576', 'designation': 'designation_576'},
        {'name': 'name_577', 'email': 'car101.pro', 'department': 'department_577', 'designation': 'designation_577'},
        {'name': 'name_578', 'email': 'carbtc.net', 'department': 'department_578', 'designation': 'designation_578'},
        {'name': 'name_579', 'email': 'cars2.club', 'department': 'department_579', 'designation': 'designation_579'},
        {'name': 'name_580', 'email': 'carsencyclopedia.com', 'department': 'department_580', 'designation': 'designation_580'},
        {'name': 'name_581', 'email': 'cartelera.org', 'department': 'department_581', 'designation': 'designation_581'},
        {'name': 'name_582', 'email': 'caseedu.tk', 'department': 'department_582', 'designation': 'designation_582'},
        {'name': 'name_583', 'email': 'cashflow35.com', 'department': 'department_583', 'designation': 'designation_583'},
        {'name': 'name_584', 'email': 'casualdx.com', 'department': 'department_584', 'designation': 'designation_584'},
        {'name': 'name_585', 'email': 'catgroup.uk', 'department': 'department_585', 'designation': 'designation_585'},
        {'name': 'name_586', 'email': 'cavi.mx', 'department': 'department_586', 'designation': 'designation_586'},
        {'name': 'name_587', 'email': 'cbair.com', 'department': 'department_587', 'designation': 'designation_587'},
        {'name': 'name_588', 'email': 'cbes.net', 'department': 'department_588', 'designation': 'designation_588'},
        {'name': 'name_589', 'email': 'cbty.ru', 'department': 'department_589', 'designation': 'designation_589'},
        {'name': 'name_590', 'email': 'cbty.store', 'department': 'department_590', 'designation': 'designation_590'},
        {'name': 'name_591', 'email': 'cc.liamria', 'department': 'department_591', 'designation': 'designation_591'},
        {'name': 'name_592', 'email': 'ccmail.uk', 'department': 'department_592', 'designation': 'designation_592'},
        {'name': 'name_593', 'email': 'cdfaq.com', 'department': 'department_593', 'designation': 'designation_593'},
        {'name': 'name_594', 'email': 'cdpa.cc', 'department': 'department_594', 'designation': 'designation_594'},
        {'name': 'name_595', 'email': 'ceed.se', 'department': 'department_595', 'designation': 'designation_595'},
        {'name': 'name_596', 'email': 'cek.pm', 'department': 'department_596', 'designation': 'designation_596'},
        {'name': 'name_597', 'email': 'cellurl.com', 'department': 'department_597', 'designation': 'designation_597'},
        {'name': 'name_598', 'email': 'centermail.com', 'department': 'department_598', 'designation': 'designation_598'},
        {'name': 'name_599', 'email': 'centermail.net', 'department': 'department_599', 'designation': 'designation_599'},
        {'name': 'name_600', 'email': 'cetpass.com', 'department': 'department_600', 'designation': 'designation_600'},
        {'name': 'name_601', 'email': 'cfo2go.ro', 'department': 'department_601', 'designation': 'designation_601'},
        {'name': 'name_602', 'email': 'chacuo.net', 'department': 'department_602', 'designation': 'designation_602'},
        {'name': 'name_603', 'email': 'chaichuang.com', 'department': 'department_603', 'designation': 'designation_603'},
        {'name': 'name_604', 'email': 'chalupaurybnicku.cz', 'department': 'department_604', 'designation': 'designation_604'},
        {'name': 'name_605', 'email': 'chammy.info', 'department': 'department_605', 'designation': 'designation_605'},
        {'name': 'name_606', 'email': 'chapsmail.com', 'department': 'department_606', 'designation': 'designation_606'},
        {'name': 'name_607', 'email': 'chasefreedomactivate.com', 'department': 'department_607', 'designation': 'designation_607'},
        {'name': 'name_608', 'email': 'chatich.com', 'department': 'department_608', 'designation': 'designation_608'},
        {'name': 'name_609', 'email': 'cheaphub.net', 'department': 'department_609', 'designation': 'designation_609'},
        {'name': 'name_610', 'email': 'cheatmail.de', 'department': 'department_610', 'designation': 'designation_610'},
        {'name': 'name_611', 'email': 'chenbot.email', 'department': 'department_611', 'designation': 'designation_611'},
        {'name': 'name_612', 'email': 'chewydonut.com', 'department': 'department_612', 'designation': 'designation_612'},
        {'name': 'name_613', 'email': 'chibakenma.ml', 'department': 'department_613', 'designation': 'designation_613'},
        {'name': 'name_614', 'email': 'chickenkiller.com', 'department': 'department_614', 'designation': 'designation_614'},
        {'name': 'name_615', 'email': 'chielo.com', 'department': 'department_615', 'designation': 'designation_615'},
        {'name': 'name_616', 'email': 'childsavetrust.org', 'department': 'department_616', 'designation': 'designation_616'},
        {'name': 'name_617', 'email': 'chilkat.com', 'department': 'department_617', 'designation': 'designation_617'},
        {'name': 'name_618', 'email': 'chinamkm.com', 'department': 'department_618', 'designation': 'designation_618'},
        {'name': 'name_619', 'email': 'chithinh.com', 'department': 'department_619', 'designation': 'designation_619'},
        {'name': 'name_620', 'email': 'chitthi.in', 'department': 'department_620', 'designation': 'designation_620'},
        {'name': 'name_621', 'email': 'choco.la', 'department': 'department_621', 'designation': 'designation_621'},
        {'name': 'name_622', 'email': 'chogmail.com', 'department': 'department_622', 'designation': 'designation_622'},
        {'name': 'name_623', 'email': 'choicemail1.com', 'department': 'department_623', 'designation': 'designation_623'},
        {'name': 'name_624', 'email': 'chong-mail.com', 'department': 'department_624', 'designation': 'designation_624'},
        {'name': 'name_625', 'email': 'chong-mail.net', 'department': 'department_625', 'designation': 'designation_625'},
        {'name': 'name_626', 'email': 'chong-mail.org', 'department': 'department_626', 'designation': 'designation_626'},
        {'name': 'name_627', 'email': 'chumpstakingdumps.com', 'department': 'department_627', 'designation': 'designation_627'},
        {'name': 'name_628', 'email': 'cigar-auctions.com', 'department': 'department_628', 'designation': 'designation_628'},
        {'name': 'name_629', 'email': 'civikli.com', 'department': 'department_629', 'designation': 'designation_629'},
        {'name': 'name_630', 'email': 'civx.org', 'department': 'department_630', 'designation': 'designation_630'},
        {'name': 'name_631', 'email': 'ckaazaza.tk', 'department': 'department_631', 'designation': 'designation_631'},
        {'name': 'name_632', 'email': 'ckiso.com', 'department': 'department_632', 'designation': 'designation_632'},
        {'name': 'name_633', 'email': 'cl-cl.org', 'department': 'department_633', 'designation': 'designation_633'},
        {'name': 'name_634', 'email': 'cl0ne.net', 'department': 'department_634', 'designation': 'designation_634'},
        {'name': 'name_635', 'email': 'claimab.com', 'department': 'department_635', 'designation': 'designation_635'},
        {'name': 'name_636', 'email': 'clandest.in', 'department': 'department_636', 'designation': 'designation_636'},
        {'name': 'name_637', 'email': 'classesmail.com', 'department': 'department_637', 'designation': 'designation_637'},
        {'name': 'name_638', 'email': 'clearwatermail.info', 'department': 'department_638', 'designation': 'designation_638'},
        {'name': 'name_639', 'email': 'click-email.com', 'department': 'department_639', 'designation': 'designation_639'},
        {'name': 'name_640', 'email': 'clickdeal.co', 'department': 'department_640', 'designation': 'designation_640'},
        {'name': 'name_641', 'email': 'clipmail.eu', 'department': 'department_641', 'designation': 'designation_641'},
        {'name': 'name_642', 'email': 'clixser.com', 'department': 'department_642', 'designation': 'designation_642'},
        {'name': 'name_643', 'email': 'clonemoi.tk', 'department': 'department_643', 'designation': 'designation_643'},
        {'name': 'name_644', 'email': 'cloud-mail.top', 'department': 'department_644', 'designation': 'designation_644'},
        {'name': 'name_645', 'email': 'clout.wiki', 'department': 'department_645', 'designation': 'designation_645'},
        {'name': 'name_646', 'email': 'clowmail.com', 'department': 'department_646', 'designation': 'designation_646'},
        {'name': 'name_647', 'email': 'clrmail.com', 'department': 'department_647', 'designation': 'designation_647'},
        {'name': 'name_648', 'email': 'cmail.club', 'department': 'department_648', 'designation': 'designation_648'},
        {'name': 'name_649', 'email': 'cmail.com', 'department': 'department_649', 'designation': 'designation_649'},
        {'name': 'name_650', 'email': 'cmail.net', 'department': 'department_650', 'designation': 'designation_650'},
        {'name': 'name_651', 'email': 'cmail.org', 'department': 'department_651', 'designation': 'designation_651'},
        {'name': 'name_652', 'email': 'cnamed.com', 'department': 'department_652', 'designation': 'designation_652'},
        {'name': 'name_653', 'email': 'cndps.com', 'department': 'department_653', 'designation': 'designation_653'},
        {'name': 'name_654', 'email': 'cnew.ir', 'department': 'department_654', 'designation': 'designation_654'},
        {'name': 'name_655', 'email': 'cnmsg.net', 'department': 'department_655', 'designation': 'designation_655'},
        {'name': 'name_656', 'email': 'cnsds.de', 'department': 'department_656', 'designation': 'designation_656'},
        {'name': 'name_657', 'email': 'co.cc', 'department': 'department_657', 'designation': 'designation_657'},
        {'name': 'name_658', 'email': 'cobarekyo1.ml', 'department': 'department_658', 'designation': 'designation_658'},
        {'name': 'name_659', 'email': 'cocoro.uk', 'department': 'department_659', 'designation': 'designation_659'},
        {'name': 'name_660', 'email': 'cocovpn.com', 'department': 'department_660', 'designation': 'designation_660'},
        {'name': 'name_661', 'email': 'codeandscotch.com', 'department': 'department_661', 'designation': 'designation_661'},
        {'name': 'name_662', 'email': 'codivide.com', 'department': 'department_662', 'designation': 'designation_662'},
        {'name': 'name_663', 'email': 'coffeetimer24.com', 'department': 'department_663', 'designation': 'designation_663'},
        {'name': 'name_664', 'email': 'coieo.com', 'department': 'department_664', 'designation': 'designation_664'},
        {'name': 'name_665', 'email': 'coin-host.net', 'department': 'department_665', 'designation': 'designation_665'},
        {'name': 'name_666', 'email': 'coinlink.club', 'department': 'department_666', 'designation': 'designation_666'},
        {'name': 'name_667', 'email': 'coldemail.info', 'department': 'department_667', 'designation': 'designation_667'},
        {'name': 'name_668', 'email': 'compareshippingrates.org', 'department': 'department_668', 'designation': 'designation_668'},
        {'name': 'name_669', 'email': 'completegolfswing.com', 'department': 'department_669', 'designation': 'designation_669'},
        {'name': 'name_670', 'email': 'comwest.de', 'department': 'department_670', 'designation': 'designation_670'},
        {'name': 'name_671', 'email': 'conf.work', 'department': 'department_671', 'designation': 'designation_671'},
        {'name': 'name_672', 'email': 'consumerriot.com', 'department': 'department_672', 'designation': 'designation_672'},
        {'name': 'name_673', 'email': 'contbay.com', 'department': 'department_673', 'designation': 'designation_673'},
        {'name': 'name_674', 'email': 'cooh-2.site', 'department': 'department_674', 'designation': 'designation_674'},
        {'name': 'name_675', 'email': 'coolandwacky.us', 'department': 'department_675', 'designation': 'designation_675'},
        {'name': 'name_676', 'email': 'coolimpool.org', 'department': 'department_676', 'designation': 'designation_676'},
        {'name': 'name_677', 'email': 'copyhome.win', 'department': 'department_677', 'designation': 'designation_677'},
        {'name': 'name_678', 'email': 'coreclip.com', 'department': 'department_678', 'designation': 'designation_678'},
        {'name': 'name_679', 'email': 'cosmorph.com', 'department': 'department_679', 'designation': 'designation_679'},
        {'name': 'name_680', 'email': 'courrieltemporaire.com', 'department': 'department_680', 'designation': 'designation_680'},
        {'name': 'name_681', 'email': 'coza.ro', 'department': 'department_681', 'designation': 'designation_681'},
        {'name': 'name_682', 'email': 'crankhole.com', 'department': 'department_682', 'designation': 'designation_682'},
        {'name': 'name_683', 'email': 'crapmail.org', 'department': 'department_683', 'designation': 'designation_683'},
        {'name': 'name_684', 'email': 'crastination.de', 'department': 'department_684', 'designation': 'designation_684'},
        {'name': 'name_685', 'email': 'crazespaces.pw', 'department': 'department_685', 'designation': 'designation_685'},
        {'name': 'name_686', 'email': 'crazymailing.com', 'department': 'department_686', 'designation': 'designation_686'},
        {'name': 'name_687', 'email': 'cream.pink', 'department': 'department_687', 'designation': 'designation_687'},
        {'name': 'name_688', 'email': 'crepeau12.com', 'department': 'department_688', 'designation': 'designation_688'},
        {'name': 'name_689', 'email': 'cringemonster.com', 'department': 'department_689', 'designation': 'designation_689'},
        {'name': 'name_690', 'email': 'cross-law.ga', 'department': 'department_690', 'designation': 'designation_690'},
        {'name': 'name_691', 'email': 'cross-law.gq', 'department': 'department_691', 'designation': 'designation_691'},
        {'name': 'name_692', 'email': 'crossmailjet.com', 'department': 'department_692', 'designation': 'designation_692'},
        {'name': 'name_693', 'email': 'crossroadsmail.com', 'department': 'department_693', 'designation': 'designation_693'},
        {'name': 'name_694', 'email': 'crunchcompass.com', 'department': 'department_694', 'designation': 'designation_694'},
        {'name': 'name_695', 'email': 'crusthost.com', 'department': 'department_695', 'designation': 'designation_695'},
        {'name': 'name_696', 'email': 'cs.email', 'department': 'department_696', 'designation': 'designation_696'},
        {'name': 'name_697', 'email': 'csh.ro', 'department': 'department_697', 'designation': 'designation_697'},
        {'name': 'name_698', 'email': 'cszbl.com', 'department': 'department_698', 'designation': 'designation_698'},
        {'name': 'name_699', 'email': 'ctmailing.us', 'department': 'department_699', 'designation': 'designation_699'},
        {'name': 'name_700', 'email': 'ctos.ch', 'department': 'department_700', 'designation': 'designation_700'},
        {'name': 'name_701', 'email': 'cu.cc', 'department': 'department_701', 'designation': 'designation_701'},
        {'name': 'name_702', 'email': 'cubene.com', 'department': 'department_702', 'designation': 'designation_702'},
        {'name': 'name_703', 'email': 'cubiclink.com', 'department': 'department_703', 'designation': 'designation_703'},
        {'name': 'name_704', 'email': 'cuendita.com', 'department': 'department_704', 'designation': 'designation_704'},
        {'name': 'name_705', 'email': 'cuirushi.org', 'department': 'department_705', 'designation': 'designation_705'},
        {'name': 'name_706', 'email': 'cuoly.com', 'department': 'department_706', 'designation': 'designation_706'},
        {'name': 'name_707', 'email': 'cupbest.com', 'department': 'department_707', 'designation': 'designation_707'},
        {'name': 'name_708', 'email': 'curlhph.tk', 'department': 'department_708', 'designation': 'designation_708'},
        {'name': 'name_709', 'email': 'currentmail.com', 'department': 'department_709', 'designation': 'designation_709'},
        {'name': 'name_710', 'email': 'curryworld.de', 'department': 'department_710', 'designation': 'designation_710'},
        {'name': 'name_711', 'email': 'cust.in', 'department': 'department_711', 'designation': 'designation_711'},
        {'name': 'name_712', 'email': 'cutout.club', 'department': 'department_712', 'designation': 'designation_712'},
        {'name': 'name_713', 'email': 'cutradition.com', 'department': 'department_713', 'designation': 'designation_713'},
        {'name': 'name_714', 'email': 'cuvox.de', 'department': 'department_714', 'designation': 'designation_714'},
        {'name': 'name_715', 'email': 'cyber-innovation.club', 'department': 'department_715', 'designation': 'designation_715'},
        {'name': 'name_716', 'email': 'cyber-phone.eu', 'department': 'department_716', 'designation': 'designation_716'},
        {'name': 'name_717', 'email': 'cylab.org', 'department': 'department_717', 'designation': 'designation_717'},
        {'name': 'name_718', 'email': 'd1yun.com', 'department': 'department_718', 'designation': 'designation_718'},
        {'name': 'name_719', 'email': 'd3p.dk', 'department': 'department_719', 'designation': 'designation_719'},
        {'name': 'name_720', 'email': 'daabox.com', 'department': 'department_720', 'designation': 'designation_720'},
        {'name': 'name_721', 'email': 'dab.ro', 'department': 'department_721', 'designation': 'designation_721'},
        {'name': 'name_722', 'email': 'dacoolest.com', 'department': 'department_722', 'designation': 'designation_722'},
        {'name': 'name_723', 'email': 'daemsteam.com', 'department': 'department_723', 'designation': 'designation_723'},
        {'name': 'name_724', 'email': 'daibond.info', 'department': 'department_724', 'designation': 'designation_724'},
        {'name': 'name_725', 'email': 'daily-email.com', 'department': 'department_725', 'designation': 'designation_725'},
        {'name': 'name_726', 'email': 'daintly.com', 'department': 'department_726', 'designation': 'designation_726'},
        {'name': 'name_727', 'email': 'damai.webcam', 'department': 'department_727', 'designation': 'designation_727'},
        {'name': 'name_728', 'email': 'dammexe.net', 'department': 'department_728', 'designation': 'designation_728'},
        {'name': 'name_729', 'email': 'damnthespam.com', 'department': 'department_729', 'designation': 'designation_729'},
        {'name': 'name_730', 'email': 'dandikmail.com', 'department': 'department_730', 'designation': 'designation_730'},
        {'name': 'name_731', 'email': 'darkharvestfilms.com', 'department': 'department_731', 'designation': 'designation_731'},
        {'name': 'name_732', 'email': 'daryxfox.net', 'department': 'department_732', 'designation': 'designation_732'},
        {'name': 'name_733', 'email': 'dasdasdascyka.tk', 'department': 'department_733', 'designation': 'designation_733'},
        {'name': 'name_734', 'email': 'dash-pads.com', 'department': 'department_734', 'designation': 'designation_734'},
        {'name': 'name_735', 'email': 'dataarca.com', 'department': 'department_735', 'designation': 'designation_735'},
        {'name': 'name_736', 'email': 'datarca.com', 'department': 'department_736', 'designation': 'designation_736'},
        {'name': 'name_737', 'email': 'datazo.ca', 'department': 'department_737', 'designation': 'designation_737'},
        {'name': 'name_738', 'email': 'datenschutz.ru', 'department': 'department_738', 'designation': 'designation_738'},
        {'name': 'name_739', 'email': 'datum2.com', 'department': 'department_739', 'designation': 'designation_739'},
        {'name': 'name_740', 'email': 'davidkoh.net', 'department': 'department_740', 'designation': 'designation_740'},
        {'name': 'name_741', 'email': 'davidlcreative.com', 'department': 'department_741', 'designation': 'designation_741'},
        {'name': 'name_742', 'email': 'dawin.com', 'department': 'department_742', 'designation': 'designation_742'},
        {'name': 'name_743', 'email': 'daymail.life', 'department': 'department_743', 'designation': 'designation_743'},
        {'name': 'name_744', 'email': 'daymailonline.com', 'department': 'department_744', 'designation': 'designation_744'},
        {'name': 'name_745', 'email': 'dayrep.com', 'department': 'department_745', 'designation': 'designation_745'},
        {'name': 'name_746', 'email': 'dbunker.com', 'department': 'department_746', 'designation': 'designation_746'},
        {'name': 'name_747', 'email': 'dcctb.com', 'department': 'department_747', 'designation': 'designation_747'},
        {'name': 'name_748', 'email': 'dcemail.com', 'department': 'department_748', 'designation': 'designation_748'},
        {'name': 'name_749', 'email': 'ddcrew.com', 'department': 'department_749', 'designation': 'designation_749'},
        {'name': 'name_750', 'email': 'de-a.org', 'department': 'department_750', 'designation': 'designation_750'},
        {'name': 'name_751', 'email': 'dea-21olympic.com', 'department': 'department_751', 'designation': 'designation_751'},
        {'name': 'name_752', 'email': 'deadaddress.com', 'department': 'department_752', 'designation': 'designation_752'},
        {'name': 'name_753', 'email': 'deadchildren.org', 'department': 'department_753', 'designation': 'designation_753'},
        {'name': 'name_754', 'email': 'deadfake.cf', 'department': 'department_754', 'designation': 'designation_754'},
        {'name': 'name_755', 'email': 'deadfake.ga', 'department': 'department_755', 'designation': 'designation_755'},
        {'name': 'name_756', 'email': 'deadfake.ml', 'department': 'department_756', 'designation': 'designation_756'},
        {'name': 'name_757', 'email': 'deadfake.tk', 'department': 'department_757', 'designation': 'designation_757'},
        {'name': 'name_758', 'email': 'deadspam.com', 'department': 'department_758', 'designation': 'designation_758'},
        {'name': 'name_759', 'email': 'deagot.com', 'department': 'department_759', 'designation': 'designation_759'},
        {'name': 'name_760', 'email': 'dealja.com', 'department': 'department_760', 'designation': 'designation_760'},
        {'name': 'name_761', 'email': 'dealrek.com', 'department': 'department_761', 'designation': 'designation_761'},
        {'name': 'name_762', 'email': 'deekayen.us', 'department': 'department_762', 'designation': 'designation_762'},
        {'name': 'name_763', 'email': 'defomail.com', 'department': 'department_763', 'designation': 'designation_763'},
        {'name': 'name_764', 'email': 'degradedfun.net', 'department': 'department_764', 'designation': 'designation_764'},
        {'name': 'name_765', 'email': 'deinbox.com', 'department': 'department_765', 'designation': 'designation_765'},
        {'name': 'name_766', 'email': 'delayload.com', 'department': 'department_766', 'designation': 'designation_766'},
        {'name': 'name_767', 'email': 'delayload.net', 'department': 'department_767', 'designation': 'designation_767'},
        {'name': 'name_768', 'email': 'delikkt.de', 'department': 'department_768', 'designation': 'designation_768'},
        {'name': 'name_769', 'email': 'delivrmail.com', 'department': 'department_769', 'designation': 'designation_769'},
        {'name': 'name_770', 'email': 'demen.ml', 'department': 'department_770', 'designation': 'designation_770'},
        {'name': 'name_771', 'email': 'dengekibunko.ga', 'department': 'department_771', 'designation': 'designation_771'},
        {'name': 'name_772', 'email': 'dengekibunko.gq', 'department': 'department_772', 'designation': 'designation_772'},
        {'name': 'name_773', 'email': 'dengekibunko.ml', 'department': 'department_773', 'designation': 'designation_773'},
        {'name': 'name_774', 'email': 'der-kombi.de', 'department': 'department_774', 'designation': 'designation_774'},
        {'name': 'name_775', 'email': 'derkombi.de', 'department': 'department_775', 'designation': 'designation_775'},
        {'name': 'name_776', 'email': 'derluxuswagen.de', 'department': 'department_776', 'designation': 'designation_776'},
        {'name': 'name_777', 'email': 'desoz.com', 'department': 'department_777', 'designation': 'designation_777'},
        {'name': 'name_778', 'email': 'despam.it', 'department': 'department_778', 'designation': 'designation_778'},
        {'name': 'name_779', 'email': 'despammed.com', 'department': 'department_779', 'designation': 'designation_779'},
        {'name': 'name_780', 'email': 'dev-null.cf', 'department': 'department_780', 'designation': 'designation_780'},
        {'name': 'name_781', 'email': 'dev-null.ga', 'department': 'department_781', 'designation': 'designation_781'},
        {'name': 'name_782', 'email': 'dev-null.gq', 'department': 'department_782', 'designation': 'designation_782'},
        {'name': 'name_783', 'email': 'dev-null.ml', 'department': 'department_783', 'designation': 'designation_783'},
        {'name': 'name_784', 'email': 'developermail.com', 'department': 'department_784', 'designation': 'designation_784'},
        {'name': 'name_785', 'email': 'devnullmail.com', 'department': 'department_785', 'designation': 'designation_785'},
        {'name': 'name_786', 'email': 'deyom.com', 'department': 'department_786', 'designation': 'designation_786'},
        {'name': 'name_787', 'email': 'dharmatel.net', 'department': 'department_787', 'designation': 'designation_787'},
        {'name': 'name_788', 'email': 'dhm.ro', 'department': 'department_788', 'designation': 'designation_788'},
        {'name': 'name_789', 'email': 'dhy.cc', 'department': 'department_789', 'designation': 'designation_789'},
        {'name': 'name_790', 'email': 'dialogus.com', 'department': 'department_790', 'designation': 'designation_790'},
        {'name': 'name_791', 'email': 'diapaulpainting.com', 'department': 'department_791', 'designation': 'designation_791'},
        {'name': 'name_792', 'email': 'dicopto.com', 'department': 'department_792', 'designation': 'designation_792'},
        {'name': 'name_793', 'email': 'digdig.org', 'department': 'department_793', 'designation': 'designation_793'},
        {'name': 'name_794', 'email': 'digital-message.com', 'department': 'department_794', 'designation': 'designation_794'},
        {'name': 'name_795', 'email': 'digitalesbusiness.info', 'department': 'department_795', 'designation': 'designation_795'},
        {'name': 'name_796', 'email': 'digitalmail.info', 'department': 'department_796', 'designation': 'designation_796'},
        {'name': 'name_797', 'email': 'digitalmariachis.com', 'department': 'department_797', 'designation': 'designation_797'},
        {'name': 'name_798', 'email': 'digitalsanctuary.com', 'department': 'department_798', 'designation': 'designation_798'},
        {'name': 'name_799', 'email': 'dildosfromspace.com', 'department': 'department_799', 'designation': 'designation_799'},
        {'name': 'name_800', 'email': 'dim-coin.com', 'department': 'department_800', 'designation': 'designation_800'},
        {'name': 'name_801', 'email': 'dingbone.com', 'department': 'department_801', 'designation': 'designation_801'},
        {'name': 'name_802', 'email': 'diolang.com', 'department': 'department_802', 'designation': 'designation_802'},
        {'name': 'name_803', 'email': 'directmail24.net', 'department': 'department_803', 'designation': 'designation_803'},
        {'name': 'name_804', 'email': 'disaq.com', 'department': 'department_804', 'designation': 'designation_804'},
        {'name': 'name_805', 'email': 'disbox.net', 'department': 'department_805', 'designation': 'designation_805'},
        {'name': 'name_806', 'email': 'disbox.org', 'department': 'department_806', 'designation': 'designation_806'},
        {'name': 'name_807', 'email': 'discard.cf', 'department': 'department_807', 'designation': 'designation_807'},
        {'name': 'name_808', 'email': 'discard.email', 'department': 'department_808', 'designation': 'designation_808'},
        {'name': 'name_809', 'email': 'discard.ga', 'department': 'department_809', 'designation': 'designation_809'},
        {'name': 'name_810', 'email': 'discard.gq', 'department': 'department_810', 'designation': 'designation_810'},
        {'name': 'name_811', 'email': 'discard.ml', 'department': 'department_811', 'designation': 'designation_811'},
        {'name': 'name_812', 'email': 'discard.tk', 'department': 'department_812', 'designation': 'designation_812'},
        {'name': 'name_813', 'email': 'discardmail.com', 'department': 'department_813', 'designation': 'designation_813'},
        {'name': 'name_814', 'email': 'discardmail.de', 'department': 'department_814', 'designation': 'designation_814'},
        {'name': 'name_815', 'email': 'discos4.com', 'department': 'department_815', 'designation': 'designation_815'},
        {'name': 'name_816', 'email': 'dishcatfish.com', 'department': 'department_816', 'designation': 'designation_816'},
        {'name': 'name_817', 'email': 'disign-concept.eu', 'department': 'department_817', 'designation': 'designation_817'},
        {'name': 'name_818', 'email': 'disign-revelation.com', 'department': 'department_818', 'designation': 'designation_818'},
        {'name': 'name_819', 'email': 'dispo.in', 'department': 'department_819', 'designation': 'designation_819'},
        {'name': 'name_820', 'email': 'dispomail.eu', 'department': 'department_820', 'designation': 'designation_820'},
        {'name': 'name_821', 'email': 'disposable-e.ml', 'department': 'department_821', 'designation': 'designation_821'},
        {'name': 'name_822', 'email': 'disposable-email.ml', 'department': 'department_822', 'designation': 'designation_822'},
        {'name': 'name_823', 'email': 'disposable.cf', 'department': 'department_823', 'designation': 'designation_823'},
        {'name': 'name_824', 'email': 'disposable.ga', 'department': 'department_824', 'designation': 'designation_824'},
        {'name': 'name_825', 'email': 'disposable.ml', 'department': 'department_825', 'designation': 'designation_825'},
        {'name': 'name_826', 'email': 'disposable.site', 'department': 'department_826', 'designation': 'designation_826'},
        {'name': 'name_827', 'email': 'disposableaddress.com', 'department': 'department_827', 'designation': 'designation_827'},
        {'name': 'name_828', 'email': 'disposableemailaddresses.com', 'department': 'department_828', 'designation': 'designation_828'},
        {'name': 'name_829', 'email': 'disposableinbox.com', 'department': 'department_829', 'designation': 'designation_829'},
        {'name': 'name_830', 'email': 'disposablemails.com', 'department': 'department_830', 'designation': 'designation_830'},
        {'name': 'name_831', 'email': 'dispose.it', 'department': 'department_831', 'designation': 'designation_831'},
        {'name': 'name_832', 'email': 'disposeamail.com', 'department': 'department_832', 'designation': 'designation_832'},
        {'name': 'name_833', 'email': 'disposemail.com', 'department': 'department_833', 'designation': 'designation_833'},
        {'name': 'name_834', 'email': 'disposemymail.com', 'department': 'department_834', 'designation': 'designation_834'},
        {'name': 'name_835', 'email': 'dispostable.com', 'department': 'department_835', 'designation': 'designation_835'},
        {'name': 'name_836', 'email': 'divad.ga', 'department': 'department_836', 'designation': 'designation_836'},
        {'name': 'name_837', 'email': 'divermail.com', 'department': 'department_837', 'designation': 'designation_837'},
        {'name': 'name_838', 'email': 'divismail.ru', 'department': 'department_838', 'designation': 'designation_838'},
        {'name': 'name_839', 'email': 'diwaq.com', 'department': 'department_839', 'designation': 'designation_839'},
        {'name': 'name_840', 'email': 'dlemail.ru', 'department': 'department_840', 'designation': 'designation_840'},
        {'name': 'name_841', 'email': 'dmarc.ro', 'department': 'department_841', 'designation': 'designation_841'},
        {'name': 'name_842', 'email': 'dndent.com', 'department': 'department_842', 'designation': 'designation_842'},
        {'name': 'name_843', 'email': 'dnses.ro', 'department': 'department_843', 'designation': 'designation_843'},
        {'name': 'name_844', 'email': 'doanart.com', 'department': 'department_844', 'designation': 'designation_844'},
        {'name': 'name_845', 'email': 'dob.jp', 'department': 'department_845', 'designation': 'designation_845'},
        {'name': 'name_846', 'email': 'dodgeit.com', 'department': 'department_846', 'designation': 'designation_846'},
        {'name': 'name_847', 'email': 'dodgemail.de', 'department': 'department_847', 'designation': 'designation_847'},
        {'name': 'name_848', 'email': 'dodgit.com', 'department': 'department_848', 'designation': 'designation_848'},
        {'name': 'name_849', 'email': 'dodgit.org', 'department': 'department_849', 'designation': 'designation_849'},
        {'name': 'name_850', 'email': 'dodsi.com', 'department': 'department_850', 'designation': 'designation_850'},
        {'name': 'name_851', 'email': 'doiea.com', 'department': 'department_851', 'designation': 'designation_851'},
        {'name': 'name_852', 'email': 'dolphinnet.net', 'department': 'department_852', 'designation': 'designation_852'},
        {'name': 'name_853', 'email': 'domforfb1.tk', 'department': 'department_853', 'designation': 'designation_853'},
        {'name': 'name_854', 'email': 'domforfb18.tk', 'department': 'department_854', 'designation': 'designation_854'},
        {'name': 'name_855', 'email': 'domforfb19.tk', 'department': 'department_855', 'designation': 'designation_855'},
        {'name': 'name_856', 'email': 'domforfb2.tk', 'department': 'department_856', 'designation': 'designation_856'},
        {'name': 'name_857', 'email': 'domforfb23.tk', 'department': 'department_857', 'designation': 'designation_857'},
        {'name': 'name_858', 'email': 'domforfb27.tk', 'department': 'department_858', 'designation': 'designation_858'},
        {'name': 'name_859', 'email': 'domforfb29.tk', 'department': 'department_859', 'designation': 'designation_859'},
        {'name': 'name_860', 'email': 'domforfb3.tk', 'department': 'department_860', 'designation': 'designation_860'},
        {'name': 'name_861', 'email': 'domforfb4.tk', 'department': 'department_861', 'designation': 'designation_861'},
        {'name': 'name_862', 'email': 'domforfb5.tk', 'department': 'department_862', 'designation': 'designation_862'},
        {'name': 'name_863', 'email': 'domforfb6.tk', 'department': 'department_863', 'designation': 'designation_863'},
        {'name': 'name_864', 'email': 'domforfb7.tk', 'department': 'department_864', 'designation': 'designation_864'},
        {'name': 'name_865', 'email': 'domforfb8.tk', 'department': 'department_865', 'designation': 'designation_865'},
        {'name': 'name_866', 'email': 'domforfb9.tk', 'department': 'department_866', 'designation': 'designation_866'},
        {'name': 'name_867', 'email': 'domozmail.com', 'department': 'department_867', 'designation': 'designation_867'},
        {'name': 'name_868', 'email': 'donebyngle.com', 'department': 'department_868', 'designation': 'designation_868'},
        {'name': 'name_869', 'email': 'donemail.ru', 'department': 'department_869', 'designation': 'designation_869'},
        {'name': 'name_870', 'email': 'dongqing365.com', 'department': 'department_870', 'designation': 'designation_870'},
        {'name': 'name_871', 'email': 'dontreg.com', 'department': 'department_871', 'designation': 'designation_871'},
        {'name': 'name_872', 'email': 'dontsendmespam.de', 'department': 'department_872', 'designation': 'designation_872'},
        {'name': 'name_873', 'email': 'doojazz.com', 'department': 'department_873', 'designation': 'designation_873'},
        {'name': 'name_874', 'email': 'doquier.tk', 'department': 'department_874', 'designation': 'designation_874'},
        {'name': 'name_875', 'email': 'dotman.de', 'department': 'department_875', 'designation': 'designation_875'},
        {'name': 'name_876', 'email': 'dotmsg.com', 'department': 'department_876', 'designation': 'designation_876'},
        {'name': 'name_877', 'email': 'dotslashrage.com', 'department': 'department_877', 'designation': 'designation_877'},
        {'name': 'name_878', 'email': 'doublemail.de', 'department': 'department_878', 'designation': 'designation_878'},
        {'name': 'name_879', 'email': 'douchelounge.com', 'department': 'department_879', 'designation': 'designation_879'},
        {'name': 'name_880', 'email': 'dozvon-spb.ru', 'department': 'department_880', 'designation': 'designation_880'},
        {'name': 'name_881', 'email': 'dp76.com', 'department': 'department_881', 'designation': 'designation_881'},
        {'name': 'name_882', 'email': 'dpptd.com', 'department': 'department_882', 'designation': 'designation_882'},
        {'name': 'name_883', 'email': 'dr69.site', 'department': 'department_883', 'designation': 'designation_883'},
        {'name': 'name_884', 'email': 'drdrb.com', 'department': 'department_884', 'designation': 'designation_884'},
        {'name': 'name_885', 'email': 'drdrb.net', 'department': 'department_885', 'designation': 'designation_885'},
        {'name': 'name_886', 'email': 'dred.ru', 'department': 'department_886', 'designation': 'designation_886'},
        {'name': 'name_887', 'email': 'drevo.si', 'department': 'department_887', 'designation': 'designation_887'},
        {'name': 'name_888', 'email': 'drivetagdev.com', 'department': 'department_888', 'designation': 'designation_888'},
        {'name': 'name_889', 'email': 'drmail.in', 'department': 'department_889', 'designation': 'designation_889'},
        {'name': 'name_890', 'email': 'droolingfanboy.de', 'department': 'department_890', 'designation': 'designation_890'},
        {'name': 'name_891', 'email': 'dropcake.de', 'department': 'department_891', 'designation': 'designation_891'},
        {'name': 'name_892', 'email': 'dropjar.com', 'department': 'department_892', 'designation': 'designation_892'},
        {'name': 'name_893', 'email': 'droplar.com', 'department': 'department_893', 'designation': 'designation_893'},
        {'name': 'name_894', 'email': 'dropmail.me', 'department': 'department_894', 'designation': 'designation_894'},
        {'name': 'name_895', 'email': 'dropsin.net', 'department': 'department_895', 'designation': 'designation_895'},
        {'name': 'name_896', 'email': 'drowblock.com', 'department': 'department_896', 'designation': 'designation_896'},
        {'name': 'name_897', 'email': 'dsgvo.party', 'department': 'department_897', 'designation': 'designation_897'},
        {'name': 'name_898', 'email': 'dsgvo.ru', 'department': 'department_898', 'designation': 'designation_898'},
        {'name': 'name_899', 'email': 'dshfjdafd.cloud', 'department': 'department_899', 'designation': 'designation_899'},
        {'name': 'name_900', 'email': 'dsiay.com', 'department': 'department_900', 'designation': 'designation_900'},
        {'name': 'name_901', 'email': 'dspwebservices.com', 'department': 'department_901', 'designation': 'designation_901'},
        {'name': 'name_902', 'email': 'duam.net', 'department': 'department_902', 'designation': 'designation_902'},
        {'name': 'name_903', 'email': 'duck2.club', 'department': 'department_903', 'designation': 'designation_903'},
        {'name': 'name_904', 'email': 'dudmail.com', 'department': 'department_904', 'designation': 'designation_904'},
        {'name': 'name_905', 'email': 'duk33.com', 'department': 'department_905', 'designation': 'designation_905'},
        {'name': 'name_906', 'email': 'dukedish.com', 'department': 'department_906', 'designation': 'designation_906'},
        {'name': 'name_907', 'email': 'dump-email.info', 'department': 'department_907', 'designation': 'designation_907'},
        {'name': 'name_908', 'email': 'dumpandjunk.com', 'department': 'department_908', 'designation': 'designation_908'},
        {'name': 'name_909', 'email': 'dumpmail.de', 'department': 'department_909', 'designation': 'designation_909'},
        {'name': 'name_910', 'email': 'dumpyemail.com', 'department': 'department_910', 'designation': 'designation_910'},
        {'name': 'name_911', 'email': 'durandinterstellar.com', 'department': 'department_911', 'designation': 'designation_911'},
        {'name': 'name_912', 'email': 'duskmail.com', 'department': 'department_912', 'designation': 'designation_912'},
        {'name': 'name_913', 'email': 'dwse.edu.pl', 'department': 'department_913', 'designation': 'designation_913'},
        {'name': 'name_914', 'email': 'dyceroprojects.com', 'department': 'department_914', 'designation': 'designation_914'},
        {'name': 'name_915', 'email': 'dz17.net', 'department': 'department_915', 'designation': 'designation_915'},
        {'name': 'name_916', 'email': 'e-mail.com', 'department': 'department_916', 'designation': 'designation_916'},
        {'name': 'name_917', 'email': 'e-mail.org', 'department': 'department_917', 'designation': 'designation_917'},
        {'name': 'name_918', 'email': 'e-marketstore.ru', 'department': 'department_918', 'designation': 'designation_918'},
        {'name': 'name_919', 'email': 'e-tomarigi.com', 'department': 'department_919', 'designation': 'designation_919'},
        {'name': 'name_920', 'email': 'e3z.de', 'department': 'department_920', 'designation': 'designation_920'},
        {'name': 'name_921', 'email': 'e4ward.com', 'department': 'department_921', 'designation': 'designation_921'},
        {'name': 'name_922', 'email': 'eanok.com', 'department': 'department_922', 'designation': 'designation_922'},
        {'name': 'name_923', 'email': 'easy-trash-mail.com', 'department': 'department_923', 'designation': 'designation_923'},
        {'name': 'name_924', 'email': 'easynetwork.info', 'department': 'department_924', 'designation': 'designation_924'},
        {'name': 'name_925', 'email': 'easytrashmail.com', 'department': 'department_925', 'designation': 'designation_925'},
        {'name': 'name_926', 'email': 'eatmea2z.club', 'department': 'department_926', 'designation': 'designation_926'},
        {'name': 'name_927', 'email': 'eay.jp', 'department': 'department_927', 'designation': 'designation_927'},
        {'name': 'name_928', 'email': 'ebbob.com', 'department': 'department_928', 'designation': 'designation_928'},
        {'name': 'name_929', 'email': 'ebeschlussbuch.de', 'department': 'department_929', 'designation': 'designation_929'},
        {'name': 'name_930', 'email': 'ecallheandi.com', 'department': 'department_930', 'designation': 'designation_930'},
        {'name': 'name_931', 'email': 'ecolo-online.fr', 'department': 'department_931', 'designation': 'designation_931'},
        {'name': 'name_932', 'email': 'edgex.ru', 'department': 'department_932', 'designation': 'designation_932'},
        {'name': 'name_933', 'email': 'edinburgh-airporthotels.com', 'department': 'department_933', 'designation': 'designation_933'},
        {'name': 'name_934', 'email': 'edupolska.edu.pl', 'department': 'department_934', 'designation': 'designation_934'},
        {'name': 'name_935', 'email': 'edv.to', 'department': 'department_935', 'designation': 'designation_935'},
        {'name': 'name_936', 'email': 'ee1.pl', 'department': 'department_936', 'designation': 'designation_936'},
        {'name': 'name_937', 'email': 'ee2.pl', 'department': 'department_937', 'designation': 'designation_937'},
        {'name': 'name_938', 'email': 'eeedv.de', 'department': 'department_938', 'designation': 'designation_938'},
        {'name': 'name_939', 'email': 'eelmail.com', 'department': 'department_939', 'designation': 'designation_939'},
        {'name': 'name_940', 'email': 'efxs.ca', 'department': 'department_940', 'designation': 'designation_940'},
        {'name': 'name_941', 'email': 'egzones.com', 'department': 'department_941', 'designation': 'designation_941'},
        {'name': 'name_942', 'email': 'einmalmail.de', 'department': 'department_942', 'designation': 'designation_942'},
        {'name': 'name_943', 'email': 'einrot.com', 'department': 'department_943', 'designation': 'designation_943'},
        {'name': 'name_944', 'email': 'einrot.de', 'department': 'department_944', 'designation': 'designation_944'},
        {'name': 'name_945', 'email': 'eintagsmail.de', 'department': 'department_945', 'designation': 'designation_945'},
        {'name': 'name_946', 'email': 'elearningjournal.org', 'department': 'department_946', 'designation': 'designation_946'},
        {'name': 'name_947', 'email': 'electro.mn', 'department': 'department_947', 'designation': 'designation_947'},
        {'name': 'name_948', 'email': 'elitevipatlantamodels.com', 'department': 'department_948', 'designation': 'designation_948'},
        {'name': 'name_949', 'email': 'elki-mkzn.ru', 'department': 'department_949', 'designation': 'designation_949'},
        {'name': 'name_950', 'email': 'email-fake.cf', 'department': 'department_950', 'designation': 'designation_950'},
        {'name': 'name_951', 'email': 'email-fake.com', 'department': 'department_951', 'designation': 'designation_951'},
        {'name': 'name_952', 'email': 'email-fake.ga', 'department': 'department_952', 'designation': 'designation_952'},
        {'name': 'name_953', 'email': 'email-fake.gq', 'department': 'department_953', 'designation': 'designation_953'},
        {'name': 'name_954', 'email': 'email-fake.ml', 'department': 'department_954', 'designation': 'designation_954'},
        {'name': 'name_955', 'email': 'email-fake.tk', 'department': 'department_955', 'designation': 'designation_955'},
        {'name': 'name_956', 'email': 'email-jetable.fr', 'department': 'department_956', 'designation': 'designation_956'},
        {'name': 'name_957', 'email': 'email-lab.com', 'department': 'department_957', 'designation': 'designation_957'},
        {'name': 'name_958', 'email': 'email-temp.com', 'department': 'department_958', 'designation': 'designation_958'},
        {'name': 'name_959', 'email': 'email.edu.pl', 'department': 'department_959', 'designation': 'designation_959'},
        {'name': 'name_960', 'email': 'email.net', 'department': 'department_960', 'designation': 'designation_960'},
        {'name': 'name_961', 'email': 'email1.pro', 'department': 'department_961', 'designation': 'designation_961'},
        {'name': 'name_962', 'email': 'email60.com', 'department': 'department_962', 'designation': 'designation_962'},
        {'name': 'name_963', 'email': 'emailage.cf', 'department': 'department_963', 'designation': 'designation_963'},
        {'name': 'name_964', 'email': 'emailage.ga', 'department': 'department_964', 'designation': 'designation_964'},
        {'name': 'name_965', 'email': 'emailage.gq', 'department': 'department_965', 'designation': 'designation_965'},
        {'name': 'name_966', 'email': 'emailage.ml', 'department': 'department_966', 'designation': 'designation_966'},
        {'name': 'name_967', 'email': 'emailage.tk', 'department': 'department_967', 'designation': 'designation_967'},
        {'name': 'name_968', 'email': 'emailate.com', 'department': 'department_968', 'designation': 'designation_968'},
        {'name': 'name_969', 'email': 'emailbin.net', 'department': 'department_969', 'designation': 'designation_969'},
        {'name': 'name_970', 'email': 'emailcbox.pro', 'department': 'department_970', 'designation': 'designation_970'},
        {'name': 'name_971', 'email': 'emailcu.icu', 'department': 'department_971', 'designation': 'designation_971'},
        {'name': 'name_972', 'email': 'emaildienst.de', 'department': 'department_972', 'designation': 'designation_972'},
        {'name': 'name_973', 'email': 'emaildrop.io', 'department': 'department_973', 'designation': 'designation_973'},
        {'name': 'name_974', 'email': 'emailfake.com', 'department': 'department_974', 'designation': 'designation_974'},
        {'name': 'name_975', 'email': 'emailfake.ml', 'department': 'department_975', 'designation': 'designation_975'},
        {'name': 'name_976', 'email': 'emailfoxi.pro', 'department': 'department_976', 'designation': 'designation_976'},
        {'name': 'name_977', 'email': 'emailfreedom.ml', 'department': 'department_977', 'designation': 'designation_977'},
        {'name': 'name_978', 'email': 'emailgenerator.de', 'department': 'department_978', 'designation': 'designation_978'},
        {'name': 'name_979', 'email': 'emailgo.de', 'department': 'department_979', 'designation': 'designation_979'},
        {'name': 'name_980', 'email': 'emailias.com', 'department': 'department_980', 'designation': 'designation_980'},
        {'name': 'name_981', 'email': 'emailigo.de', 'department': 'department_981', 'designation': 'designation_981'},
        {'name': 'name_982', 'email': 'emailinfive.com', 'department': 'department_982', 'designation': 'designation_982'},
        {'name': 'name_983', 'email': 'emailisvalid.com', 'department': 'department_983', 'designation': 'designation_983'},
        {'name': 'name_984', 'email': 'emaillime.com', 'department': 'department_984', 'designation': 'designation_984'},
        {'name': 'name_985', 'email': 'emailmiser.com', 'department': 'department_985', 'designation': 'designation_985'},
        {'name': 'name_986', 'email': 'emailna.co', 'department': 'department_986', 'designation': 'designation_986'},
        {'name': 'name_987', 'email': 'emailnax.com', 'department': 'department_987', 'designation': 'designation_987'},
        {'name': 'name_988', 'email': 'emailo.pro', 'department': 'department_988', 'designation': 'designation_988'},
        {'name': 'name_989', 'email': 'emailondeck.com', 'department': 'department_989', 'designation': 'designation_989'},
        {'name': 'name_990', 'email': 'emailportal.info', 'department': 'department_990', 'designation': 'designation_990'},
        {'name': 'name_991', 'email': 'emailproxsy.com', 'department': 'department_991', 'designation': 'designation_991'},
        {'name': 'name_992', 'email': 'emailresort.com', 'department': 'department_992', 'designation': 'designation_992'},
        {'name': 'name_993', 'email': 'emails.ga', 'department': 'department_993', 'designation': 'designation_993'},
        {'name': 'name_994', 'email': 'emailsecurer.com', 'department': 'department_994', 'designation': 'designation_994'},
        {'name': 'name_995', 'email': 'emailsensei.com', 'department': 'department_995', 'designation': 'designation_995'},
        {'name': 'name_996', 'email': 'emailsingularity.net', 'department': 'department_996', 'designation': 'designation_996'},
        {'name': 'name_997', 'email': 'emailspam.cf', 'department': 'department_997', 'designation': 'designation_997'},
        {'name': 'name_998', 'email': 'emailspam.ga', 'department': 'department_998', 'designation': 'designation_998'},
        {'name': 'name_999', 'email': 'emailspam.gq', 'department': 'department_999', 'designation': 'designation_999'},
        {'name': 'name_1000', 'email': 'emailspam.ml', 'department': 'department_1000', 'designation': 'designation_1000'}
    ]

    # colleagues = [Colleagues(name=data['name'], email=data['email'],
    #                          designation=data['designation']) for data in colleagues_data]

    for data in colleagues_data:
        existing_colleague = Colleagues.query.filter_by(
            email=data['email']).first()
        if not existing_colleague:
            colleague = Colleagues(
                name=data['name'], email=data['email'], department=data['department'], designation=data['designation'])
            db.session.add(colleague)

    users_data = [
        {"email": "tech@kvqaindia.com",
            "username": "tech@kvqaindia", "password": "asdfgh"}
    ]

    for data in users_data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if not existing_user:
            user = User(email=data['email'], username=data['username'])
            user.set_password(data['password'])
            db.session.add(user)

    db.session.commit()


with app.app_context():
    # create_database()
    db.create_all()
    insert_dummy_data()


class EmailTemplate:
    def __init__(self, template_file):

        with open(template_file, 'r') as file:
            self.template = file.read()

    def generate_email(self, sender_name, sender_email, recipient_name, subject):

        email_content = self.template
        email_content = email_content.replace('{{sender_name}}', sender_name)
        email_content = email_content.replace('{{sender_email}}', sender_email)
        email_content = email_content.replace(
            '{{recipient_name}}', recipient_name)
        email_content = email_content.replace('{{subject}}', subject)

        email_content = email_content.replace('\n', '<br>')
        email_content = email_content.replace('\n\n', '</p><p>')
        email_content = f"<p>{email_content}</p>"

        return email_content


@app.route('/')
def home():
    return 'Hello World'


@app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
#         return jsonify({'message': 'User with this email or username already exists!'}), 409
#     new_user = User(email=email, username=username)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User registered successfully'}), 201
def register():
    data = request.get_json()

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({"message": "All fields are required."}), 400

    # Check if the user already exists
    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"message": "User with this email or username already exists."}), 400

    try:
        # Create a new user
        new_user = User(email=email, username=username,
                        password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error registering user: {str(e)}"}), 500


@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    username = credentials.get('username')
    password = credentials.get('password')

    user = User.query.filter_by(
        username=username).first()

    if user and user.check_password(password):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(
            payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Login Successful", "access_token": token}), 200

    return jsonify({"message": "Invalid username or password"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


emailed_candidates = []


# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

#     colleagues = Colleagues.query.all()

#     # part_size = len(colleagues) // 3
#     # group1 = colleagues[:part_size]
#     # group2 = colleagues[part_size:2*part_size]
#     # group3 = colleagues[2*part_size:]

#     part_size = len(colleagues) // 4
#     group1 = colleagues[:part_size]
#     group2 = colleagues[part_size:2*part_size]
#     group3 = colleagues[2*part_size:3*part_size]
#     group4 = colleagues[3*part_size:]

#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },

#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     # send_group_email(group1, department_config['HR'], templates_dir)
#     # send_group_email(group2, department_config['Leadership'], templates_dir)
#     # send_group_email(group3, department_config['Developer'], templates_dir)

#     # return jsonify({'message': 'Phishing emails sent to colleagues.'})

#     try:
#         send_group_email(group1, department_config['HR'], templates_dir)
#         send_group_email(
#             group2, department_config['Leadership'], templates_dir)
#         send_group_email(group3, department_config['Developer'], templates_dir)
#         send_group_email(group4, department_config['Account'], templates_dir)

#         return jsonify({
#             'message': 'Phishing emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email(group, config, templates_dir):
#     """Helper function to send emails to a group with specific department config."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     for colleague in group:
#         tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"

#         print(f"Generated tracking link for {colleague.name}: {tracking_link}")

#         to_email = colleague.email
#         msg = MIMEMultipart('related')
#         msg['Subject'] = email_subject
#         msg['From'] = from_email
#         msg['To'] = to_email

#         body = email_template.replace("{{recipient_name}}", colleague.name)
#         body = body.replace("{{action_link}}", tracking_link)
#         body = body.replace("{{action_name}}", action_name)
#         body = body.replace("{{email_subject}}", email_subject)

#         html_content = f"""
#         <html>
#             <body>
#                 {body}
#             </body>
#         </html>
#         """
#         msg.attach(MIMEText(html_content, 'html'))

#         try:
#             # with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             #     server.starttls()
#             #     server.login(from_email, password)
#             #     server.send_message(msg)
#             # print(f"Email sent to {colleague.email}")

#             # with smtplib.SMTP_SSL('smtp.secureserver.net', 465) as server:
#             #     server.login(from_email, password)
#             #     server.send_message(msg)
#             # print(f"Email sent to {colleague.email}")

#             with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#                 server.starttls()
#                 server.login(from_email, password)
#                 server.send_message(msg)
#             print(f"Email sent to {colleague.email}")

#             # emailed_candidates.append({
#             #     'name': colleague.name,
#             #     'email': colleague.email,
#             #     'designation': colleague.designation
#             # })
#             update_email_log(colleague)
#             emailed_candidates.append({
#                 'name': colleague.name,
#                 'email': colleague.email,
#                 'designation': colleague.designation
#             })
#             print("Emailed candidates list after sending:", emailed_candidates)

#         except Exception as e:
#             print(f"Failed to send email to {colleague.email}: {str(e)}")

# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
#     colleagues = Colleagues.query.all()

#     part_size = len(colleagues) // 4
#     group1 = colleagues[:part_size]
#     group2 = colleagues[part_size:2*part_size]
#     group3 = colleagues[2*part_size:3*part_size]
#     group4 = colleagues[3*part_size:]

#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },
#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         send_group_email(group1, department_config['HR'], templates_dir)
#         send_group_email(
#             group2, department_config['Leadership'], templates_dir)
#         send_group_email(group3, department_config['Developer'], templates_dir)
#         send_group_email(group4, department_config['Account'], templates_dir)

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email(group, config, templates_dir, batch_size=10, delay=10):
#     """Helper function to send emails to a group in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     try:
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             for i in range(0, len(group), batch_size):
#                 batch = group[i:i + batch_size]

#                 for colleague in batch:
#                     # tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                     tracking_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     body = email_template.replace(
#                         "{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         update_email_log(colleague)
#                         emailed_candidates.append({
#                             'name': colleague.name,
#                             'email': colleague.email,
#                             'designation': colleague.designation
#                         })

#                     except Exception as e:
#                         print(
#                             f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between each batch to manage CPU load
#                 time.sleep(delay)
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 80:  # If memory usage exceeds 80%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")


#######

# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

#     # Define group sizes
#     groups = [
#         {'start': 0, 'end': 400, 'config': 'Developer'},
#         {'start': 400, 'end': 788, 'config': 'Developer'},
#         {'start': 788, 'end': 802, 'config': 'Leadership'},
#         {'start': 802, 'end': 986, 'config': 'HR'},
#         {'start': 986, 'end': 1000, 'config': 'Account'}
#     ]

#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },
#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         # Process each group separately
#         for group in groups:
#             send_group_email_in_batches(
#                 start_idx=group['start'],
#                 end_idx=group['end'],
#                 config=department_config[group['config']],
#                 templates_dir=templates_dir
#             )

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email_in_batches(start_idx, end_idx, config, templates_dir, batch_size=5, delay=15):
#     """Send emails to a subset of the database in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     try:
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             # Load the data in small batches
#             for i in range(start_idx, end_idx, batch_size):
#                 batch = Colleagues.query.filter(
#                     Colleagues.id >= i + 1,
#                     Colleagues.id < i + batch_size + 1
#                 ).all()

#                 if not batch:
#                     break  # Stop if there are no more records

#                 for colleague in batch:
#                     tracking_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     body = email_template.replace(
#                         "{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         update_email_log(colleague)
#                         emailed_candidates.append({
#                             'name': colleague.name,
#                             'email': colleague.email,
#                             'designation': colleague.designation
#                         })

#                     except Exception as e:
#                         print(
#                             f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between each batch to manage CPU load
#                 time.sleep(delay)
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 70:  # If memory usage exceeds 70%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")


#######


# groups = [
#     {'start': 0, 'end': 400, 'config': 'Developer'},
#     {'start': 400, 'end': 788, 'config': 'Developer'},
#     {'start': 788, 'end': 802, 'config': 'Leadership'},
#     {'start': 802, 'end': 986, 'config': 'HR'},
#     {'start': 986, 'end': 1000, 'config': 'Account'}
# ]

# department_config = {
#     'HR': {
#         'email': os.getenv('HR_EMAIL'),
#         'password': os.getenv('HR_PASSWORD'),
#         'template': 'hr_email_template.html',
#         'subject': "Update Your Payroll Information for Q4",
#         'action_name': "Update Payroll Information"
#     },
#     'Leadership': {
#         'email': os.getenv('LEADERSHIP_EMAIL'),
#         'password': os.getenv('LEADERSHIP_PASSWORD'),
#         'template': 'leadership_template.html',
#         'subject': "Strategic Plan Review for Q4 - Action Required",
#         'action_name': "Review Strategic Plan"
#     },
#     'Developer': {
#         'email': os.getenv('DEVELOPER_EMAIL'),
#         'password': os.getenv('DEVELOPER_PASSWORD'),
#         'template': 'developer_template.html',
#         'subject': "Security Patch Deployment for Development Tools",
#         'action_name': "Download Security Patch"
#     },
#     'Account': {
#         'email': os.getenv('ACCOUNT_EMAIL'),
#         'password': os.getenv('ACCOUNT_PASSWORD'),
#         'template': 'accounts_email_template.html',
#         'subject': "System Update for new Compliance Standards",
#         'action_name': "Update Credential"
#     }
# }

# templates_dir = os.path.join(os.path.dirname(__file__), 'templates')


# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     """API to trigger email sending process."""
#     global emailed_candidates
#     emailed_candidates = []  # Reset the emailed candidates log

#     try:
#         # Call the function to send emails group by group
#         send_emails_by_group(groups, department_config, templates_dir)

#         return jsonify({'message': 'Emails are being sent successfully.', 'status': 'success'}), 200

#     except Exception as e:
#         return jsonify({'message': f'Error: {str(e)}', 'status': 'error'}), 500


# def send_emails_by_group(groups, department_config, templates_dir):
#     """Send emails group by group."""
#     global emailed_candidates

#     for group in groups:
#         config = department_config[group['config']]
#         print(f"Processing group: {group['config']}")

#         # Load the template for the group
#         with open(os.path.join(templates_dir, config['template'])) as f:
#             email_template = f.read()

#         send_emails_in_batches(
#             start_idx=group['start'],
#             end_idx=group['end'],
#             config=config,
#             templates_dir=templates_dir,
#             email_template=email_template,
#             batch_size=5,  # 5 emails per batch
#             email_delay=2,  # 2 seconds between emails
#             batch_delay=15  # 15 seconds between batches
#         )

#         # Clean up after finishing a group
#         gc.collect()  # Release memory
#         time.sleep(10)  # 10 seconds delay before the next group


# def send_emails_in_batches(start_idx, end_idx, config, templates_dir, email_template, batch_size, email_delay, batch_delay):
#     """Send emails in smaller batches with delays."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']
#     training_link = "https://trial-ria-app.vercel.app/phishing_test/common_training_link"  # Common link

#     try:
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             for i in range(start_idx, end_idx, batch_size):
#                 # Query the batch
#                 batch = Colleagues.query.filter(
#                     Colleagues.id >= i + 1,
#                     Colleagues.id < i + batch_size + 1
#                 ).options(load_only(Colleagues.id, Colleagues.name, Colleagues.email, Colleagues.designation)).all()

#                 if not batch:
#                     break  # Stop if no more records

#                 for colleague in batch:
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     # Replace placeholders in the email template
#                     body = email_template.replace(
#                         "{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", training_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         # Log email sent
#                         update_email_log(colleague)
#                         emailed_candidates.append({
#                             'name': colleague.name,
#                             'email': colleague.email,
#                             'designation': colleague.designation
#                         })

#                     except Exception as e:
#                         print(
#                             f"Failed to send email to {colleague.email}: {str(e)}")

#                     # Delay between emails
#                     time.sleep(email_delay)

#                 # Clean up after processing a batch
#                 gc.collect()
#                 time.sleep(batch_delay)

#     except Exception as e:
#         print(f"Error in sending emails: {str(e)}")


### New code

groups = [
    {'start': 0, 'end': 400, 'config': 'Developer'},
    {'start': 400, 'end': 788, 'config': 'Developer'},
    {'start': 788, 'end': 802, 'config': 'Leadership'},
    {'start': 802, 'end': 986, 'config': 'HR'},
    {'start': 986, 'end': 1000, 'config': 'Account'}
]

department_config = {
    'HR': {
        'email': os.getenv('HR_EMAIL'),
        'password': os.getenv('HR_PASSWORD'),
        'template': 'hr_email_template.html',
        'subject': "Update Your Payroll Information for Q4",
        'action_name': "Update Payroll Information"
    },
    'Leadership': {
        'email': os.getenv('LEADERSHIP_EMAIL'),
        'password': os.getenv('LEADERSHIP_PASSWORD'),
        'template': 'leadership_template.html',
        'subject': "Strategic Plan Review for Q4 - Action Required",
        'action_name': "Review Strategic Plan"
    },
    'Developer': {
        'email': os.getenv('DEVELOPER_EMAIL'),
        'password': os.getenv('DEVELOPER_PASSWORD'),
        'template': 'developer_template.html',
        'subject': "Security Patch Deployment for Development Tools",
        'action_name': "Download Security Patch"
    },
    'Account': {
        'email': os.getenv('ACCOUNT_EMAIL'),
        'password': os.getenv('ACCOUNT_PASSWORD'),
        'template': 'accounts_email_template.html',
        'subject': "System Update for new Compliance Standards",
        'action_name': "Update Credential"
    }
}

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
# common_training_link = "https://trial-ria-app.vercel.app/phishing_test/common_training_link"
# common_training_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"


# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     """API to trigger email sending process."""
#     try:
#         # Process each group
#         for group in groups:
#             config = department_config[group['config']]
#             print(f"Processing group: {group['config']}")

#             # Load the email template once per group
#             with open(os.path.join(templates_dir, config['template'])) as f:
#                 email_template = f.read()

#             # SMTP connection setup
#             with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#                 server.starttls()
#                 server.login(config['email'], config['password'])

#                 # Process emails in batches
#                 for i in range(group['start'], group['end'], 5):  # Batch size = 5
#                     # Query a batch of emails
#                     batch = Colleagues.query.filter(
#                         Colleagues.id >= i + 1,
#                         Colleagues.id < i + 6  # 5 emails per batch
#                     ).with_entities(Colleagues.id, Colleagues.name, Colleagues.email, Colleagues.designation).yield_per(5)

#                     if not batch:
#                         break  # No more records in the group

#                     for colleague in batch:
#                         to_email = colleague.email
#                         msg = MIMEMultipart('related')
#                         msg['Subject'] = config['subject']
#                         msg['From'] = config['email']
#                         msg['To'] = to_email

#                         # Replace placeholders in the email template
#                         body = email_template.replace(
#                             "{{recipient_name}}", colleague.name)
#                         body = body.replace("{{action_link}}", common_training_link)
#                         body = body.replace("{{action_name}}", config['action_name'])
#                         body = body.replace("{{email_subject}}", config['subject'])

#                         html_content = f"""
#                         <html>
#                             <body>
#                                 {body}
#                             </body>
#                         </html>
#                         """
#                         msg.attach(MIMEText(html_content, 'html'))

#                         try:
#                             server.send_message(msg)
#                             print(f"Email sent to {colleague.email}")

#                             # Log email sent (store in database or a file)
#                             update_email_log(colleague)
#                             emailed_candidates.append({
#                                 'name': colleague.name,
#                                 'email': colleague.email,
#                                 'designation': colleague.designation
#                             })

#                         except Exception as e:
#                             print(f"Failed to send email to {colleague.email}: {str(e)}")

#                         # Delay between emails
#                         time.sleep(dynamic_delay())

#                     # Clean up batch from memory
#                     del batch
#                     gc.collect()
#                     time.sleep(15)  # Batch delay

#             # Clean up group from memory
#             del email_template
#             gc.collect()
#             time.sleep(10)  # Group delay

#         return jsonify({'message': 'Emails have been sent successfully.', 'status': 'success'}), 200

#     except Exception as e:
#         return jsonify({'message': f'Error: {str(e)}', 'status': 'error'}), 500



@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        emails_sent = []  # Keep track of sent emails
        failed_emails = []  # Track failed emails for debugging

        # SMTP connection setup
        with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
            server.starttls()
            server.login(os.getenv('DEVELOPER_EMAIL'), os.getenv('DEVELOPER_PASSWORD'))  # Adjust based on department

            # Fetch emails from the database for a specific group
            for colleague in Colleagues.query.filter(Colleagues.id >= 1, Colleagues.id <= 400):  # Adjust range for each group
                to_email = colleague.email
                config = department_config['Developer']  # Adjust based on group
                msg = MIMEMultipart('related')
                msg['Subject'] = config['subject']
                msg['From'] = config['email']
                msg['To'] = to_email

                # Prepare the email body
                with open(os.path.join('templates', config['template'])) as f:
                    email_template = f.read()

                common_training_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"

                body = email_template.replace("{{recipient_name}}", colleague.name)
                body = body.replace("{{action_link}}", common_training_link)
                body = body.replace("{{action_name}}", config['action_name'])
                body = body.replace("{{email_subject}}", config['subject'])

                html_content = f"<html><body>{body}</body></html>"
                msg.attach(MIMEText(html_content, 'html'))

                try:
                    # Send the email
                    server.send_message(msg)
                    emails_sent.append(colleague.email)  # Track successful email

                    # Log the email in the database
                    update_email_log(colleague)

                    # Log progress with a print statement (to avoid Gunicorn timeout)
                    print(f"Email successfully sent to: {colleague.email}")

                    # Optional: delay to avoid too rapid sending
                    time.sleep(1)  # Small delay between emails

                except Exception as e:
                    print(f"Failed to send email to {colleague.email}: {str(e)}")
                    failed_emails.append(colleague.email)  # Track failed email

        # After processing all emails, print a completion log
        print(f"All emails processed. Sent: {len(emails_sent)}, Failed: {len(failed_emails)}")

        return jsonify({
            'message': 'Emails sent successfully.',
            'status': 'success',
            'emails_sent': emails_sent,
            'failed_emails': failed_emails
        }), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'message': f"Error: {str(e)}", 'status': 'error'}), 500





def dynamic_delay():
    """Calculate delay based on system resource usage."""
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=0.1)
    if memory_usage > 80 or cpu_usage > 80:
        return 15  # Increase delay under high load
    elif memory_usage < 50 and cpu_usage < 50:
        return 10  # Decrease delay under low load
    return 5  # Default delay


# def send_group_email(group, config, templates_dir, batch_size=10, delay=10):
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#         server.starttls()
#         server.login(from_email, password)

#         for i in range(0, len(group), batch_size):
#             batch = group[i:i + batch_size]  # Process emails in batches
#             for colleague in batch:
#                 tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                 body = email_template.replace(
#                     "{{recipient_name}}", colleague.name)
#                 body = body.replace("{{action_link}}", tracking_link)
#                 body = body.replace("{{action_name}}", action_name)
#                 body = body.replace("{{email_subject}}", email_subject)

#                 msg = MIMEMultipart('related')
#                 msg['Subject'] = email_subject
#                 msg['From'] = from_email
#                 msg['To'] = colleague.email
#                 msg.attach(MIMEText(body, 'html'))

#                 try:
#                     server.send_message(msg)
#                     print(f"Email sent to {colleague.email}")
#                 except Exception as e:
#                     print(
#                         f"Failed to send email to {colleague.email}: {str(e)}")
#                 finally:
#                     del msg  # Explicitly delete the message object to free memory

#             time.sleep(delay)  # Delay before the next batch

# def log_system_usage():
#     # CPU Usage
#     cpu_usage = psutil.cpu_percent()  # Overall CPU usage as a percentage
#     cpu_count = psutil.cpu_count()  # Total number of CPU cores

#     # Memory Usage
#     memory = psutil.virtual_memory()
#     memory_usage = memory.percent  # Memory usage as a percentage
#     memory_total = memory.total  # Total memory (in bytes)
#     memory_available = memory.available  # Available memory (in bytes)
#     memory_used = memory.used  # Used memory (in bytes)

#     print(f"CPU Usage: {cpu_usage}%")
#     print(f"Number of CPU cores: {cpu_count}")
#     print(f"Memory Usage: {memory_usage}%")
#     print(f"Total Memory: {memory_total / (1024 ** 3):.2f} GB")
#     print(f"Used Memory: {memory_used / (1024 ** 3):.2f} GB")
#     print(f"Available Memory: {memory_available / (1024 ** 3):.2f} GB")

# return cpu_usage, cpu_count, memory_usage, memory_total, memory_used, memory_available

def log_system_usage():
    # CPU Usage
    cpu_usage = psutil.cpu_percent()  # Overall CPU usage as a percentage

    # Memory Usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent  # Memory usage as a percentage

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")

    return cpu_usage, memory_usage

# Send email function
# def send_group_email(group, config, templates_dir, batch_size=10, delay=10):
#     """Helper function to send emails to a group in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     # Load the email template from cache or file
#     email_template = cache.get('email_template')
#     if email_template is None:
#         with open(os.path.join(templates_dir, config['template'])) as f:
#             email_template = f.read()
#         cache.set('email_template', email_template)

#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             # Process emails in batches
#             for i in range(0, len(group), batch_size):
#                 batch = group[i:i + batch_size]

#                 for colleague in batch:
#                     tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     # Customize the email body with the colleague's name and tracking link
#                     body = email_template.replace("{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         # Log the sent email details
#                         update_email_log(colleague)

#                     except Exception as e:
#                         print(f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between batches to prevent overloading the CPU
#                 time.sleep(delay)

#                 # Log system usage and perform garbage collection
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 80:  # If memory usage exceeds 80%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")

# # Email sending route
# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
#     colleagues = Colleagues.query.all()

#     # Define groupings
#     part_size = len(colleagues) // 5
#     group1 = colleagues[:8]
#     group2 = colleagues[8:13]
#     group3 = colleagues[13:18]
#     group4 = colleagues[18:20]
#     group5 = colleagues[20:]

#     # Department configuration
#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },

#         'Developer_1': {
#             'email': os.getenv('DEVELOPER_EMAIL_1'),
#             'password': os.getenv('DEVELOPER_PASSWORD_1'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },


#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         # Send emails for each group
#         send_group_email(group1, department_config['Developer'], templates_dir)
#         send_group_email(group2, department_config['Developer_1'], templates_dir)
#         send_group_email(group3, department_config['HR'], templates_dir)
#         send_group_email(group4, department_config['Account'], templates_dir)
#         send_group_email(group5, department_config['Leadership'], templates_dir)

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email(group_start, group_end, config, templates_dir, batch_size=10, delay=10):
#     """Helper function to send emails to a group in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     # Load the email template from cache or file
#     email_template = cache.get('email_template')
#     if email_template is None:
#         with open(os.path.join(templates_dir, config['template'])) as f:
#             email_template = f.read()
#         cache.set('email_template', email_template)

#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             # Query the database for the batch of colleagues
#             session = Session()
#             colleagues = session.query(Colleagues).slice(group_start, group_end).all()

#             # Process emails in batches
#             for i in range(0, len(colleagues), batch_size):
#                 batch = colleagues[i:i + batch_size]

#                 for colleague in batch:
#                     tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     # Customize the email body with the colleague's name and tracking link
#                     body = email_template.replace("{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         # Log the sent email details
#                         update_email_log(colleague)

#                     except Exception as e:
#                         print(f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between batches to prevent overloading the CPU
#                 time.sleep(delay)

#                 # Log system usage and perform garbage collection
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 80:  # If memory usage exceeds 80%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")

# # Email sending route
# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

#     # Define the range of colleagues for each group based on your specified ranges
#     group_ranges = [
#         (1, 8),    # Group 1 (First 400 colleagues)
#         (8, 14),  # Group 2 (Next 388 colleagues)
#         (14, 18),  # Group 3 (Next 14 colleagues)
#         (18, 20),  # Group 4 (Next 184 colleagues)
#         (20, 21)  # Group 5 (Remaining 14 colleagues)
#     ]

#     # Department configuration
#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },
#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         # Send emails for each group
#         send_group_email(group_ranges[0][0], group_ranges[0][1], department_config['Developer'], templates_dir)
#         send_group_email(group_ranges[1][0], group_ranges[1][1], department_config['Developer'], templates_dir)
#         send_group_email(group_ranges[2][0], group_ranges[2][1], department_config['HR'], templates_dir)
#         send_group_email(group_ranges[3][0], group_ranges[3][1], department_config['Account'], templates_dir)
#         send_group_email(group_ranges[4][0], group_ranges[4][1], department_config['Leadership'], templates_dir)

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def update_email_log(colleague):
#     """Single function to update the record in the EmailLogs table."""
#     try:
#         # Create a new email log entry
#         email_log = EmailLogs(
#             colleague_id=colleague.id,
#             email_address=colleague.email
#         )
#         db.session.add(email_log)
#         db.session.commit()
#         print(f"Email log added for {colleague.name}")
#     except Exception as e:
#         db.session.rollback()
#         print(f"Failed to log email for {colleague.name}: {str(e)}")


def update_email_log(colleague):
    """Function to update the record in the EmailLogs table."""
    try:
        # Capture the current time for when the email is sent
        sent_date = datetime.utcnow()

        # Create a new email log entry with colleague's details and sent date
        email_log = EmailLogs(
            colleague_id=colleague.id,
            email_address=colleague.email,
            sent_date=sent_date  # Store the sent date
        )

        # Add to session and commit to save it in the database
        db.session.add(email_log)
        db.session.commit()
        print(f"Email log added for {colleague.name}")

    except Exception as e:
        db.session.rollback()
        print(f"Failed to log email for {colleague.name}: {str(e)}")


@app.route('/phishing_test/<int:colleague_id>', methods=['GET'])
def phishing_test(colleague_id):
    print(f'Phishing test accessed for colleague ID: {colleague_id}')

    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return jsonify({'error': 'Colleague not found.'}), 404

    return jsonify({'message': 'Tracking link accessed successfully', 'colleague_id': colleague_id})


# @app.route('/generate_emailed_candidates_report', methods=['GET', 'POST'])
# def generate_emailed_candidates_report():
#     global emailed_candidates

#     if not emailed_candidates:
#         print("No candidates in emailed_candidates:",
#               emailed_candidates)
#         return jsonify({'error': 'No successfully emailed candidates.'}), 400

#     print("Generating CSV for:", emailed_candidates)

#     try:
#         csv_file_path = "emailed_candidates_report.csv"
#         with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
#             fieldnames = ['name', 'email', 'department',
#                           'designation', 'clicked_date']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             writer.writeheader()
#             writer.writerows(emailed_candidates)

#         return send_file(csv_file_path, as_attachment=True)
#     except Exception as e:
#         print(f"Error generating report: {str(e)}")
#         return jsonify({'error': str(e)}), 500


@app.route('/generate_emailed_candidates_report', methods=['GET'])
def generate_emailed_candidates_report():
    try:
        # Fetch all email logs
        email_logs = EmailLogs.query.all()
        if not email_logs:
            return jsonify({'error': 'No candidates have been emailed yet.'}), 400

        # Prepare list of emailed candidates with additional fields
        emailed_candidates = []
        for log in email_logs:
            colleague = log.colleague  # Get colleague related to the log
            emailed_candidates.append({
                'name': colleague.name,  # Get colleague name
                'email': log.email_address,  # Get email from log
                'department': colleague.department,  # Get department from colleague model
                'designation': colleague.designation,  # Get designation from colleague model
                # Format sent date
                'sent_date': log.sent_date.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Generate CSV report
        csv_file_path = "emailed_candidates_report.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'department',
                          'designation', 'sent_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(emailed_candidates)

        # Return the CSV file as download
        return send_file(csv_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users')
def users():
    user = Colleagues.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'department': u.department, 'designation': u.designation} for u in user])


@app.route('/phising_click/<int:colleague_id>', methods=['POST'])
def phising_click(colleague_id):
    print(f'Received request for colleague ID: {colleague_id}')

    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return jsonify({'error': 'Colleague not found.'}), 404

    report = Reports.query.filter_by(colleague_id=colleague_id).first()

    if report:
        report.clicked = True
        report.clicked_date = datetime.now()
        print(
            f"Updated clicked_date for existing report: {report.clicked_date}")

    else:
        report = Reports(
            colleague_id=colleague_id,
            clicked=True,
            clicked_date=datetime.now(),
            answered=False,
            answers={}
        )
        db.session.add(report)
        print(f"Created new report with clicked_date: {report.clicked_date}")

    db.session.commit()

    candidate_data = {
        'id': colleague.id,
        'name': colleague.name,
        'email': colleague.email,
        'department': colleague.department,
        'designation': colleague.designation
    }

    return jsonify({'message': 'Click recorded', 'candidate': candidate_data})


@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Reports.query.all()
    report_data = [{'id': r.id, 'colleague_id': r.colleague_id, 'clicked': r.clicked,
                    'answered': r.answered, 'answers': r.answers, 'status': r.status, 'score': r.score, 'clicked_date': r.clicked_date} for r in reports]
    return jsonify(report_data)


@app.route('/phishing_opened/<int:colleague_id>', methods=['GET'])
def phishing_opened(colleague_id):
    report = Reports.query.filter_by(colleague_id=colleague_id).first()
    print(
        f'Processing click for colleague ID: {colleague_id} | Existing report: {report}')

    if report:
        report.clicked = True
        print(f'Updated existing report for ID {colleague_id} to clicked=True')
    else:
        report = Reports(colleague_id=colleague_id,
                         clicked=True, answered=False, answers={}, clicked_date=datetime.now())
        db.session.add(report)
        print(f'Created new report for ID {colleague_id} with clicked=True')

    db.session.commit()
    return jsonify({'message': 'Thank you for participating in our phishing awareness program.', 'showPopup': True})


@app.route('/generate_reports', methods=['GET', 'POST'])
def generate_reports():
    try:
        reports = Reports.query.all()
        report_data = []

        for report in reports:
            colleague = Colleagues.query.get(report.colleague_id)
            report_entry = {
                'Colleague Name': colleague.name,
                'Colleague Email': colleague.email,
                'Department': colleague.department,
                'Designation': colleague.designation,
                'Link Clicked': 'Yes' if report.clicked else 'No',
                'Score': report.score,
                'Status': report.status,
                'Completion Date': report.clicked_date.strftime('%Y-%m-%d') if report.clicked_date else None,
            }
            report_data.append(report_entry)

        csv_file_path = "candidate_reports.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Colleague Name', 'Colleague Email', 'Department',
                          'Designation', 'Link Clicked', 'Score',
                          'Status', 'Completion Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in report_data:
                writer.writerow(data)

        return send_file(csv_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload_colleagues_data', methods=['POST'])
def upload_colleagues_data():
    try:
        db.session.query(Colleagues).delete()

        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                colleague = Colleagues(
                    name=row['Full Name'],
                    email=row['Work Email'],
                    department=row['Department'],
                    designation=row['Job Title']
                )
                db.session.add(colleague)

            db.session.commit()
            return jsonify({'message': 'Data uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Invalid file format. Please upload an .xlsx file.'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error processing file: {str(e)}'}), 500


@app.route('/get_all_reports', methods=['GET'])
def get_all_reports():
    try:
        reports = Reports.query.all()
        report_data = [{'id': r.id, 'colleague_id': r.colleague_id, 'clicked': r.clicked,
                        'answered': r.answered, 'answers': r.answers, 'status': r.status, 'score': r.score, 'clicked_date': r.clicked_date} for r in reports]
        return jsonify({'reports': report_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_dashboard_clicked_report', methods=['GET'])
def generate_dashboard_clicked_report():
    clicked_reports = Reports.query.filter_by(clicked=True).all()

    if not clicked_reports:
        return jsonify({'error': 'No candidates have clicked the link.'}), 400

    clicked_candidates = []
    for report in clicked_reports:
        colleague = report.colleague
        clicked_candidates.append({
            'name': colleague.name,
            'email': colleague.email,
            'department': colleague.department,
            'designation': colleague.designation,
            'clicked_date': report.clicked_date.strftime('%Y-%m-%d') if report.clicked_date else None
        })

    try:
        csv_file_path = "dashboard_clicked_candidates_report.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'department',
                          'designation', 'clicked_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(clicked_candidates)

        return send_file(csv_file_path, as_attachment=True)

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
