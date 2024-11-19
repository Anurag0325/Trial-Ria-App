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
        # {"name": "Anurag Kumar", "email": "akanuragkumar75@gmail.com",
        #     "department": "Developer", "designation": "Developer"},
        # {"name": "Sethi", "email": "tech@kvqaindia.com",
        #     "department": "Developer", "designation": "Frontend Developer"},
        # {"name": "Ritika Gupta", "email": "guptaritika705@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
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

        # {"name": "Ritika", "email": "training@kvqaindia.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "lav@kvqaindia.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun", "email": "2345varun@gmail.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG", "email": "trg@kvqaindia.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales", "email": "sales1@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO", "email": "noidaiso22@gmail.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby", "email": "ruby@kvqaindia.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli", "email": "babli12@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha", "email": "shikha12@kvqaindia.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan", "email": "kanchan@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info", "email": "info@kvqaindia.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali", "email": "vaishali@kvqaindia.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha", "email": "neha12@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR", "email": "dhr@kvqaindia.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi", "email": "delhi@kvqaindia.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun", "email": "arun.kvqa@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS", "email": "ops@kvqaindia.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Himanshi", "email": "himanshichaudhary8377@gmail.com",
        #     "department": "Data Analyzer", "designation" : "Data Analyst"}

        {'name': 'Name_1', 'email': '0-mail.com',
            'department': 'Department_1', 'designation': 'Designation_1'},
        {'name': 'Name_2', 'email': '027168.com',
            'department': 'Department_2', 'designation': 'Designation_2'},
        {'name': 'Name_3', 'email': '0815.ru',
            'department': 'Department_3', 'designation': 'Designation_3'},
        {'name': 'Name_4', 'email': '0815.ry',
            'department': 'Department_4', 'designation': 'Designation_4'},
        {'name': 'Name_5', 'email': '0815.su',
            'department': 'Department_5', 'designation': 'Designation_5'},
        {'name': 'Name_6', 'email': '0845.ru',
            'department': 'Department_6', 'designation': 'Designation_6'},
        {'name': 'Name_7', 'email': '0box.eu',
            'department': 'Department_7', 'designation': 'Designation_7'},
        {'name': 'Name_8', 'email': '0clickemail.com',
            'department': 'Department_8', 'designation': 'Designation_8'},
        {'name': 'Name_9', 'email': '0n0ff.net',
            'department': 'Department_9', 'designation': 'Designation_9'},
        {'name': 'Name_10', 'email': '0nelce.com',
            'department': 'Department_10', 'designation': 'Designation_10'},
        {'name': 'Name_11', 'email': '0v.ro',
            'department': 'Department_11', 'designation': 'Designation_11'},
        {'name': 'Name_12', 'email': '0w.ro',
            'department': 'Department_12', 'designation': 'Designation_12'},
        {'name': 'Name_13', 'email': '0wnd.net',
            'department': 'Department_13', 'designation': 'Designation_13'},
        {'name': 'Name_14', 'email': '0wnd.org',
            'department': 'Department_14', 'designation': 'Designation_14'},
        {'name': 'Name_15', 'email': '0x207.info',
            'department': 'Department_15', 'designation': 'Designation_15'},
        {'name': 'Name_16', 'email': '1-8.biz',
            'department': 'Department_16', 'designation': 'Designation_16'},
        {'name': 'Name_17', 'email': '1-tm.com',
            'department': 'Department_17', 'designation': 'Designation_17'},
        {'name': 'Name_18', 'email': '10-minute-mail.com',
            'department': 'Department_18', 'designation': 'Designation_18'},
        {'name': 'Name_19', 'email': '1000rebates.stream',
            'department': 'Department_19', 'designation': 'Designation_19'},
        {'name': 'Name_20', 'email': '100likers.com',
            'department': 'Department_20', 'designation': 'Designation_20'},
        {'name': 'Name_21', 'email': '105kg.ru',
            'department': 'Department_21', 'designation': 'Designation_21'},
        {'name': 'Name_22', 'email': '10dk.email',
            'department': 'Department_22', 'designation': 'Designation_22'},
        {'name': 'Name_23', 'email': '10mail.com',
            'department': 'Department_23', 'designation': 'Designation_23'},
        {'name': 'Name_24', 'email': '10mail.org',
            'department': 'Department_24', 'designation': 'Designation_24'},
        {'name': 'Name_25', 'email': '10minut.com.pl',
            'department': 'Department_25', 'designation': 'Designation_25'},
        {'name': 'Name_26', 'email': '10minut.xyz',
            'department': 'Department_26', 'designation': 'Designation_26'},
        {'name': 'Name_27', 'email': '10minutemail.be',
            'department': 'Department_27', 'designation': 'Designation_27'},
        {'name': 'Name_28', 'email': '10minutemail.cf',
            'department': 'Department_28', 'designation': 'Designation_28'},
        {'name': 'Name_29', 'email': '10minutemail.co.uk',
            'department': 'Department_29', 'designation': 'Designation_29'},
        {'name': 'Name_30', 'email': '10minutemail.co.za',
            'department': 'Department_30', 'designation': 'Designation_30'},
        {'name': 'Name_31', 'email': '10minutemail.com',
            'department': 'Department_31', 'designation': 'Designation_31'},
        {'name': 'Name_32', 'email': '10minutemail.de',
            'department': 'Department_32', 'designation': 'Designation_32'},
        {'name': 'Name_33', 'email': '10minutemail.ga',
            'department': 'Department_33', 'designation': 'Designation_33'},
        {'name': 'Name_34', 'email': '10minutemail.gq',
            'department': 'Department_34', 'designation': 'Designation_34'},
        {'name': 'Name_35', 'email': '10minutemail.ml',
            'department': 'Department_35', 'designation': 'Designation_35'},
        {'name': 'Name_36', 'email': '10minutemail.net',
            'department': 'Department_36', 'designation': 'Designation_36'},
        {'name': 'Name_37', 'email': '10minutemail.nl',
            'department': 'Department_37', 'designation': 'Designation_37'},
        {'name': 'Name_38', 'email': '10minutemail.pro',
            'department': 'Department_38', 'designation': 'Designation_38'},
        {'name': 'Name_39', 'email': '10minutemail.us',
            'department': 'Department_39', 'designation': 'Designation_39'},
        {'name': 'Name_40', 'email': '10minutemailbox.com',
            'department': 'Department_40', 'designation': 'Designation_40'},
        {'name': 'Name_41', 'email': '10minutemails.in',
            'department': 'Department_41', 'designation': 'Designation_41'},
        {'name': 'Name_42', 'email': '10minutenemail.de',
            'department': 'Department_42', 'designation': 'Designation_42'},
        {'name': 'Name_43', 'email': '10minutesmail.com',
            'department': 'Department_43', 'designation': 'Designation_43'},
        {'name': 'Name_44', 'email': '10minutesmail.fr',
            'department': 'Department_44', 'designation': 'Designation_44'},
        {'name': 'Name_45', 'email': '10minutmail.pl',
            'department': 'Department_45', 'designation': 'Designation_45'},
        {'name': 'Name_46', 'email': '10x9.com',
            'department': 'Department_46', 'designation': 'Designation_46'},
        {'name': 'Name_47', 'email': '11163.com',
            'department': 'Department_47', 'designation': 'Designation_47'},
        {'name': 'Name_48', 'email': '123-m.com',
            'department': 'Department_48', 'designation': 'Designation_48'},
        {'name': 'Name_49', 'email': '12hosting.net',
            'department': 'Department_49', 'designation': 'Designation_49'},
        {'name': 'Name_50', 'email': '12houremail.com',
            'department': 'Department_50', 'designation': 'Designation_50'},
        {'name': 'Name_51', 'email': '12minutemail.com',
            'department': 'Department_51', 'designation': 'Designation_51'},
        {'name': 'Name_52', 'email': '12minutemail.net',
            'department': 'Department_52', 'designation': 'Designation_52'},
        {'name': 'Name_53', 'email': '12storage.com',
            'department': 'Department_53', 'designation': 'Designation_53'},
        {'name': 'Name_54', 'email': '140unichars.com',
            'department': 'Department_54', 'designation': 'Designation_54'},
        {'name': 'Name_55', 'email': '147.cl',
            'department': 'Department_55', 'designation': 'Designation_55'},
        {'name': 'Name_56', 'email': '14n.co.uk',
            'department': 'Department_56', 'designation': 'Designation_56'},
        {'name': 'Name_57', 'email': '15qm.com',
            'department': 'Department_57', 'designation': 'Designation_57'},
        {'name': 'Name_58', 'email': '1blackmoon.com',
            'department': 'Department_58', 'designation': 'Designation_58'},
        {'name': 'Name_59', 'email': '1ce.us',
            'department': 'Department_59', 'designation': 'Designation_59'},
        {'name': 'Name_60', 'email': '1chuan.com',
            'department': 'Department_60', 'designation': 'Designation_60'},
        {'name': 'Name_61', 'email': '1clck2.com',
            'department': 'Department_61', 'designation': 'Designation_61'},
        {'name': 'Name_62', 'email': '1fsdfdsfsdf.tk',
            'department': 'Department_62', 'designation': 'Designation_62'},
        {'name': 'Name_63', 'email': '1mail.ml',
            'department': 'Department_63', 'designation': 'Designation_63'},
        {'name': 'Name_64', 'email': '1pad.de',
            'department': 'Department_64', 'designation': 'Designation_64'},
        {'name': 'Name_65', 'email': '1s.fr',
            'department': 'Department_65', 'designation': 'Designation_65'},
        {'name': 'Name_66', 'email': '1secmail.com',
            'department': 'Department_66', 'designation': 'Designation_66'},
        {'name': 'Name_67', 'email': '1secmail.net',
            'department': 'Department_67', 'designation': 'Designation_67'},
        {'name': 'Name_68', 'email': '1secmail.org',
            'department': 'Department_68', 'designation': 'Designation_68'},
        {'name': 'Name_69', 'email': '1st-forms.com',
            'department': 'Department_69', 'designation': 'Designation_69'},
        {'name': 'Name_70', 'email': '1to1mail.org',
            'department': 'Department_70', 'designation': 'Designation_70'},
        {'name': 'Name_71', 'email': '1usemail.com',
            'department': 'Department_71', 'designation': 'Designation_71'},
        {'name': 'Name_72', 'email': '1webmail.info',
            'department': 'Department_72', 'designation': 'Designation_72'},
        {'name': 'Name_73', 'email': '1zhuan.com',
            'department': 'Department_73', 'designation': 'Designation_73'},
        {'name': 'Name_74', 'email': '2012-2016.ru',
            'department': 'Department_74', 'designation': 'Designation_74'},
        {'name': 'Name_75', 'email': '20email.eu',
            'department': 'Department_75', 'designation': 'Designation_75'},
        {'name': 'Name_76', 'email': '20email.it',
            'department': 'Department_76', 'designation': 'Designation_76'},
        {'name': 'Name_77', 'email': '20mail.eu',
            'department': 'Department_77', 'designation': 'Designation_77'},
        {'name': 'Name_78', 'email': '20mail.in',
            'department': 'Department_78', 'designation': 'Designation_78'},
        {'name': 'Name_79', 'email': '20mail.it',
            'department': 'Department_79', 'designation': 'Designation_79'},
        {'name': 'Name_80', 'email': '20minutemail.com',
            'department': 'Department_80', 'designation': 'Designation_80'},
        {'name': 'Name_81', 'email': '20minutemail.it',
            'department': 'Department_81', 'designation': 'Designation_81'},
        {'name': 'Name_82', 'email': '20mm.eu',
            'department': 'Department_82', 'designation': 'Designation_82'},
        {'name': 'Name_83', 'email': '2120001.net',
            'department': 'Department_83', 'designation': 'Designation_83'},
        {'name': 'Name_84', 'email': '21cn.com',
            'department': 'Department_84', 'designation': 'Designation_84'},
        {'name': 'Name_85', 'email': '247web.net',
            'department': 'Department_85', 'designation': 'Designation_85'},
        {'name': 'Name_86', 'email': '24hinbox.com',
            'department': 'Department_86', 'designation': 'Designation_86'},
        {'name': 'Name_87', 'email': '24hourmail.com',
            'department': 'Department_87', 'designation': 'Designation_87'},
        {'name': 'Name_88', 'email': '24hourmail.net',
            'department': 'Department_88', 'designation': 'Designation_88'},
        {'name': 'Name_89', 'email': '2anom.com',
            'department': 'Department_89', 'designation': 'Designation_89'},
        {'name': 'Name_90', 'email': '2chmail.net',
            'department': 'Department_90', 'designation': 'Designation_90'},
        {'name': 'Name_91', 'email': '2ether.net',
            'department': 'Department_91', 'designation': 'Designation_91'},
        {'name': 'Name_92', 'email': '2fdgdfgdfgdf.tk',
            'department': 'Department_92', 'designation': 'Designation_92'},
        {'name': 'Name_93', 'email': '2odem.com',
            'department': 'Department_93', 'designation': 'Designation_93'},
        {'name': 'Name_94', 'email': '2prong.com',
            'department': 'Department_94', 'designation': 'Designation_94'},
        {'name': 'Name_95', 'email': '2wc.info',
            'department': 'Department_95', 'designation': 'Designation_95'},
        {'name': 'Name_96', 'email': '300book.info',
            'department': 'Department_96', 'designation': 'Designation_96'},
        {'name': 'Name_97', 'email': '30mail.ir',
            'department': 'Department_97', 'designation': 'Designation_97'},
        {'name': 'Name_98', 'email': '30minutemail.com',
            'department': 'Department_98', 'designation': 'Designation_98'},
        {'name': 'Name_99', 'email': '30wave.com',
            'department': 'Department_99', 'designation': 'Designation_99'},
        {'name': 'Name_100', 'email': '3202.com',
            'department': 'Department_100', 'designation': 'Designation_100'},
        {'name': 'Name_101', 'email': '33mail.com',
            'department': 'Department_101', 'designation': 'Designation_101'},
        {'name': 'Name_102', 'email': '36ru.com',
            'department': 'Department_102', 'designation': 'Designation_102'},
        {'name': 'Name_103', 'email': '3d-painting.com',
            'department': 'Department_103', 'designation': 'Designation_103'},
        {'name': 'Name_104', 'email': '3l6.com',
            'department': 'Department_104', 'designation': 'Designation_104'},
        {'name': 'Name_105', 'email': '3mail.ga',
            'department': 'Department_105', 'designation': 'Designation_105'},
        {'name': 'Name_106', 'email': '3trtretgfrfe.tk',
            'department': 'Department_106', 'designation': 'Designation_106'},
        {'name': 'Name_107', 'email': '4-n.us',
            'department': 'Department_107', 'designation': 'Designation_107'},
        {'name': 'Name_108', 'email': '4057.com',
            'department': 'Department_108', 'designation': 'Designation_108'},
        {'name': 'Name_109', 'email': '418.dk',
            'department': 'Department_109', 'designation': 'Designation_109'},
        {'name': 'Name_110', 'email': '42o.org',
            'department': 'Department_110', 'designation': 'Designation_110'},
        {'name': 'Name_111', 'email': '4gfdsgfdgfd.tk',
            'department': 'Department_111', 'designation': 'Designation_111'},
        {'name': 'Name_112', 'email': '4k5.net',
            'department': 'Department_112', 'designation': 'Designation_112'},
        {'name': 'Name_113', 'email': '4mail.cf',
            'department': 'Department_113', 'designation': 'Designation_113'},
        {'name': 'Name_114', 'email': '4mail.ga',
            'department': 'Department_114', 'designation': 'Designation_114'},
        {'name': 'Name_115', 'email': '4nextmail.com',
            'department': 'Department_115', 'designation': 'Designation_115'},
        {'name': 'Name_116', 'email': '4nmv.ru',
            'department': 'Department_116', 'designation': 'Designation_116'},
        {'name': 'Name_117', 'email': '4tb.host',
            'department': 'Department_117', 'designation': 'Designation_117'},
        {'name': 'Name_118', 'email': '4warding.com',
            'department': 'Department_118', 'designation': 'Designation_118'},
        {'name': 'Name_119', 'email': '4warding.net',
            'department': 'Department_119', 'designation': 'Designation_119'},
        {'name': 'Name_120', 'email': '4warding.org',
            'department': 'Department_120', 'designation': 'Designation_120'},
        {'name': 'Name_121', 'email': '50set.ru',
            'department': 'Department_121', 'designation': 'Designation_121'},
        {'name': 'Name_122', 'email': '55hosting.net',
            'department': 'Department_122', 'designation': 'Designation_122'},
        {'name': 'Name_123', 'email': '5ghgfhfghfgh.tk',
            'department': 'Department_123', 'designation': 'Designation_123'},
        {'name': 'Name_124', 'email': '5gramos.com',
            'department': 'Department_124', 'designation': 'Designation_124'},
        {'name': 'Name_125', 'email': '5july.org',
            'department': 'Department_125', 'designation': 'Designation_125'},
        {'name': 'Name_126', 'email': '5mail.cf',
            'department': 'Department_126', 'designation': 'Designation_126'},
        {'name': 'Name_127', 'email': '5mail.ga',
            'department': 'Department_127', 'designation': 'Designation_127'},
        {'name': 'Name_128', 'email': '5minutemail.net',
            'department': 'Department_128', 'designation': 'Designation_128'},
        {'name': 'Name_129', 'email': '5oz.ru',
            'department': 'Department_129', 'designation': 'Designation_129'},
        {'name': 'Name_130', 'email': '5tb.in',
            'department': 'Department_130', 'designation': 'Designation_130'},
        {'name': 'Name_131', 'email': '5x25.com',
            'department': 'Department_131', 'designation': 'Designation_131'},
        {'name': 'Name_132', 'email': '5ymail.com',
            'department': 'Department_132', 'designation': 'Designation_132'},
        {'name': 'Name_133', 'email': '60minutemail.com',
            'department': 'Department_133', 'designation': 'Designation_133'},
        {'name': 'Name_134', 'email': '672643.net',
            'department': 'Department_134', 'designation': 'Designation_134'},
        {'name': 'Name_135', 'email': '675hosting.com',
            'department': 'Department_135', 'designation': 'Designation_135'},
        {'name': 'Name_136', 'email': '675hosting.net',
            'department': 'Department_136', 'designation': 'Designation_136'},
        {'name': 'Name_137', 'email': '675hosting.org',
            'department': 'Department_137', 'designation': 'Designation_137'},
        {'name': 'Name_138', 'email': '6hjgjhgkilkj.tk',
            'department': 'Department_138', 'designation': 'Designation_138'},
        {'name': 'Name_139', 'email': '6ip.us',
            'department': 'Department_139', 'designation': 'Designation_139'},
        {'name': 'Name_140', 'email': '6mail.cf',
            'department': 'Department_140', 'designation': 'Designation_140'},
        {'name': 'Name_141', 'email': '6mail.ga',
            'department': 'Department_141', 'designation': 'Designation_141'},
        {'name': 'Name_142', 'email': '6mail.ml',
            'department': 'Department_142', 'designation': 'Designation_142'},
        {'name': 'Name_143', 'email': '6paq.com',
            'department': 'Department_143', 'designation': 'Designation_143'},
        {'name': 'Name_144', 'email': '6somok.ru',
            'department': 'Department_144', 'designation': 'Designation_144'},
        {'name': 'Name_145', 'email': '6url.com',
            'department': 'Department_145', 'designation': 'Designation_145'},
        {'name': 'Name_146', 'email': '75hosting.com',
            'department': 'Department_146', 'designation': 'Designation_146'},
        {'name': 'Name_147', 'email': '75hosting.net',
            'department': 'Department_147', 'designation': 'Designation_147'},
        {'name': 'Name_148', 'email': '75hosting.org',
            'department': 'Department_148', 'designation': 'Designation_148'},
        {'name': 'Name_149', 'email': '7days-printing.com',
            'department': 'Department_149', 'designation': 'Designation_149'},
        {'name': 'Name_150', 'email': '7mail.ga',
            'department': 'Department_150', 'designation': 'Designation_150'},
        {'name': 'Name_151', 'email': '7mail.ml',
            'department': 'Department_151', 'designation': 'Designation_151'},
        {'name': 'Name_152', 'email': '7tags.com',
            'department': 'Department_152', 'designation': 'Designation_152'},
        {'name': 'Name_153', 'email': '80665.com',
            'department': 'Department_153', 'designation': 'Designation_153'},
        {'name': 'Name_154', 'email': '8127ep.com',
            'department': 'Department_154', 'designation': 'Designation_154'},
        {'name': 'Name_155', 'email': '8mail.cf',
            'department': 'Department_155', 'designation': 'Designation_155'},
        {'name': 'Name_156', 'email': '8mail.ga',
            'department': 'Department_156', 'designation': 'Designation_156'},
        {'name': 'Name_157', 'email': '8mail.ml',
            'department': 'Department_157', 'designation': 'Designation_157'},
        {'name': 'Name_158', 'email': '99.com',
            'department': 'Department_158', 'designation': 'Designation_158'},
        {'name': 'Name_159', 'email': '99cows.com',
            'department': 'Department_159', 'designation': 'Designation_159'},
        {'name': 'Name_160', 'email': '99experts.com',
            'department': 'Department_160', 'designation': 'Designation_160'},
        {'name': 'Name_161', 'email': '9mail.cf',
            'department': 'Department_161', 'designation': 'Designation_161'},
        {'name': 'Name_162', 'email': '9me.site',
            'department': 'Department_162', 'designation': 'Designation_162'},
        {'name': 'Name_163', 'email': '9mot.ru',
            'department': 'Department_163', 'designation': 'Designation_163'},
        {'name': 'Name_164', 'email': '9ox.net',
            'department': 'Department_164', 'designation': 'Designation_164'},
        {'name': 'Name_165', 'email': '9q.ro',
            'department': 'Department_165', 'designation': 'Designation_165'},
        {'name': 'Name_166', 'email': 'a-bc.net',
            'department': 'Department_166', 'designation': 'Designation_166'},
        {'name': 'Name_167', 'email': 'a45.in',
            'department': 'Department_167', 'designation': 'Designation_167'},
        {'name': 'Name_168', 'email': 'a7996.com',
            'department': 'Department_168', 'designation': 'Designation_168'},
        {'name': 'Name_169', 'email': 'aa5zy64.com',
            'department': 'Department_169', 'designation': 'Designation_169'},
        {'name': 'Name_170', 'email': 'abacuswe.us',
            'department': 'Department_170', 'designation': 'Designation_170'},
        {'name': 'Name_171', 'email': 'abakiss.com',
            'department': 'Department_171', 'designation': 'Designation_171'},
        {'name': 'Name_172', 'email': 'abcmail.email',
            'department': 'Department_172', 'designation': 'Designation_172'},
        {'name': 'Name_173', 'email': 'abilitywe.us',
            'department': 'Department_173', 'designation': 'Designation_173'},
        {'name': 'Name_174', 'email': 'abovewe.us',
            'department': 'Department_174', 'designation': 'Designation_174'},
        {'name': 'Name_175', 'email': 'absolutewe.us',
            'department': 'Department_175', 'designation': 'Designation_175'},
        {'name': 'Name_176', 'email': 'abundantwe.us',
            'department': 'Department_176', 'designation': 'Designation_176'},
        {'name': 'Name_177', 'email': 'abusemail.de',
            'department': 'Department_177', 'designation': 'Designation_177'},
        {'name': 'Name_178', 'email': 'abuser.eu',
            'department': 'Department_178', 'designation': 'Designation_178'},
        {'name': 'Name_179', 'email': 'abyssmail.com',
            'department': 'Department_179', 'designation': 'Designation_179'},
        {'name': 'Name_180', 'email': 'ac20mail.in',
            'department': 'Department_180', 'designation': 'Designation_180'},
        {'name': 'Name_181', 'email': 'academiccommunity.com',
            'department': 'Department_181', 'designation': 'Designation_181'},
        {'name': 'Name_182', 'email': 'academywe.us',
            'department': 'Department_182', 'designation': 'Designation_182'},
        {'name': 'Name_183', 'email': 'acceleratewe.us',
            'department': 'Department_183', 'designation': 'Designation_183'},
        {'name': 'Name_184', 'email': 'accentwe.us',
            'department': 'Department_184', 'designation': 'Designation_184'},
        {'name': 'Name_185', 'email': 'acceptwe.us',
            'department': 'Department_185', 'designation': 'Designation_185'},
        {'name': 'Name_186', 'email': 'acclaimwe.us',
            'department': 'Department_186', 'designation': 'Designation_186'},
        {'name': 'Name_187', 'email': 'accordwe.us',
            'department': 'Department_187', 'designation': 'Designation_187'},
        {'name': 'Name_188', 'email': 'accreditedwe.us',
            'department': 'Department_188', 'designation': 'Designation_188'},
        {'name': 'Name_189', 'email': 'acentri.com',
            'department': 'Department_189', 'designation': 'Designation_189'},
        {'name': 'Name_190', 'email': 'achievementwe.us',
            'department': 'Department_190', 'designation': 'Designation_190'},
        {'name': 'Name_191', 'email': 'achievewe.us',
            'department': 'Department_191', 'designation': 'Designation_191'},
        {'name': 'Name_192', 'email': 'acornwe.us',
            'department': 'Department_192', 'designation': 'Designation_192'},
        {'name': 'Name_193', 'email': 'acrossgracealley.com',
            'department': 'Department_193', 'designation': 'Designation_193'},
        {'name': 'Name_194', 'email': 'acrylicwe.us',
            'department': 'Department_194', 'designation': 'Designation_194'},
        {'name': 'Name_195', 'email': 'activatewe.us',
            'department': 'Department_195', 'designation': 'Designation_195'},
        {'name': 'Name_196', 'email': 'activitywe.us',
            'department': 'Department_196', 'designation': 'Designation_196'},
        {'name': 'Name_197', 'email': 'acucre.com',
            'department': 'Department_197', 'designation': 'Designation_197'},
        {'name': 'Name_198', 'email': 'acuitywe.us',
            'department': 'Department_198', 'designation': 'Designation_198'},
        {'name': 'Name_199', 'email': 'acumenwe.us',
            'department': 'Department_199', 'designation': 'Designation_199'},
        {'name': 'Name_200', 'email': 'adaptivewe.us',
            'department': 'Department_200', 'designation': 'Designation_200'},
        {'name': 'Name_201', 'email': 'adaptwe.us',
            'department': 'Department_201', 'designation': 'Designation_201'},
        {'name': 'Name_202', 'email': 'add3000.pp.ua',
            'department': 'Department_202', 'designation': 'Designation_202'},
        {'name': 'Name_203', 'email': 'addictingtrailers.com',
            'department': 'Department_203', 'designation': 'Designation_203'},
        {'name': 'Name_204', 'email': 'adeptwe.us',
            'department': 'Department_204', 'designation': 'Designation_204'},
        {'name': 'Name_205', 'email': 'adfskj.com',
            'department': 'Department_205', 'designation': 'Designation_205'},
        {'name': 'Name_206', 'email': 'adios.email',
            'department': 'Department_206', 'designation': 'Designation_206'},
        {'name': 'Name_207', 'email': 'adiq.eu',
            'department': 'Department_207', 'designation': 'Designation_207'},
        {'name': 'Name_208', 'email': 'aditus.info',
            'department': 'Department_208', 'designation': 'Designation_208'},
        {'name': 'Name_209', 'email': 'admiralwe.us',
            'department': 'Department_209', 'designation': 'Designation_209'},
        {'name': 'Name_210', 'email': 'ado888.biz',
            'department': 'Department_210', 'designation': 'Designation_210'},
        {'name': 'Name_211', 'email': 'adobeccepdm.com',
            'department': 'Department_211', 'designation': 'Designation_211'},
        {'name': 'Name_212', 'email': 'adoniswe.us',
            'department': 'Department_212', 'designation': 'Designation_212'},
        {'name': 'Name_213', 'email': 'adpugh.org',
            'department': 'Department_213', 'designation': 'Designation_213'},
        {'name': 'Name_214', 'email': 'adroh.com',
            'department': 'Department_214', 'designation': 'Designation_214'},
        {'name': 'Name_215', 'email': 'adsd.org',
            'department': 'Department_215', 'designation': 'Designation_215'},
        {'name': 'Name_216', 'email': 'adubiz.info',
            'department': 'Department_216', 'designation': 'Designation_216'},
        {'name': 'Name_217', 'email': 'advantagewe.us',
            'department': 'Department_217', 'designation': 'Designation_217'},
        {'name': 'Name_218', 'email': 'advantimo.com',
            'department': 'Department_218', 'designation': 'Designation_218'},
        {'name': 'Name_219', 'email': 'adventurewe.us',
            'department': 'Department_219', 'designation': 'Designation_219'},
        {'name': 'Name_220', 'email': 'adventwe.us',
            'department': 'Department_220', 'designation': 'Designation_220'},
        {'name': 'Name_221', 'email': 'advisorwe.us',
            'department': 'Department_221', 'designation': 'Designation_221'},
        {'name': 'Name_222', 'email': 'advocatewe.us',
            'department': 'Department_222', 'designation': 'Designation_222'},
        {'name': 'Name_223', 'email': 'adwaterandstir.com',
            'department': 'Department_223', 'designation': 'Designation_223'},
        {'name': 'Name_224', 'email': 'aegde.com',
            'department': 'Department_224', 'designation': 'Designation_224'},
        {'name': 'Name_225', 'email': 'aegia.net',
            'department': 'Department_225', 'designation': 'Designation_225'},
        {'name': 'Name_226', 'email': 'aegiscorp.net',
            'department': 'Department_226', 'designation': 'Designation_226'},
        {'name': 'Name_227', 'email': 'aegiswe.us',
            'department': 'Department_227', 'designation': 'Designation_227'},
        {'name': 'Name_228', 'email': 'aelo.es',
            'department': 'Department_228', 'designation': 'Designation_228'},
        {'name': 'Name_229', 'email': 'aeonpsi.com',
            'department': 'Department_229', 'designation': 'Designation_229'},
        {'name': 'Name_230', 'email': 'afarek.com',
            'department': 'Department_230', 'designation': 'Designation_230'},
        {'name': 'Name_231', 'email': 'affiliate-nebenjob.info',
            'department': 'Department_231', 'designation': 'Designation_231'},
        {'name': 'Name_232', 'email': 'affiliatedwe.us',
            'department': 'Department_232', 'designation': 'Designation_232'},
        {'name': 'Name_233', 'email': 'affilikingz.de',
            'department': 'Department_233', 'designation': 'Designation_233'},
        {'name': 'Name_234', 'email': 'affinitywe.us',
            'department': 'Department_234', 'designation': 'Designation_234'},
        {'name': 'Name_235', 'email': 'affluentwe.us',
            'department': 'Department_235', 'designation': 'Designation_235'},
        {'name': 'Name_236', 'email': 'affordablewe.us',
            'department': 'Department_236', 'designation': 'Designation_236'},
        {'name': 'Name_237', 'email': 'afrobacon.com',
            'department': 'Department_237', 'designation': 'Designation_237'},
        {'name': 'Name_238', 'email': 'afterhourswe.us',
            'department': 'Department_238', 'designation': 'Designation_238'},
        {'name': 'Name_239', 'email': 'agedmail.com',
            'department': 'Department_239', 'designation': 'Designation_239'},
        {'name': 'Name_240', 'email': 'agendawe.us',
            'department': 'Department_240', 'designation': 'Designation_240'},
        {'name': 'Name_241', 'email': 'agger.ro',
            'department': 'Department_241', 'designation': 'Designation_241'},
        {'name': 'Name_242', 'email': 'agilewe.us',
            'department': 'Department_242', 'designation': 'Designation_242'},
        {'name': 'Name_243', 'email': 'agorawe.us',
            'department': 'Department_243', 'designation': 'Designation_243'},
        {'name': 'Name_244', 'email': 'agtx.net',
            'department': 'Department_244', 'designation': 'Designation_244'},
        {'name': 'Name_245', 'email': 'aheadwe.us',
            'department': 'Department_245', 'designation': 'Designation_245'},
        {'name': 'Name_246', 'email': 'ahem.email',
            'department': 'Department_246', 'designation': 'Designation_246'},
        {'name': 'Name_247', 'email': 'ahk.jp',
            'department': 'Department_247', 'designation': 'Designation_247'},
        {'name': 'Name_248', 'email': 'ahmedkhlef.com',
            'department': 'Department_248', 'designation': 'Designation_248'},
        {'name': 'Name_249', 'email': 'aiafhg.com',
            'department': 'Department_249', 'designation': 'Designation_249'},
        {'name': 'Name_250', 'email': 'air2token.com',
            'department': 'Department_250', 'designation': 'Designation_250'},
        {'name': 'Name_251', 'email': 'airmailbox.website',
            'department': 'Department_251', 'designation': 'Designation_251'},
        {'name': 'Name_252', 'email': 'airsi.de',
            'department': 'Department_252', 'designation': 'Designation_252'},
        {'name': 'Name_253', 'email': 'ajaxapp.net',
            'department': 'Department_253', 'designation': 'Designation_253'},
        {'name': 'Name_254', 'email': 'akapost.com',
            'department': 'Department_254', 'designation': 'Designation_254'},
        {'name': 'Name_255', 'email': 'akerd.com',
            'department': 'Department_255', 'designation': 'Designation_255'},
        {'name': 'Name_256', 'email': 'akgq701.com',
            'department': 'Department_256', 'designation': 'Designation_256'},
        {'name': 'Name_257', 'email': 'al-qaeda.us',
            'department': 'Department_257', 'designation': 'Designation_257'},
        {'name': 'Name_258', 'email': 'albionwe.us',
            'department': 'Department_258', 'designation': 'Designation_258'},
        {'name': 'Name_259', 'email': 'alchemywe.us',
            'department': 'Department_259', 'designation': 'Designation_259'},
        {'name': 'Name_260', 'email': 'aleeas.com',
            'department': 'Department_260', 'designation': 'Designation_260'},
        {'name': 'Name_261', 'email': 'alfaceti.com',
            'department': 'Department_261', 'designation': 'Designation_261'},
        {'name': 'Name_262', 'email': 'aliaswe.us',
            'department': 'Department_262', 'designation': 'Designation_262'},
        {'name': 'Name_263', 'email': 'alienware13.com',
            'department': 'Department_263', 'designation': 'Designation_263'},
        {'name': 'Name_264', 'email': 'aligamel.com',
            'department': 'Department_264', 'designation': 'Designation_264'},
        {'name': 'Name_265', 'email': 'alisongamel.com',
            'department': 'Department_265', 'designation': 'Designation_265'},
        {'name': 'Name_266', 'email': 'alivance.com',
            'department': 'Department_266', 'designation': 'Designation_266'},
        {'name': 'Name_267', 'email': 'alivewe.us',
            'department': 'Department_267', 'designation': 'Designation_267'},
        {'name': 'Name_268', 'email': 'all-cats.ru',
            'department': 'Department_268', 'designation': 'Designation_268'},
        {'name': 'Name_269', 'email': 'allaccesswe.us',
            'department': 'Department_269', 'designation': 'Designation_269'},
        {'name': 'Name_270', 'email': 'allamericanwe.us',
            'department': 'Department_270', 'designation': 'Designation_270'},
        {'name': 'Name_271', 'email': 'allaroundwe.us',
            'department': 'Department_271', 'designation': 'Designation_271'},
        {'name': 'Name_272', 'email': 'alldirectbuy.com',
            'department': 'Department_272', 'designation': 'Designation_272'},
        {'name': 'Name_273', 'email': 'allegiancewe.us',
            'department': 'Department_273', 'designation': 'Designation_273'},
        {'name': 'Name_274', 'email': 'allegrowe.us',
            'department': 'Department_274', 'designation': 'Designation_274'},
        {'name': 'Name_275', 'email': 'allemojikeyboard.com',
            'department': 'Department_275', 'designation': 'Designation_275'},
        {'name': 'Name_276', 'email': 'allgoodwe.us',
            'department': 'Department_276', 'designation': 'Designation_276'},
        {'name': 'Name_277', 'email': 'alliancewe.us',
            'department': 'Department_277', 'designation': 'Designation_277'},
        {'name': 'Name_278', 'email': 'allinonewe.us',
            'department': 'Department_278', 'designation': 'Designation_278'},
        {'name': 'Name_279', 'email': 'allofthem.net',
            'department': 'Department_279', 'designation': 'Designation_279'},
        {'name': 'Name_280', 'email': 'alloutwe.us',
            'department': 'Department_280', 'designation': 'Designation_280'},
        {'name': 'Name_281', 'email': 'allowed.org',
            'department': 'Department_281', 'designation': 'Designation_281'},
        {'name': 'Name_282', 'email': 'alloywe.us',
            'department': 'Department_282', 'designation': 'Designation_282'},
        {'name': 'Name_283', 'email': 'allprowe.us',
            'department': 'Department_283', 'designation': 'Designation_283'},
        {'name': 'Name_284', 'email': 'allseasonswe.us',
            'department': 'Department_284', 'designation': 'Designation_284'},
        {'name': 'Name_285', 'email': 'allstarwe.us',
            'department': 'Department_285', 'designation': 'Designation_285'},
        {'name': 'Name_286', 'email': 'allthegoodnamesaretaken.org',
            'department': 'Department_286', 'designation': 'Designation_286'},
        {'name': 'Name_287', 'email': 'allurewe.us',
            'department': 'Department_287', 'designation': 'Designation_287'},
        {'name': 'Name_288', 'email': 'almondwe.us',
            'department': 'Department_288', 'designation': 'Designation_288'},
        {'name': 'Name_289', 'email': 'alph.wtf',
            'department': 'Department_289', 'designation': 'Designation_289'},
        {'name': 'Name_290', 'email': 'alpha-web.net',
            'department': 'Department_290', 'designation': 'Designation_290'},
        {'name': 'Name_291', 'email': 'alphaomegawe.us',
            'department': 'Department_291', 'designation': 'Designation_291'},
        {'name': 'Name_292', 'email': 'alpinewe.us',
            'department': 'Department_292', 'designation': 'Designation_292'},
        {'name': 'Name_293', 'email': 'altairwe.us',
            'department': 'Department_293', 'designation': 'Designation_293'},
        {'name': 'Name_294', 'email': 'altitudewe.us',
            'department': 'Department_294', 'designation': 'Designation_294'},
        {'name': 'Name_295', 'email': 'altuswe.us',
            'department': 'Department_295', 'designation': 'Designation_295'},
        {'name': 'Name_296', 'email': 'ama-trade.de',
            'department': 'Department_296', 'designation': 'Designation_296'},
        {'name': 'Name_297', 'email': 'ama-trans.de',
            'department': 'Department_297', 'designation': 'Designation_297'},
        {'name': 'Name_298', 'email': 'amadeuswe.us',
            'department': 'Department_298', 'designation': 'Designation_298'},
        {'name': 'Name_299', 'email': 'amail.club',
            'department': 'Department_299', 'designation': 'Designation_299'},
        {'name': 'Name_300', 'email': 'amail.com',
            'department': 'Department_300', 'designation': 'Designation_300'},
        {'name': 'Name_301', 'email': 'amail1.com',
            'department': 'Department_301', 'designation': 'Designation_301'},
        {'name': 'Name_302', 'email': 'amail4.me',
            'department': 'Department_302', 'designation': 'Designation_302'},
        {'name': 'Name_303', 'email': 'amazon-aws.org',
            'department': 'Department_303', 'designation': 'Designation_303'},
        {'name': 'Name_304', 'email': 'amberwe.us',
            'department': 'Department_304', 'designation': 'Designation_304'},
        {'name': 'Name_305', 'email': 'ambiancewe.us',
            'department': 'Department_305', 'designation': 'Designation_305'},
        {'name': 'Name_306', 'email': 'ambitiouswe.us',
            'department': 'Department_306', 'designation': 'Designation_306'},
        {'name': 'Name_307', 'email': 'amelabs.com',
            'department': 'Department_307', 'designation': 'Designation_307'},
        {'name': 'Name_308', 'email': 'americanawe.us',
            'department': 'Department_308', 'designation': 'Designation_308'},
        {'name': 'Name_309', 'email': 'americasbestwe.us',
            'department': 'Department_309', 'designation': 'Designation_309'},
        {'name': 'Name_310', 'email': 'americaswe.us',
            'department': 'Department_310', 'designation': 'Designation_310'},
        {'name': 'Name_311', 'email': 'amicuswe.us',
            'department': 'Department_311', 'designation': 'Designation_311'},
        {'name': 'Name_312', 'email': 'amilegit.com',
            'department': 'Department_312', 'designation': 'Designation_312'},
        {'name': 'Name_313', 'email': 'amiri.net',
            'department': 'Department_313', 'designation': 'Designation_313'},
        {'name': 'Name_314', 'email': 'amiriindustries.com',
            'department': 'Department_314', 'designation': 'Designation_314'},
        {'name': 'Name_315', 'email': 'amplewe.us',
            'department': 'Department_315', 'designation': 'Designation_315'},
        {'name': 'Name_316', 'email': 'amplifiedwe.us',
            'department': 'Department_316', 'designation': 'Designation_316'},
        {'name': 'Name_317', 'email': 'amplifywe.us',
            'department': 'Department_317', 'designation': 'Designation_317'},
        {'name': 'Name_318', 'email': 'ampsylike.com',
            'department': 'Department_318', 'designation': 'Designation_318'},
        {'name': 'Name_319', 'email': 'analogwe.us',
            'department': 'Department_319', 'designation': 'Designation_319'},
        {'name': 'Name_320', 'email': 'analysiswe.us',
            'department': 'Department_320', 'designation': 'Designation_320'},
        {'name': 'Name_321', 'email': 'analyticalwe.us',
            'department': 'Department_321', 'designation': 'Designation_321'},
        {'name': 'Name_322', 'email': 'analyticswe.us',
            'department': 'Department_322', 'designation': 'Designation_322'},
        {'name': 'Name_323', 'email': 'analyticwe.us',
            'department': 'Department_323', 'designation': 'Designation_323'},
        {'name': 'Name_324', 'email': 'anappfor.com',
            'department': 'Department_324', 'designation': 'Designation_324'},
        {'name': 'Name_325', 'email': 'anappthat.com',
            'department': 'Department_325', 'designation': 'Designation_325'},
        {'name': 'Name_326', 'email': 'andreihusanu.ro',
            'department': 'Department_326', 'designation': 'Designation_326'},
        {'name': 'Name_327', 'email': 'andthen.us',
            'department': 'Department_327', 'designation': 'Designation_327'},
        {'name': 'Name_328', 'email': 'animesos.com',
            'department': 'Department_328', 'designation': 'Designation_328'},
        {'name': 'Name_329', 'email': 'anit.ro',
            'department': 'Department_329', 'designation': 'Designation_329'},
        {'name': 'Name_330', 'email': 'ano-mail.net',
            'department': 'Department_330', 'designation': 'Designation_330'},
        {'name': 'Name_331', 'email': 'anon-mail.de',
            'department': 'Department_331', 'designation': 'Designation_331'},
        {'name': 'Name_332', 'email': 'anonaddy.com',
            'department': 'Department_332', 'designation': 'Designation_332'},
        {'name': 'Name_333', 'email': 'anonbox.net',
            'department': 'Department_333', 'designation': 'Designation_333'},
        {'name': 'Name_334', 'email': 'anonmail.top',
            'department': 'Department_334', 'designation': 'Designation_334'},
        {'name': 'Name_335', 'email': 'anonmails.de',
            'department': 'Department_335', 'designation': 'Designation_335'},
        {'name': 'Name_336', 'email': 'anonymail.dk',
            'department': 'Department_336', 'designation': 'Designation_336'},
        {'name': 'Name_337', 'email': 'anonymbox.com',
            'department': 'Department_337', 'designation': 'Designation_337'},
        {'name': 'Name_338', 'email': 'anonymized.org',
            'department': 'Department_338', 'designation': 'Designation_338'},
        {'name': 'Name_339', 'email': 'anonymousness.com',
            'department': 'Department_339', 'designation': 'Designation_339'},
        {'name': 'Name_340', 'email': 'anotherdomaincyka.tk',
            'department': 'Department_340', 'designation': 'Designation_340'},
        {'name': 'Name_341', 'email': 'ansibleemail.com',
            'department': 'Department_341', 'designation': 'Designation_341'},
        {'name': 'Name_342', 'email': 'anthony-junkmail.com',
            'department': 'Department_342', 'designation': 'Designation_342'},
        {'name': 'Name_343', 'email': 'antireg.com',
            'department': 'Department_343', 'designation': 'Designation_343'},
        {'name': 'Name_344', 'email': 'antireg.ru',
            'department': 'Department_344', 'designation': 'Designation_344'},
        {'name': 'Name_345', 'email': 'antispam.de',
            'department': 'Department_345', 'designation': 'Designation_345'},
        {'name': 'Name_346', 'email': 'antispam24.de',
            'department': 'Department_346', 'designation': 'Designation_346'},
        {'name': 'Name_347', 'email': 'antispammail.de',
            'department': 'Department_347', 'designation': 'Designation_347'},
        {'name': 'Name_348', 'email': 'anyalias.com',
            'department': 'Department_348', 'designation': 'Designation_348'},
        {'name': 'Name_349', 'email': 'aoeuhtns.com',
            'department': 'Department_349', 'designation': 'Designation_349'},
        {'name': 'Name_350', 'email': 'apfelkorps.de',
            'department': 'Department_350', 'designation': 'Designation_350'},
        {'name': 'Name_351', 'email': 'aphlog.com',
            'department': 'Department_351', 'designation': 'Designation_351'},
        {'name': 'Name_352', 'email': 'apkmd.com',
            'department': 'Department_352', 'designation': 'Designation_352'},
        {'name': 'Name_353', 'email': 'appc.se',
            'department': 'Department_353', 'designation': 'Designation_353'},
        {'name': 'Name_354', 'email': 'appinventor.nl',
            'department': 'Department_354', 'designation': 'Designation_354'},
        {'name': 'Name_355', 'email': 'appixie.com',
            'department': 'Department_355', 'designation': 'Designation_355'},
        {'name': 'Name_356', 'email': 'apps.dj',
            'department': 'Department_356', 'designation': 'Designation_356'},
        {'name': 'Name_357', 'email': 'appzily.com',
            'department': 'Department_357', 'designation': 'Designation_357'},
        {'name': 'Name_358', 'email': 'arduino.hk',
            'department': 'Department_358', 'designation': 'Designation_358'},
        {'name': 'Name_359', 'email': 'ariaz.jetzt',
            'department': 'Department_359', 'designation': 'Designation_359'},
        {'name': 'Name_360', 'email': 'armyspy.com',
            'department': 'Department_360', 'designation': 'Designation_360'},
        {'name': 'Name_361', 'email': 'aron.us',
            'department': 'Department_361', 'designation': 'Designation_361'},
        {'name': 'Name_362', 'email': 'arroisijewellery.com',
            'department': 'Department_362', 'designation': 'Designation_362'},
        {'name': 'Name_363', 'email': 'art-en-ligne.pro',
            'department': 'Department_363', 'designation': 'Designation_363'},
        {'name': 'Name_364', 'email': 'artman-conception.com',
            'department': 'Department_364', 'designation': 'Designation_364'},
        {'name': 'Name_365', 'email': 'arur01.tk',
            'department': 'Department_365', 'designation': 'Designation_365'},
        {'name': 'Name_366', 'email': 'arurgitu.gq',
            'department': 'Department_366', 'designation': 'Designation_366'},
        {'name': 'Name_367', 'email': 'arvato-community.de',
            'department': 'Department_367', 'designation': 'Designation_367'},
        {'name': 'Name_368', 'email': 'aschenbrandt.net',
            'department': 'Department_368', 'designation': 'Designation_368'},
        {'name': 'Name_369', 'email': 'asdasd.nl',
            'department': 'Department_369', 'designation': 'Designation_369'},
        {'name': 'Name_370', 'email': 'asdasd.ru',
            'department': 'Department_370', 'designation': 'Designation_370'},
        {'name': 'Name_371', 'email': 'ashleyandrew.com',
            'department': 'Department_371', 'designation': 'Designation_371'},
        {'name': 'Name_372', 'email': 'ask-mail.com',
            'department': 'Department_372', 'designation': 'Designation_372'},
        {'name': 'Name_373', 'email': 'asorent.com',
            'department': 'Department_373', 'designation': 'Designation_373'},
        {'name': 'Name_374', 'email': 'ass.pp.ua',
            'department': 'Department_374', 'designation': 'Designation_374'},
        {'name': 'Name_375', 'email': 'astonut.tk',
            'department': 'Department_375', 'designation': 'Designation_375'},
        {'name': 'Name_376', 'email': 'astroempires.info',
            'department': 'Department_376', 'designation': 'Designation_376'},
        {'name': 'Name_377', 'email': 'asu.mx',
            'department': 'Department_377', 'designation': 'Designation_377'},
        {'name': 'Name_378', 'email': 'asu.su',
            'department': 'Department_378', 'designation': 'Designation_378'},
        {'name': 'Name_379', 'email': 'at.hm',
            'department': 'Department_379', 'designation': 'Designation_379'},
        {'name': 'Name_380', 'email': 'at0mik.org',
            'department': 'Department_380', 'designation': 'Designation_380'},
        {'name': 'Name_381', 'email': 'atnextmail.com',
            'department': 'Department_381', 'designation': 'Designation_381'},
        {'name': 'Name_382', 'email': 'attnetwork.com',
            'department': 'Department_382', 'designation': 'Designation_382'},
        {'name': 'Name_383', 'email': 'augmentationtechnology.com',
            'department': 'Department_383', 'designation': 'Designation_383'},
        {'name': 'Name_384', 'email': 'ausgefallen.info',
            'department': 'Department_384', 'designation': 'Designation_384'},
        {'name': 'Name_385', 'email': 'auti.st',
            'department': 'Department_385', 'designation': 'Designation_385'},
        {'name': 'Name_386', 'email': 'autorobotica.com',
            'department': 'Department_386', 'designation': 'Designation_386'},
        {'name': 'Name_387', 'email': 'autosouvenir39.ru',
            'department': 'Department_387', 'designation': 'Designation_387'},
        {'name': 'Name_388', 'email': 'autotwollow.com',
            'department': 'Department_388', 'designation': 'Designation_388'},
        {'name': 'Name_389', 'email': 'autowb.com',
            'department': 'Department_389', 'designation': 'Designation_389'},
        {'name': 'Name_390', 'email': 'aver.com',
            'department': 'Department_390', 'designation': 'Designation_390'},
        {'name': 'Name_391', 'email': 'averdov.com',
            'department': 'Department_391', 'designation': 'Designation_391'},
        {'name': 'Name_392', 'email': 'avia-tonic.fr',
            'department': 'Department_392', 'designation': 'Designation_392'},
        {'name': 'Name_393', 'email': 'avls.pt',
            'department': 'Department_393', 'designation': 'Designation_393'},
        {'name': 'Name_394', 'email': 'awatum.de',
            'department': 'Department_394', 'designation': 'Designation_394'},
        {'name': 'Name_395', 'email': 'awdrt.org',
            'department': 'Department_395', 'designation': 'Designation_395'},
        {'name': 'Name_396', 'email': 'awiki.org',
            'department': 'Department_396', 'designation': 'Designation_396'},
        {'name': 'Name_397', 'email': 'awsoo.com',
            'department': 'Department_397', 'designation': 'Designation_397'},
        {'name': 'Name_398', 'email': 'axiz.org',
            'department': 'Department_398', 'designation': 'Designation_398'},
        {'name': 'Name_399', 'email': 'axon7zte.com',
            'department': 'Department_399', 'designation': 'Designation_399'},
        {'name': 'Name_400', 'email': 'axsup.net',
            'department': 'Department_400', 'designation': 'Designation_400'},
        {'name': 'Name_401', 'email': 'ayakamail.cf',
            'department': 'Department_401', 'designation': 'Designation_401'},
        {'name': 'Name_402', 'email': 'azazazatashkent.tk',
            'department': 'Department_402', 'designation': 'Designation_402'},
        {'name': 'Name_403', 'email': 'azcomputerworks.com',
            'department': 'Department_403', 'designation': 'Designation_403'},
        {'name': 'Name_404', 'email': 'azmeil.tk',
            'department': 'Department_404', 'designation': 'Designation_404'},
        {'name': 'Name_405', 'email': 'azwev.site',
            'department': 'Department_405', 'designation': 'Designation_405'},
        {'name': 'Name_406', 'email': 'b1of96u.com',
            'department': 'Department_406', 'designation': 'Designation_406'},
        {'name': 'Name_407', 'email': 'b2bx.net',
            'department': 'Department_407', 'designation': 'Designation_407'},
        {'name': 'Name_408', 'email': 'b2cmail.de',
            'department': 'Department_408', 'designation': 'Designation_408'},
        {'name': 'Name_409', 'email': 'badgerland.eu',
            'department': 'Department_409', 'designation': 'Designation_409'},
        {'name': 'Name_410', 'email': 'badoop.com',
            'department': 'Department_410', 'designation': 'Designation_410'},
        {'name': 'Name_411', 'email': 'badpotato.tk',
            'department': 'Department_411', 'designation': 'Designation_411'},
        {'name': 'Name_412', 'email': 'balaket.com',
            'department': 'Department_412', 'designation': 'Designation_412'},
        {'name': 'Name_413', 'email': 'banit.club',
            'department': 'Department_413', 'designation': 'Designation_413'},
        {'name': 'Name_414', 'email': 'banit.me',
            'department': 'Department_414', 'designation': 'Designation_414'},
        {'name': 'Name_415', 'email': 'bank-opros1.ru',
            'department': 'Department_415', 'designation': 'Designation_415'},
        {'name': 'Name_416', 'email': 'bareed.ws',
            'department': 'Department_416', 'designation': 'Designation_416'},
        {'name': 'Name_417', 'email': 'barryogorman.com',
            'department': 'Department_417', 'designation': 'Designation_417'},
        {'name': 'Name_418', 'email': 'bartdevos.be',
            'department': 'Department_418', 'designation': 'Designation_418'},
        {'name': 'Name_419', 'email': 'basscode.org',
            'department': 'Department_419', 'designation': 'Designation_419'},
        {'name': 'Name_420', 'email': 'bauwerke-online.com',
            'department': 'Department_420', 'designation': 'Designation_420'},
        {'name': 'Name_421', 'email': 'bazaaboom.com',
            'department': 'Department_421', 'designation': 'Designation_421'},
        {'name': 'Name_422', 'email': 'bbbbyyzz.info',
            'department': 'Department_422', 'designation': 'Designation_422'},
        {'name': 'Name_423', 'email': 'bbhost.us',
            'department': 'Department_423', 'designation': 'Designation_423'},
        {'name': 'Name_424', 'email': 'bcaoo.com',
            'department': 'Department_424', 'designation': 'Designation_424'},
        {'name': 'Name_425', 'email': 'bcast.ws',
            'department': 'Department_425', 'designation': 'Designation_425'},
        {'name': 'Name_426', 'email': 'bcb.ro',
            'department': 'Department_426', 'designation': 'Designation_426'},
        {'name': 'Name_427', 'email': 'bccto.me',
            'department': 'Department_427', 'designation': 'Designation_427'},
        {'name': 'Name_428', 'email': 'bdmuzic.pw',
            'department': 'Department_428', 'designation': 'Designation_428'},
        {'name': 'Name_429', 'email': 'bearsarefuzzy.com',
            'department': 'Department_429', 'designation': 'Designation_429'},
        {'name': 'Name_430', 'email': 'beddly.com',
            'department': 'Department_430', 'designation': 'Designation_430'},
        {'name': 'Name_431', 'email': 'beefmilk.com',
            'department': 'Department_431', 'designation': 'Designation_431'},
        {'name': 'Name_432', 'email': 'belamail.org',
            'department': 'Department_432', 'designation': 'Designation_432'},
        {'name': 'Name_433', 'email': 'belljonestax.com',
            'department': 'Department_433', 'designation': 'Designation_433'},
        {'name': 'Name_434', 'email': 'beluckygame.com',
            'department': 'Department_434', 'designation': 'Designation_434'},
        {'name': 'Name_435', 'email': 'benipaula.org',
            'department': 'Department_435', 'designation': 'Designation_435'},
        {'name': 'Name_436', 'email': 'bepureme.com',
            'department': 'Department_436', 'designation': 'Designation_436'},
        {'name': 'Name_437', 'email': 'beribase.ru',
            'department': 'Department_437', 'designation': 'Designation_437'},
        {'name': 'Name_438', 'email': 'beribaza.ru',
            'department': 'Department_438', 'designation': 'Designation_438'},
        {'name': 'Name_439', 'email': 'berirabotay.ru',
            'department': 'Department_439', 'designation': 'Designation_439'},
        {'name': 'Name_440', 'email': 'best-john-boats.com',
            'department': 'Department_440', 'designation': 'Designation_440'},
        {'name': 'Name_441', 'email': 'bestchoiceusedcar.com',
            'department': 'Department_441', 'designation': 'Designation_441'},
        {'name': 'Name_442', 'email': 'bestlistbase.com',
            'department': 'Department_442', 'designation': 'Designation_442'},
        {'name': 'Name_443', 'email': 'bestoption25.club',
            'department': 'Department_443', 'designation': 'Designation_443'},
        {'name': 'Name_444', 'email': 'bestparadize.com',
            'department': 'Department_444', 'designation': 'Designation_444'},
        {'name': 'Name_445', 'email': 'bestsoundeffects.com',
            'department': 'Department_445', 'designation': 'Designation_445'},
        {'name': 'Name_446', 'email': 'besttempmail.com',
            'department': 'Department_446', 'designation': 'Designation_446'},
        {'name': 'Name_447', 'email': 'betr.co',
            'department': 'Department_447', 'designation': 'Designation_447'},
        {'name': 'Name_448', 'email': 'bgtmail.com',
            'department': 'Department_448', 'designation': 'Designation_448'},
        {'name': 'Name_449', 'email': 'bgx.ro',
            'department': 'Department_449', 'designation': 'Designation_449'},
        {'name': 'Name_450', 'email': 'bidourlnks.com',
            'department': 'Department_450', 'designation': 'Designation_450'},
        {'name': 'Name_451', 'email': 'big1.us',
            'department': 'Department_451', 'designation': 'Designation_451'},
        {'name': 'Name_452', 'email': 'bigprofessor.so',
            'department': 'Department_452', 'designation': 'Designation_452'},
        {'name': 'Name_453', 'email': 'bigstring.com',
            'department': 'Department_453', 'designation': 'Designation_453'},
        {'name': 'Name_454', 'email': 'bigwhoop.co.za',
            'department': 'Department_454', 'designation': 'Designation_454'},
        {'name': 'Name_455', 'email': 'bij.pl',
            'department': 'Department_455', 'designation': 'Designation_455'},
        {'name': 'Name_456', 'email': 'binka.me',
            'department': 'Department_456', 'designation': 'Designation_456'},
        {'name': 'Name_457', 'email': 'binkmail.com',
            'department': 'Department_457', 'designation': 'Designation_457'},
        {'name': 'Name_458', 'email': 'binnary.com',
            'department': 'Department_458', 'designation': 'Designation_458'},
        {'name': 'Name_459', 'email': 'bio-muesli.info',
            'department': 'Department_459', 'designation': 'Designation_459'},
        {'name': 'Name_460', 'email': 'bio-muesli.net',
            'department': 'Department_460', 'designation': 'Designation_460'},
        {'name': 'Name_461', 'email': 'bione.co',
            'department': 'Department_461', 'designation': 'Designation_461'},
        {'name': 'Name_462', 'email': 'bitwhites.top',
            'department': 'Department_462', 'designation': 'Designation_462'},
        {'name': 'Name_463', 'email': 'bitymails.us',
            'department': 'Department_463', 'designation': 'Designation_463'},
        {'name': 'Name_464', 'email': 'blackgoldagency.ru',
            'department': 'Department_464', 'designation': 'Designation_464'},
        {'name': 'Name_465', 'email': 'blackmarket.to',
            'department': 'Department_465', 'designation': 'Designation_465'},
        {'name': 'Name_466', 'email': 'bladesmail.net',
            'department': 'Department_466', 'designation': 'Designation_466'},
        {'name': 'Name_467', 'email': 'blip.ch',
            'department': 'Department_467', 'designation': 'Designation_467'},
        {'name': 'Name_468', 'email': 'blnkt.net',
            'department': 'Department_468', 'designation': 'Designation_468'},
        {'name': 'Name_469', 'email': 'block521.com',
            'department': 'Department_469', 'designation': 'Designation_469'},
        {'name': 'Name_470', 'email': 'blogmyway.org',
            'department': 'Department_470', 'designation': 'Designation_470'},
        {'name': 'Name_471', 'email': 'blogos.net',
            'department': 'Department_471', 'designation': 'Designation_471'},
        {'name': 'Name_472', 'email': 'blogspam.ro',
            'department': 'Department_472', 'designation': 'Designation_472'},
        {'name': 'Name_473', 'email': 'blondemorkin.com',
            'department': 'Department_473', 'designation': 'Designation_473'},
        {'name': 'Name_474', 'email': 'bluedumpling.info',
            'department': 'Department_474', 'designation': 'Designation_474'},
        {'name': 'Name_475', 'email': 'bluewerks.com',
            'department': 'Department_475', 'designation': 'Designation_475'},
        {'name': 'Name_476', 'email': 'bnote.com',
            'department': 'Department_476', 'designation': 'Designation_476'},
        {'name': 'Name_477', 'email': 'boatmail.us',
            'department': 'Department_477', 'designation': 'Designation_477'},
        {'name': 'Name_478', 'email': 'bobmail.info',
            'department': 'Department_478', 'designation': 'Designation_478'},
        {'name': 'Name_479', 'email': 'bobmurchison.com',
            'department': 'Department_479', 'designation': 'Designation_479'},
        {'name': 'Name_480', 'email': 'bofthew.com',
            'department': 'Department_480', 'designation': 'Designation_480'},
        {'name': 'Name_481', 'email': 'bonobo.email',
            'department': 'Department_481', 'designation': 'Designation_481'},
        {'name': 'Name_482', 'email': 'boofx.com',
            'department': 'Department_482', 'designation': 'Designation_482'},
        {'name': 'Name_483', 'email': 'bookthemmore.com',
            'department': 'Department_483', 'designation': 'Designation_483'},
        {'name': 'Name_484', 'email': 'bootybay.de',
            'department': 'Department_484', 'designation': 'Designation_484'},
        {'name': 'Name_485', 'email': 'borged.com',
            'department': 'Department_485', 'designation': 'Designation_485'},
        {'name': 'Name_486', 'email': 'borged.net',
            'department': 'Department_486', 'designation': 'Designation_486'},
        {'name': 'Name_487', 'email': 'borged.org',
            'department': 'Department_487', 'designation': 'Designation_487'},
        {'name': 'Name_488', 'email': 'bot.nu',
            'department': 'Department_488', 'designation': 'Designation_488'},
        {'name': 'Name_489', 'email': 'boun.cr',
            'department': 'Department_489', 'designation': 'Designation_489'},
        {'name': 'Name_490', 'email': 'bouncr.com',
            'department': 'Department_490', 'designation': 'Designation_490'},
        {'name': 'Name_491', 'email': 'boxformail.in',
            'department': 'Department_491', 'designation': 'Designation_491'},
        {'name': 'Name_492', 'email': 'boximail.com',
            'department': 'Department_492', 'designation': 'Designation_492'},
        {'name': 'Name_493', 'email': 'boxomail.live',
            'department': 'Department_493', 'designation': 'Designation_493'},
        {'name': 'Name_494', 'email': 'boxtemp.com.br',
            'department': 'Department_494', 'designation': 'Designation_494'},
        {'name': 'Name_495', 'email': 'bptfp.net',
            'department': 'Department_495', 'designation': 'Designation_495'},
        {'name': 'Name_496', 'email': 'brandallday.net',
            'department': 'Department_496', 'designation': 'Designation_496'},
        {'name': 'Name_497', 'email': 'brasx.org',
            'department': 'Department_497', 'designation': 'Designation_497'},
        {'name': 'Name_498', 'email': 'breakthru.com',
            'department': 'Department_498', 'designation': 'Designation_498'},
        {'name': 'Name_499', 'email': 'brefmail.com',
            'department': 'Department_499', 'designation': 'Designation_499'},
        {'name': 'Name_500', 'email': 'brennendesreich.de',
            'department': 'Department_500', 'designation': 'Designation_500'},
        {'name': 'Name_501', 'email': 'briggsmarcus.com',
            'department': 'Department_501', 'designation': 'Designation_501'},
        {'name': 'Name_502', 'email': 'broadbandninja.com',
            'department': 'Department_502', 'designation': 'Designation_502'},
        {'name': 'Name_503', 'email': 'bsnow.net',
            'department': 'Department_503', 'designation': 'Designation_503'},
        {'name': 'Name_504', 'email': 'bspamfree.org',
            'department': 'Department_504', 'designation': 'Designation_504'},
        {'name': 'Name_505', 'email': 'bspooky.com',
            'department': 'Department_505', 'designation': 'Designation_505'},
        {'name': 'Name_506', 'email': 'bst-72.com',
            'department': 'Department_506', 'designation': 'Designation_506'},
        {'name': 'Name_507', 'email': 'btb-notes.com',
            'department': 'Department_507', 'designation': 'Designation_507'},
        {'name': 'Name_508', 'email': 'btc.email',
            'department': 'Department_508', 'designation': 'Designation_508'},
        {'name': 'Name_509', 'email': 'btcmail.pw',
            'department': 'Department_509', 'designation': 'Designation_509'},
        {'name': 'Name_510', 'email': 'btcmod.com',
            'department': 'Department_510', 'designation': 'Designation_510'},
        {'name': 'Name_511', 'email': 'btizet.pl',
            'department': 'Department_511', 'designation': 'Designation_511'},
        {'name': 'Name_512', 'email': 'buccalmassage.ru',
            'department': 'Department_512', 'designation': 'Designation_512'},
        {'name': 'Name_513', 'email': 'budaya-tionghoa.com',
            'department': 'Department_513', 'designation': 'Designation_513'},
        {'name': 'Name_514', 'email': 'budayationghoa.com',
            'department': 'Department_514', 'designation': 'Designation_514'},
        {'name': 'Name_515', 'email': 'buffemail.com',
            'department': 'Department_515', 'designation': 'Designation_515'},
        {'name': 'Name_516', 'email': 'bugmenever.com',
            'department': 'Department_516', 'designation': 'Designation_516'},
        {'name': 'Name_517', 'email': 'bugmenot.com',
            'department': 'Department_517', 'designation': 'Designation_517'},
        {'name': 'Name_518', 'email': 'bulrushpress.com',
            'department': 'Department_518', 'designation': 'Designation_518'},
        {'name': 'Name_519', 'email': 'bum.net',
            'department': 'Department_519', 'designation': 'Designation_519'},
        {'name': 'Name_520', 'email': 'bumpymail.com',
            'department': 'Department_520', 'designation': 'Designation_520'},
        {'name': 'Name_521', 'email': 'bunchofidiots.com',
            'department': 'Department_521', 'designation': 'Designation_521'},
        {'name': 'Name_522', 'email': 'bund.us',
            'department': 'Department_522', 'designation': 'Designation_522'},
        {'name': 'Name_523', 'email': 'bundes-li.ga',
            'department': 'Department_523', 'designation': 'Designation_523'},
        {'name': 'Name_524', 'email': 'bunsenhoneydew.com',
            'department': 'Department_524', 'designation': 'Designation_524'},
        {'name': 'Name_525', 'email': 'burnermail.com',
            'department': 'Department_525', 'designation': 'Designation_525'},
        {'name': 'Name_526', 'email': 'burnthespam.info',
            'department': 'Department_526', 'designation': 'Designation_526'},
        {'name': 'Name_527', 'email': 'burstmail.info',
            'department': 'Department_527', 'designation': 'Designation_527'},
        {'name': 'Name_528', 'email': 'businessbackend.com',
            'department': 'Department_528', 'designation': 'Designation_528'},
        {'name': 'Name_529', 'email': 'businesssuccessislifesuccess.com',
            'department': 'Department_529', 'designation': 'Designation_529'},
        {'name': 'Name_530', 'email': 'buspad.org',
            'department': 'Department_530', 'designation': 'Designation_530'},
        {'name': 'Name_531', 'email': 'bussitussi.com',
            'department': 'Department_531', 'designation': 'Designation_531'},
        {'name': 'Name_532', 'email': 'buy-blog.com',
            'department': 'Department_532', 'designation': 'Designation_532'},
        {'name': 'Name_533', 'email': 'buymoreplays.com',
            'department': 'Department_533', 'designation': 'Designation_533'},
        {'name': 'Name_534', 'email': 'buyordie.info',
            'department': 'Department_534', 'designation': 'Designation_534'},
        {'name': 'Name_535', 'email': 'buyusdomain.com',
            'department': 'Department_535', 'designation': 'Designation_535'},
        {'name': 'Name_536', 'email': 'buyusedlibrarybooks.org',
            'department': 'Department_536', 'designation': 'Designation_536'},
        {'name': 'Name_537', 'email': 'buzzcluby.com',
            'department': 'Department_537', 'designation': 'Designation_537'},
        {'name': 'Name_538', 'email': 'byebyemail.com',
            'department': 'Department_538', 'designation': 'Designation_538'},
        {'name': 'Name_539', 'email': 'byespm.com',
            'department': 'Department_539', 'designation': 'Designation_539'},
        {'name': 'Name_540', 'email': 'bylup.com',
            'department': 'Department_540', 'designation': 'Designation_540'},
        {'name': 'Name_541', 'email': 'byom.de',
            'department': 'Department_541', 'designation': 'Designation_541'},
        {'name': 'Name_542', 'email': 'c51vsgq.com',
            'department': 'Department_542', 'designation': 'Designation_542'},
        {'name': 'Name_543', 'email': 'cachedot.net',
            'department': 'Department_543', 'designation': 'Designation_543'},
        {'name': 'Name_544', 'email': 'californiafitnessdeals.com',
            'department': 'Department_544', 'designation': 'Designation_544'},
        {'name': 'Name_545', 'email': 'caltiger.net.in ',
            'department': 'Department_545', 'designation': 'Designation_545'},
        {'name': 'Name_546', 'email': 'cam4you.cc',
            'department': 'Department_546', 'designation': 'Designation_546'},
        {'name': 'Name_547', 'email': 'camping-grill.info',
            'department': 'Department_547', 'designation': 'Designation_547'},
        {'name': 'Name_548', 'email': 'candymail.de',
            'department': 'Department_548', 'designation': 'Designation_548'},
        {'name': 'Name_549', 'email': 'cane.pw',
            'department': 'Department_549', 'designation': 'Designation_549'},
        {'name': 'Name_550', 'email': 'capitalistdilemma.com',
            'department': 'Department_550', 'designation': 'Designation_550'},
        {'name': 'Name_551', 'email': 'car101.pro',
            'department': 'Department_551', 'designation': 'Designation_551'},
        {'name': 'Name_552', 'email': 'carbtc.net',
            'department': 'Department_552', 'designation': 'Designation_552'},
        {'name': 'Name_553', 'email': 'cars2.club',
            'department': 'Department_553', 'designation': 'Designation_553'},
        {'name': 'Name_554', 'email': 'carsencyclopedia.com',
            'department': 'Department_554', 'designation': 'Designation_554'},
        {'name': 'Name_555', 'email': 'cartelera.org',
            'department': 'Department_555', 'designation': 'Designation_555'},
        {'name': 'Name_556', 'email': 'caseedu.tk',
            'department': 'Department_556', 'designation': 'Designation_556'},
        {'name': 'Name_557', 'email': 'cashflow35.com',
            'department': 'Department_557', 'designation': 'Designation_557'},
        {'name': 'Name_558', 'email': 'casualdx.com',
            'department': 'Department_558', 'designation': 'Designation_558'},
        {'name': 'Name_559', 'email': 'cavi.mx',
            'department': 'Department_559', 'designation': 'Designation_559'},
        {'name': 'Name_560', 'email': 'cbair.com',
            'department': 'Department_560', 'designation': 'Designation_560'},
        {'name': 'Name_561', 'email': 'cbes.net',
            'department': 'Department_561', 'designation': 'Designation_561'},
        {'name': 'Name_562', 'email': 'cc.liamria',
            'department': 'Department_562', 'designation': 'Designation_562'},
        {'name': 'Name_563', 'email': 'ccmail.uk',
            'department': 'Department_563', 'designation': 'Designation_563'},
        {'name': 'Name_564', 'email': 'cdfaq.com',
            'department': 'Department_564', 'designation': 'Designation_564'},
        {'name': 'Name_565', 'email': 'cdpa.cc',
            'department': 'Department_565', 'designation': 'Designation_565'},
        {'name': 'Name_566', 'email': 'ceed.se',
            'department': 'Department_566', 'designation': 'Designation_566'},
        {'name': 'Name_567', 'email': 'cek.pm',
            'department': 'Department_567', 'designation': 'Designation_567'},
        {'name': 'Name_568', 'email': 'cellurl.com',
            'department': 'Department_568', 'designation': 'Designation_568'},
        {'name': 'Name_569', 'email': 'centermail.com',
            'department': 'Department_569', 'designation': 'Designation_569'},
        {'name': 'Name_570', 'email': 'centermail.net',
            'department': 'Department_570', 'designation': 'Designation_570'},
        {'name': 'Name_571', 'email': 'cetpass.com',
            'department': 'Department_571', 'designation': 'Designation_571'},
        {'name': 'Name_572', 'email': 'cfo2go.ro',
            'department': 'Department_572', 'designation': 'Designation_572'},
        {'name': 'Name_573', 'email': 'chacuo.net',
            'department': 'Department_573', 'designation': 'Designation_573'},
        {'name': 'Name_574', 'email': 'chaichuang.com',
            'department': 'Department_574', 'designation': 'Designation_574'},
        {'name': 'Name_575', 'email': 'chalupaurybnicku.cz',
            'department': 'Department_575', 'designation': 'Designation_575'},
        {'name': 'Name_576', 'email': 'chammy.info',
            'department': 'Department_576', 'designation': 'Designation_576'},
        {'name': 'Name_577', 'email': 'chasefreedomactivate.com',
            'department': 'Department_577', 'designation': 'Designation_577'},
        {'name': 'Name_578', 'email': 'chatich.com',
            'department': 'Department_578', 'designation': 'Designation_578'},
        {'name': 'Name_579', 'email': 'cheaphub.net',
            'department': 'Department_579', 'designation': 'Designation_579'},
        {'name': 'Name_580', 'email': 'cheatmail.de',
            'department': 'Department_580', 'designation': 'Designation_580'},
        {'name': 'Name_581', 'email': 'chenbot.email',
            'department': 'Department_581', 'designation': 'Designation_581'},
        {'name': 'Name_582', 'email': 'chibakenma.ml',
            'department': 'Department_582', 'designation': 'Designation_582'},
        {'name': 'Name_583', 'email': 'chickenkiller.com',
            'department': 'Department_583', 'designation': 'Designation_583'},
        {'name': 'Name_584', 'email': 'chielo.com',
            'department': 'Department_584', 'designation': 'Designation_584'},
        {'name': 'Name_585', 'email': 'childsavetrust.org',
            'department': 'Department_585', 'designation': 'Designation_585'},
        {'name': 'Name_586', 'email': 'chilkat.com',
            'department': 'Department_586', 'designation': 'Designation_586'},
        {'name': 'Name_587', 'email': 'chinamkm.com',
            'department': 'Department_587', 'designation': 'Designation_587'},
        {'name': 'Name_588', 'email': 'chithinh.com',
            'department': 'Department_588', 'designation': 'Designation_588'},
        {'name': 'Name_589', 'email': 'chitthi.in',
            'department': 'Department_589', 'designation': 'Designation_589'},
        {'name': 'Name_590', 'email': 'choco.la',
            'department': 'Department_590', 'designation': 'Designation_590'},
        {'name': 'Name_591', 'email': 'chogmail.com',
            'department': 'Department_591', 'designation': 'Designation_591'},
        {'name': 'Name_592', 'email': 'choicemail1.com',
            'department': 'Department_592', 'designation': 'Designation_592'},
        {'name': 'Name_593', 'email': 'chong-mail.com',
            'department': 'Department_593', 'designation': 'Designation_593'},
        {'name': 'Name_594', 'email': 'chong-mail.net',
            'department': 'Department_594', 'designation': 'Designation_594'},
        {'name': 'Name_595', 'email': 'chong-mail.org',
            'department': 'Department_595', 'designation': 'Designation_595'},
        {'name': 'Name_596', 'email': 'chumpstakingdumps.com',
            'department': 'Department_596', 'designation': 'Designation_596'},
        {'name': 'Name_597', 'email': 'cigar-auctions.com',
            'department': 'Department_597', 'designation': 'Designation_597'},
        {'name': 'Name_598', 'email': 'civx.org',
            'department': 'Department_598', 'designation': 'Designation_598'},
        {'name': 'Name_599', 'email': 'ckaazaza.tk',
            'department': 'Department_599', 'designation': 'Designation_599'},
        {'name': 'Name_600', 'email': 'ckiso.com',
            'department': 'Department_600', 'designation': 'Designation_600'},
        {'name': 'Name_601', 'email': 'cl-cl.org',
            'department': 'Department_601', 'designation': 'Designation_601'},
        {'name': 'Name_602', 'email': 'cl0ne.net',
            'department': 'Department_602', 'designation': 'Designation_602'},
        {'name': 'Name_603', 'email': 'claimab.com',
            'department': 'Department_603', 'designation': 'Designation_603'},
        {'name': 'Name_604', 'email': 'clandest.in',
            'department': 'Department_604', 'designation': 'Designation_604'},
        {'name': 'Name_605', 'email': 'classesmail.com',
            'department': 'Department_605', 'designation': 'Designation_605'},
        {'name': 'Name_606', 'email': 'clearwatermail.info',
            'department': 'Department_606', 'designation': 'Designation_606'},
        {'name': 'Name_607', 'email': 'click-email.com',
            'department': 'Department_607', 'designation': 'Designation_607'},
        {'name': 'Name_608', 'email': 'clickdeal.co',
            'department': 'Department_608', 'designation': 'Designation_608'},
        {'name': 'Name_609', 'email': 'clipmail.eu',
            'department': 'Department_609', 'designation': 'Designation_609'},
        {'name': 'Name_610', 'email': 'clixser.com',
            'department': 'Department_610', 'designation': 'Designation_610'},
        {'name': 'Name_611', 'email': 'clonemoi.tk',
            'department': 'Department_611', 'designation': 'Designation_611'},
        {'name': 'Name_612', 'email': 'cloud-mail.top',
            'department': 'Department_612', 'designation': 'Designation_612'},
        {'name': 'Name_613', 'email': 'cloudns.cx',
            'department': 'Department_613', 'designation': 'Designation_613'},
        {'name': 'Name_614', 'email': 'clrmail.com',
            'department': 'Department_614', 'designation': 'Designation_614'},
        {'name': 'Name_615', 'email': 'cmail.club',
            'department': 'Department_615', 'designation': 'Designation_615'},
        {'name': 'Name_616', 'email': 'cmail.com',
            'department': 'Department_616', 'designation': 'Designation_616'},
        {'name': 'Name_617', 'email': 'cmail.net',
            'department': 'Department_617', 'designation': 'Designation_617'},
        {'name': 'Name_618', 'email': 'cmail.org',
            'department': 'Department_618', 'designation': 'Designation_618'},
        {'name': 'Name_619', 'email': 'cnamed.com',
            'department': 'Department_619', 'designation': 'Designation_619'},
        {'name': 'Name_620', 'email': 'cndps.com',
            'department': 'Department_620', 'designation': 'Designation_620'},
        {'name': 'Name_621', 'email': 'cnew.ir',
            'department': 'Department_621', 'designation': 'Designation_621'},
        {'name': 'Name_622', 'email': 'cnmsg.net',
            'department': 'Department_622', 'designation': 'Designation_622'},
        {'name': 'Name_623', 'email': 'cnsds.de',
            'department': 'Department_623', 'designation': 'Designation_623'},
        {'name': 'Name_624', 'email': 'co.cc',
            'department': 'Department_624', 'designation': 'Designation_624'},
        {'name': 'Name_625', 'email': 'cobarekyo1.ml',
            'department': 'Department_625', 'designation': 'Designation_625'},
        {'name': 'Name_626', 'email': 'cocoro.uk',
            'department': 'Department_626', 'designation': 'Designation_626'},
        {'name': 'Name_627', 'email': 'cocovpn.com',
            'department': 'Department_627', 'designation': 'Designation_627'},
        {'name': 'Name_628', 'email': 'codeandscotch.com',
            'department': 'Department_628', 'designation': 'Designation_628'},
        {'name': 'Name_629', 'email': 'codivide.com',
            'department': 'Department_629', 'designation': 'Designation_629'},
        {'name': 'Name_630', 'email': 'coffeetimer24.com',
            'department': 'Department_630', 'designation': 'Designation_630'},
        {'name': 'Name_631', 'email': 'coieo.com',
            'department': 'Department_631', 'designation': 'Designation_631'},
        {'name': 'Name_632', 'email': 'coin-host.net',
            'department': 'Department_632', 'designation': 'Designation_632'},
        {'name': 'Name_633', 'email': 'coinlink.club',
            'department': 'Department_633', 'designation': 'Designation_633'},
        {'name': 'Name_634', 'email': 'coldemail.info',
            'department': 'Department_634', 'designation': 'Designation_634'},
        {'name': 'Name_635', 'email': 'compareshippingrates.org',
            'department': 'Department_635', 'designation': 'Designation_635'},
        {'name': 'Name_636', 'email': 'completegolfswing.com',
            'department': 'Department_636', 'designation': 'Designation_636'},
        {'name': 'Name_637', 'email': 'comwest.de',
            'department': 'Department_637', 'designation': 'Designation_637'},
        {'name': 'Name_638', 'email': 'conf.work',
            'department': 'Department_638', 'designation': 'Designation_638'},
        {'name': 'Name_639', 'email': 'consumerriot.com',
            'department': 'Department_639', 'designation': 'Designation_639'},
        {'name': 'Name_640', 'email': 'contbay.com',
            'department': 'Department_640', 'designation': 'Designation_640'},
        {'name': 'Name_641', 'email': 'cooh-2.site',
            'department': 'Department_641', 'designation': 'Designation_641'},
        {'name': 'Name_642', 'email': 'coolandwacky.us',
            'department': 'Department_642', 'designation': 'Designation_642'},
        {'name': 'Name_643', 'email': 'coolimpool.org',
            'department': 'Department_643', 'designation': 'Designation_643'},
        {'name': 'Name_644', 'email': 'coreclip.com',
            'department': 'Department_644', 'designation': 'Designation_644'},
        {'name': 'Name_645', 'email': 'cosmorph.com',
            'department': 'Department_645', 'designation': 'Designation_645'},
        {'name': 'Name_646', 'email': 'courrieltemporaire.com',
            'department': 'Department_646', 'designation': 'Designation_646'},
        {'name': 'Name_647', 'email': 'coza.ro',
            'department': 'Department_647', 'designation': 'Designation_647'},
        {'name': 'Name_648', 'email': 'crankhole.com',
            'department': 'Department_648', 'designation': 'Designation_648'},
        {'name': 'Name_649', 'email': 'crapmail.org',
            'department': 'Department_649', 'designation': 'Designation_649'},
        {'name': 'Name_650', 'email': 'crastination.de',
            'department': 'Department_650', 'designation': 'Designation_650'},
        {'name': 'Name_651', 'email': 'crazespaces.pw',
            'department': 'Department_651', 'designation': 'Designation_651'},
        {'name': 'Name_652', 'email': 'crazymailing.com',
            'department': 'Department_652', 'designation': 'Designation_652'},
        {'name': 'Name_653', 'email': 'cream.pink',
            'department': 'Department_653', 'designation': 'Designation_653'},
        {'name': 'Name_654', 'email': 'crepeau12.com',
            'department': 'Department_654', 'designation': 'Designation_654'},
        {'name': 'Name_655', 'email': 'cross-law.ga',
            'department': 'Department_655', 'designation': 'Designation_655'},
        {'name': 'Name_656', 'email': 'cross-law.gq',
            'department': 'Department_656', 'designation': 'Designation_656'},
        {'name': 'Name_657', 'email': 'crossmailjet.com',
            'department': 'Department_657', 'designation': 'Designation_657'},
        {'name': 'Name_658', 'email': 'crossroadsmail.com',
            'department': 'Department_658', 'designation': 'Designation_658'},
        {'name': 'Name_659', 'email': 'crunchcompass.com',
            'department': 'Department_659', 'designation': 'Designation_659'},
        {'name': 'Name_660', 'email': 'crusthost.com',
            'department': 'Department_660', 'designation': 'Designation_660'},
        {'name': 'Name_661', 'email': 'cs.email',
            'department': 'Department_661', 'designation': 'Designation_661'},
        {'name': 'Name_662', 'email': 'csh.ro',
            'department': 'Department_662', 'designation': 'Designation_662'},
        {'name': 'Name_663', 'email': 'cszbl.com',
            'department': 'Department_663', 'designation': 'Designation_663'},
        {'name': 'Name_664', 'email': 'ctmailing.us',
            'department': 'Department_664', 'designation': 'Designation_664'},
        {'name': 'Name_665', 'email': 'ctos.ch',
            'department': 'Department_665', 'designation': 'Designation_665'},
        {'name': 'Name_666', 'email': 'cu.cc',
            'department': 'Department_666', 'designation': 'Designation_666'},
        {'name': 'Name_667', 'email': 'cubiclink.com',
            'department': 'Department_667', 'designation': 'Designation_667'},
        {'name': 'Name_668', 'email': 'cuendita.com',
            'department': 'Department_668', 'designation': 'Designation_668'},
        {'name': 'Name_669', 'email': 'cuirushi.org',
            'department': 'Department_669', 'designation': 'Designation_669'},
        {'name': 'Name_670', 'email': 'cuoly.com',
            'department': 'Department_670', 'designation': 'Designation_670'},
        {'name': 'Name_671', 'email': 'cupbest.com',
            'department': 'Department_671', 'designation': 'Designation_671'},
        {'name': 'Name_672', 'email': 'curlhph.tk',
            'department': 'Department_672', 'designation': 'Designation_672'},
        {'name': 'Name_673', 'email': 'curryworld.de',
            'department': 'Department_673', 'designation': 'Designation_673'},
        {'name': 'Name_674', 'email': 'cust.in',
            'department': 'Department_674', 'designation': 'Designation_674'},
        {'name': 'Name_675', 'email': 'cutout.club',
            'department': 'Department_675', 'designation': 'Designation_675'},
        {'name': 'Name_676', 'email': 'cutradition.com',
            'department': 'Department_676', 'designation': 'Designation_676'},
        {'name': 'Name_677', 'email': 'cuvox.de',
            'department': 'Department_677', 'designation': 'Designation_677'},
        {'name': 'Name_678', 'email': 'cyber-innovation.club',
            'department': 'Department_678', 'designation': 'Designation_678'},
        {'name': 'Name_679', 'email': 'cyber-phone.eu',
            'department': 'Department_679', 'designation': 'Designation_679'},
        {'name': 'Name_680', 'email': 'cylab.org',
            'department': 'Department_680', 'designation': 'Designation_680'},
        {'name': 'Name_681', 'email': 'd1yun.com',
            'department': 'Department_681', 'designation': 'Designation_681'},
        {'name': 'Name_682', 'email': 'd3p.dk',
            'department': 'Department_682', 'designation': 'Designation_682'},
        {'name': 'Name_683', 'email': 'daabox.com',
            'department': 'Department_683', 'designation': 'Designation_683'},
        {'name': 'Name_684', 'email': 'dab.ro',
            'department': 'Department_684', 'designation': 'Designation_684'},
        {'name': 'Name_685', 'email': 'dacoolest.com',
            'department': 'Department_685', 'designation': 'Designation_685'},
        {'name': 'Name_686', 'email': 'daemsteam.com',
            'department': 'Department_686', 'designation': 'Designation_686'},
        {'name': 'Name_687', 'email': 'daibond.info',
            'department': 'Department_687', 'designation': 'Designation_687'},
        {'name': 'Name_688', 'email': 'daily-email.com',
            'department': 'Department_688', 'designation': 'Designation_688'},
        {'name': 'Name_689', 'email': 'daintly.com',
            'department': 'Department_689', 'designation': 'Designation_689'},
        {'name': 'Name_690', 'email': 'damai.webcam',
            'department': 'Department_690', 'designation': 'Designation_690'},
        {'name': 'Name_691', 'email': 'dammexe.net',
            'department': 'Department_691', 'designation': 'Designation_691'},
        {'name': 'Name_692', 'email': 'damnthespam.com',
            'department': 'Department_692', 'designation': 'Designation_692'},
        {'name': 'Name_693', 'email': 'dandikmail.com',
            'department': 'Department_693', 'designation': 'Designation_693'},
        {'name': 'Name_694', 'email': 'darkharvestfilms.com',
            'department': 'Department_694', 'designation': 'Designation_694'},
        {'name': 'Name_695', 'email': 'daryxfox.net',
            'department': 'Department_695', 'designation': 'Designation_695'},
        {'name': 'Name_696', 'email': 'dasdasdascyka.tk',
            'department': 'Department_696', 'designation': 'Designation_696'},
        {'name': 'Name_697', 'email': 'dash-pads.com',
            'department': 'Department_697', 'designation': 'Designation_697'},
        {'name': 'Name_698', 'email': 'dataarca.com',
            'department': 'Department_698', 'designation': 'Designation_698'},
        {'name': 'Name_699', 'email': 'datarca.com',
            'department': 'Department_699', 'designation': 'Designation_699'},
        {'name': 'Name_700', 'email': 'datazo.ca',
            'department': 'Department_700', 'designation': 'Designation_700'},
        {'name': 'Name_701', 'email': 'datenschutz.ru',
            'department': 'Department_701', 'designation': 'Designation_701'},
        {'name': 'Name_702', 'email': 'datum2.com',
            'department': 'Department_702', 'designation': 'Designation_702'},
        {'name': 'Name_703', 'email': 'davidkoh.net',
            'department': 'Department_703', 'designation': 'Designation_703'},
        {'name': 'Name_704', 'email': 'davidlcreative.com',
            'department': 'Department_704', 'designation': 'Designation_704'},
        {'name': 'Name_705', 'email': 'dawin.com',
            'department': 'Department_705', 'designation': 'Designation_705'},
        {'name': 'Name_706', 'email': 'daymail.life',
            'department': 'Department_706', 'designation': 'Designation_706'},
        {'name': 'Name_707', 'email': 'daymailonline.com',
            'department': 'Department_707', 'designation': 'Designation_707'},
        {'name': 'Name_708', 'email': 'dayrep.com',
            'department': 'Department_708', 'designation': 'Designation_708'},
        {'name': 'Name_709', 'email': 'dbunker.com',
            'department': 'Department_709', 'designation': 'Designation_709'},
        {'name': 'Name_710', 'email': 'dcemail.com',
            'department': 'Department_710', 'designation': 'Designation_710'},
        {'name': 'Name_711', 'email': 'ddcrew.com',
            'department': 'Department_711', 'designation': 'Designation_711'},
        {'name': 'Name_712', 'email': 'de-a.org',
            'department': 'Department_712', 'designation': 'Designation_712'},
        {'name': 'Name_713', 'email': 'dea-21olympic.com',
            'department': 'Department_713', 'designation': 'Designation_713'},
        {'name': 'Name_714', 'email': 'deadaddress.com',
            'department': 'Department_714', 'designation': 'Designation_714'},
        {'name': 'Name_715', 'email': 'deadchildren.org',
            'department': 'Department_715', 'designation': 'Designation_715'},
        {'name': 'Name_716', 'email': 'deadfake.cf',
            'department': 'Department_716', 'designation': 'Designation_716'},
        {'name': 'Name_717', 'email': 'deadfake.ga',
            'department': 'Department_717', 'designation': 'Designation_717'},
        {'name': 'Name_718', 'email': 'deadfake.ml',
            'department': 'Department_718', 'designation': 'Designation_718'},
        {'name': 'Name_719', 'email': 'deadfake.tk',
            'department': 'Department_719', 'designation': 'Designation_719'},
        {'name': 'Name_720', 'email': 'deadspam.com',
            'department': 'Department_720', 'designation': 'Designation_720'},
        {'name': 'Name_721', 'email': 'deagot.com',
            'department': 'Department_721', 'designation': 'Designation_721'},
        {'name': 'Name_722', 'email': 'dealja.com',
            'department': 'Department_722', 'designation': 'Designation_722'},
        {'name': 'Name_723', 'email': 'dealrek.com',
            'department': 'Department_723', 'designation': 'Designation_723'},
        {'name': 'Name_724', 'email': 'deekayen.us',
            'department': 'Department_724', 'designation': 'Designation_724'},
        {'name': 'Name_725', 'email': 'defomail.com',
            'department': 'Department_725', 'designation': 'Designation_725'},
        {'name': 'Name_726', 'email': 'degradedfun.net',
            'department': 'Department_726', 'designation': 'Designation_726'},
        {'name': 'Name_727', 'email': 'deinbox.com',
            'department': 'Department_727', 'designation': 'Designation_727'},
        {'name': 'Name_728', 'email': 'delayload.com',
            'department': 'Department_728', 'designation': 'Designation_728'},
        {'name': 'Name_729', 'email': 'delayload.net',
            'department': 'Department_729', 'designation': 'Designation_729'},
        {'name': 'Name_730', 'email': 'delikkt.de',
            'department': 'Department_730', 'designation': 'Designation_730'},
        {'name': 'Name_731', 'email': 'delivrmail.com',
            'department': 'Department_731', 'designation': 'Designation_731'},
        {'name': 'Name_732', 'email': 'demen.ml',
            'department': 'Department_732', 'designation': 'Designation_732'},
        {'name': 'Name_733', 'email': 'dengekibunko.ga',
            'department': 'Department_733', 'designation': 'Designation_733'},
        {'name': 'Name_734', 'email': 'dengekibunko.gq',
            'department': 'Department_734', 'designation': 'Designation_734'},
        {'name': 'Name_735', 'email': 'dengekibunko.ml',
            'department': 'Department_735', 'designation': 'Designation_735'},
        {'name': 'Name_736', 'email': 'der-kombi.de',
            'department': 'Department_736', 'designation': 'Designation_736'},
        {'name': 'Name_737', 'email': 'derkombi.de',
            'department': 'Department_737', 'designation': 'Designation_737'},
        {'name': 'Name_738', 'email': 'derluxuswagen.de',
            'department': 'Department_738', 'designation': 'Designation_738'},
        {'name': 'Name_739', 'email': 'desoz.com',
            'department': 'Department_739', 'designation': 'Designation_739'},
        {'name': 'Name_740', 'email': 'despam.it',
            'department': 'Department_740', 'designation': 'Designation_740'},
        {'name': 'Name_741', 'email': 'despammed.com',
            'department': 'Department_741', 'designation': 'Designation_741'},
        {'name': 'Name_742', 'email': 'dev-null.cf',
            'department': 'Department_742', 'designation': 'Designation_742'},
        {'name': 'Name_743', 'email': 'dev-null.ga',
            'department': 'Department_743', 'designation': 'Designation_743'},
        {'name': 'Name_744', 'email': 'dev-null.gq',
            'department': 'Department_744', 'designation': 'Designation_744'},
        {'name': 'Name_745', 'email': 'dev-null.ml',
            'department': 'Department_745', 'designation': 'Designation_745'},
        {'name': 'Name_746', 'email': 'devnullmail.com',
            'department': 'Department_746', 'designation': 'Designation_746'},
        {'name': 'Name_747', 'email': 'deyom.com',
            'department': 'Department_747', 'designation': 'Designation_747'},
        {'name': 'Name_748', 'email': 'deypo.com',
            'department': 'Department_748', 'designation': 'Designation_748'},
        {'name': 'Name_749', 'email': 'dharmatel.net',
            'department': 'Department_749', 'designation': 'Designation_749'},
        {'name': 'Name_750', 'email': 'dhm.ro',
            'department': 'Department_750', 'designation': 'Designation_750'},
        {'name': 'Name_751', 'email': 'dhy.cc',
            'department': 'Department_751', 'designation': 'Designation_751'},
        {'name': 'Name_752', 'email': 'dialogus.com',
            'department': 'Department_752', 'designation': 'Designation_752'},
        {'name': 'Name_753', 'email': 'diapaulpainting.com',
            'department': 'Department_753', 'designation': 'Designation_753'},
        {'name': 'Name_754', 'email': 'dicopto.com',
            'department': 'Department_754', 'designation': 'Designation_754'},
        {'name': 'Name_755', 'email': 'digdig.org',
            'department': 'Department_755', 'designation': 'Designation_755'},
        {'name': 'Name_756', 'email': 'digital-message.com',
            'department': 'Department_756', 'designation': 'Designation_756'},
        {'name': 'Name_757', 'email': 'digitalesbusiness.info',
            'department': 'Department_757', 'designation': 'Designation_757'},
        {'name': 'Name_758', 'email': 'digitalmail.info',
            'department': 'Department_758', 'designation': 'Designation_758'},
        {'name': 'Name_759', 'email': 'digitalmariachis.com',
            'department': 'Department_759', 'designation': 'Designation_759'},
        {'name': 'Name_760', 'email': 'digitalsanctuary.com',
            'department': 'Department_760', 'designation': 'Designation_760'},
        {'name': 'Name_761', 'email': 'dildosfromspace.com',
            'department': 'Department_761', 'designation': 'Designation_761'},
        {'name': 'Name_762', 'email': 'dim-coin.com',
            'department': 'Department_762', 'designation': 'Designation_762'},
        {'name': 'Name_763', 'email': 'dingbone.com',
            'department': 'Department_763', 'designation': 'Designation_763'},
        {'name': 'Name_764', 'email': 'diolang.com',
            'department': 'Department_764', 'designation': 'Designation_764'},
        {'name': 'Name_765', 'email': 'directmail24.net',
            'department': 'Department_765', 'designation': 'Designation_765'},
        {'name': 'Name_766', 'email': 'disaq.com',
            'department': 'Department_766', 'designation': 'Designation_766'},
        {'name': 'Name_767', 'email': 'disbox.net',
            'department': 'Department_767', 'designation': 'Designation_767'},
        {'name': 'Name_768', 'email': 'disbox.org',
            'department': 'Department_768', 'designation': 'Designation_768'},
        {'name': 'Name_769', 'email': 'discard.cf',
            'department': 'Department_769', 'designation': 'Designation_769'},
        {'name': 'Name_770', 'email': 'discard.email',
            'department': 'Department_770', 'designation': 'Designation_770'},
        {'name': 'Name_771', 'email': 'discard.ga',
            'department': 'Department_771', 'designation': 'Designation_771'},
        {'name': 'Name_772', 'email': 'discard.gq',
            'department': 'Department_772', 'designation': 'Designation_772'},
        {'name': 'Name_773', 'email': 'discard.ml',
            'department': 'Department_773', 'designation': 'Designation_773'},
        {'name': 'Name_774', 'email': 'discard.tk',
            'department': 'Department_774', 'designation': 'Designation_774'},
        {'name': 'Name_775', 'email': 'discardmail.com',
            'department': 'Department_775', 'designation': 'Designation_775'},
        {'name': 'Name_776', 'email': 'discardmail.de',
            'department': 'Department_776', 'designation': 'Designation_776'},
        {'name': 'Name_777', 'email': 'discos4.com',
            'department': 'Department_777', 'designation': 'Designation_777'},
        {'name': 'Name_778', 'email': 'disign-concept.eu',
            'department': 'Department_778', 'designation': 'Designation_778'},
        {'name': 'Name_779', 'email': 'disign-revelation.com',
            'department': 'Department_779', 'designation': 'Designation_779'},
        {'name': 'Name_780', 'email': 'dispo.in',
            'department': 'Department_780', 'designation': 'Designation_780'},
        {'name': 'Name_781', 'email': 'dispomail.eu',
            'department': 'Department_781', 'designation': 'Designation_781'},
        {'name': 'Name_782', 'email': 'disposable-e.ml',
            'department': 'Department_782', 'designation': 'Designation_782'},
        {'name': 'Name_783', 'email': 'disposable-email.ml',
            'department': 'Department_783', 'designation': 'Designation_783'},
        {'name': 'Name_784', 'email': 'disposable.cf',
            'department': 'Department_784', 'designation': 'Designation_784'},
        {'name': 'Name_785', 'email': 'disposable.ga',
            'department': 'Department_785', 'designation': 'Designation_785'},
        {'name': 'Name_786', 'email': 'disposable.ml',
            'department': 'Department_786', 'designation': 'Designation_786'},
        {'name': 'Name_787', 'email': 'disposable.site',
            'department': 'Department_787', 'designation': 'Designation_787'},
        {'name': 'Name_788', 'email': 'disposableaddress.com',
            'department': 'Department_788', 'designation': 'Designation_788'},
        {'name': 'Name_789', 'email': 'disposableemailaddresses.com',
            'department': 'Department_789', 'designation': 'Designation_789'},
        {'name': 'Name_790', 'email': 'disposableinbox.com',
            'department': 'Department_790', 'designation': 'Designation_790'},
        {'name': 'Name_791', 'email': 'disposablemails.com',
            'department': 'Department_791', 'designation': 'Designation_791'},
        {'name': 'Name_792', 'email': 'dispose.it',
            'department': 'Department_792', 'designation': 'Designation_792'},
        {'name': 'Name_793', 'email': 'disposeamail.com',
            'department': 'Department_793', 'designation': 'Designation_793'},
        {'name': 'Name_794', 'email': 'disposemail.com',
            'department': 'Department_794', 'designation': 'Designation_794'},
        {'name': 'Name_795', 'email': 'disposemymail.com',
            'department': 'Department_795', 'designation': 'Designation_795'},
        {'name': 'Name_796', 'email': 'dispostable.com',
            'department': 'Department_796', 'designation': 'Designation_796'},
        {'name': 'Name_797', 'email': 'divad.ga',
            'department': 'Department_797', 'designation': 'Designation_797'},
        {'name': 'Name_798', 'email': 'divermail.com',
            'department': 'Department_798', 'designation': 'Designation_798'},
        {'name': 'Name_799', 'email': 'divismail.ru',
            'department': 'Department_799', 'designation': 'Designation_799'},
        {'name': 'Name_800', 'email': 'diwaq.com',
            'department': 'Department_800', 'designation': 'Designation_800'},
        {'name': 'Name_801', 'email': 'dlemail.ru',
            'department': 'Department_801', 'designation': 'Designation_801'},
        {'name': 'Name_802', 'email': 'dmarc.ro',
            'department': 'Department_802', 'designation': 'Designation_802'},
        {'name': 'Name_803', 'email': 'dndent.com',
            'department': 'Department_803', 'designation': 'Designation_803'},
        {'name': 'Name_804', 'email': 'dnses.ro',
            'department': 'Department_804', 'designation': 'Designation_804'},
        {'name': 'Name_805', 'email': 'doanart.com',
            'department': 'Department_805', 'designation': 'Designation_805'},
        {'name': 'Name_806', 'email': 'dob.jp',
            'department': 'Department_806', 'designation': 'Designation_806'},
        {'name': 'Name_807', 'email': 'dodgeit.com',
            'department': 'Department_807', 'designation': 'Designation_807'},
        {'name': 'Name_808', 'email': 'dodgemail.de',
            'department': 'Department_808', 'designation': 'Designation_808'},
        {'name': 'Name_809', 'email': 'dodgit.com',
            'department': 'Department_809', 'designation': 'Designation_809'},
        {'name': 'Name_810', 'email': 'dodgit.org',
            'department': 'Department_810', 'designation': 'Designation_810'},
        {'name': 'Name_811', 'email': 'dodsi.com',
            'department': 'Department_811', 'designation': 'Designation_811'},
        {'name': 'Name_812', 'email': 'doiea.com',
            'department': 'Department_812', 'designation': 'Designation_812'},
        {'name': 'Name_813', 'email': 'dolphinnet.net',
            'department': 'Department_813', 'designation': 'Designation_813'},
        {'name': 'Name_814', 'email': 'domforfb1.tk',
            'department': 'Department_814', 'designation': 'Designation_814'},
        {'name': 'Name_815', 'email': 'domforfb18.tk',
            'department': 'Department_815', 'designation': 'Designation_815'},
        {'name': 'Name_816', 'email': 'domforfb19.tk',
            'department': 'Department_816', 'designation': 'Designation_816'},
        {'name': 'Name_817', 'email': 'domforfb2.tk',
            'department': 'Department_817', 'designation': 'Designation_817'},
        {'name': 'Name_818', 'email': 'domforfb23.tk',
            'department': 'Department_818', 'designation': 'Designation_818'},
        {'name': 'Name_819', 'email': 'domforfb27.tk',
            'department': 'Department_819', 'designation': 'Designation_819'},
        {'name': 'Name_820', 'email': 'domforfb29.tk',
            'department': 'Department_820', 'designation': 'Designation_820'},
        {'name': 'Name_821', 'email': 'domforfb3.tk',
            'department': 'Department_821', 'designation': 'Designation_821'},
        {'name': 'Name_822', 'email': 'domforfb4.tk',
            'department': 'Department_822', 'designation': 'Designation_822'},
        {'name': 'Name_823', 'email': 'domforfb5.tk',
            'department': 'Department_823', 'designation': 'Designation_823'},
        {'name': 'Name_824', 'email': 'domforfb6.tk',
            'department': 'Department_824', 'designation': 'Designation_824'},
        {'name': 'Name_825', 'email': 'domforfb7.tk',
            'department': 'Department_825', 'designation': 'Designation_825'},
        {'name': 'Name_826', 'email': 'domforfb8.tk',
            'department': 'Department_826', 'designation': 'Designation_826'},
        {'name': 'Name_827', 'email': 'domforfb9.tk',
            'department': 'Department_827', 'designation': 'Designation_827'},
        {'name': 'Name_828', 'email': 'domozmail.com',
            'department': 'Department_828', 'designation': 'Designation_828'},
        {'name': 'Name_829', 'email': 'donemail.ru',
            'department': 'Department_829', 'designation': 'Designation_829'},
        {'name': 'Name_830', 'email': 'dongqing365.com',
            'department': 'Department_830', 'designation': 'Designation_830'},
        {'name': 'Name_831', 'email': 'dontreg.com',
            'department': 'Department_831', 'designation': 'Designation_831'},
        {'name': 'Name_832', 'email': 'dontsendmespam.de',
            'department': 'Department_832', 'designation': 'Designation_832'},
        {'name': 'Name_833', 'email': 'doquier.tk',
            'department': 'Department_833', 'designation': 'Designation_833'},
        {'name': 'Name_834', 'email': 'dotman.de',
            'department': 'Department_834', 'designation': 'Designation_834'},
        {'name': 'Name_835', 'email': 'dotmsg.com',
            'department': 'Department_835', 'designation': 'Designation_835'},
        {'name': 'Name_836', 'email': 'dotslashrage.com',
            'department': 'Department_836', 'designation': 'Designation_836'},
        {'name': 'Name_837', 'email': 'doublemail.de',
            'department': 'Department_837', 'designation': 'Designation_837'},
        {'name': 'Name_838', 'email': 'douchelounge.com',
            'department': 'Department_838', 'designation': 'Designation_838'},
        {'name': 'Name_839', 'email': 'dozvon-spb.ru',
            'department': 'Department_839', 'designation': 'Designation_839'},
        {'name': 'Name_840', 'email': 'dp76.com',
            'department': 'Department_840', 'designation': 'Designation_840'},
        {'name': 'Name_841', 'email': 'dr69.site',
            'department': 'Department_841', 'designation': 'Designation_841'},
        {'name': 'Name_842', 'email': 'drdrb.com',
            'department': 'Department_842', 'designation': 'Designation_842'},
        {'name': 'Name_843', 'email': 'drdrb.net',
            'department': 'Department_843', 'designation': 'Designation_843'},
        {'name': 'Name_844', 'email': 'dred.ru',
            'department': 'Department_844', 'designation': 'Designation_844'},
        {'name': 'Name_845', 'email': 'drevo.si',
            'department': 'Department_845', 'designation': 'Designation_845'},
        {'name': 'Name_846', 'email': 'drivetagdev.com',
            'department': 'Department_846', 'designation': 'Designation_846'},
        {'name': 'Name_847', 'email': 'droolingfanboy.de',
            'department': 'Department_847', 'designation': 'Designation_847'},
        {'name': 'Name_848', 'email': 'dropcake.de',
            'department': 'Department_848', 'designation': 'Designation_848'},
        {'name': 'Name_849', 'email': 'dropjar.com',
            'department': 'Department_849', 'designation': 'Designation_849'},
        {'name': 'Name_850', 'email': 'droplar.com',
            'department': 'Department_850', 'designation': 'Designation_850'},
        {'name': 'Name_851', 'email': 'dropmail.me',
            'department': 'Department_851', 'designation': 'Designation_851'},
        {'name': 'Name_852', 'email': 'dsgvo.ru',
            'department': 'Department_852', 'designation': 'Designation_852'},
        {'name': 'Name_853', 'email': 'dsiay.com',
            'department': 'Department_853', 'designation': 'Designation_853'},
        {'name': 'Name_854', 'email': 'dspwebservices.com',
            'department': 'Department_854', 'designation': 'Designation_854'},
        {'name': 'Name_855', 'email': 'duam.net',
            'department': 'Department_855', 'designation': 'Designation_855'},
        {'name': 'Name_856', 'email': 'duck2.club',
            'department': 'Department_856', 'designation': 'Designation_856'},
        {'name': 'Name_857', 'email': 'dudmail.com',
            'department': 'Department_857', 'designation': 'Designation_857'},
        {'name': 'Name_858', 'email': 'duk33.com',
            'department': 'Department_858', 'designation': 'Designation_858'},
        {'name': 'Name_859', 'email': 'dukedish.com',
            'department': 'Department_859', 'designation': 'Designation_859'},
        {'name': 'Name_860', 'email': 'dump-email.info',
            'department': 'Department_860', 'designation': 'Designation_860'},
        {'name': 'Name_861', 'email': 'dumpandjunk.com',
            'department': 'Department_861', 'designation': 'Designation_861'},
        {'name': 'Name_862', 'email': 'dumpmail.de',
            'department': 'Department_862', 'designation': 'Designation_862'},
        {'name': 'Name_863', 'email': 'dumpyemail.com',
            'department': 'Department_863', 'designation': 'Designation_863'},
        {'name': 'Name_864', 'email': 'durandinterstellar.com',
            'department': 'Department_864', 'designation': 'Designation_864'},
        {'name': 'Name_865', 'email': 'duskmail.com',
            'department': 'Department_865', 'designation': 'Designation_865'},
        {'name': 'Name_866', 'email': 'dwse.edu.pl',
            'department': 'Department_866', 'designation': 'Designation_866'},
        {'name': 'Name_867', 'email': 'dyceroprojects.com',
            'department': 'Department_867', 'designation': 'Designation_867'},
        {'name': 'Name_868', 'email': 'dz17.net',
            'department': 'Department_868', 'designation': 'Designation_868'},
        {'name': 'Name_869', 'email': 'e-mail.com',
            'department': 'Department_869', 'designation': 'Designation_869'},
        {'name': 'Name_870', 'email': 'e-mail.org',
            'department': 'Department_870', 'designation': 'Designation_870'},
        {'name': 'Name_871', 'email': 'e-marketstore.ru',
            'department': 'Department_871', 'designation': 'Designation_871'},
        {'name': 'Name_872', 'email': 'e-tomarigi.com',
            'department': 'Department_872', 'designation': 'Designation_872'},
        {'name': 'Name_873', 'email': 'e3z.de',
            'department': 'Department_873', 'designation': 'Designation_873'},
        {'name': 'Name_874', 'email': 'e4ward.com',
            'department': 'Department_874', 'designation': 'Designation_874'},
        {'name': 'Name_875', 'email': 'eanok.com',
            'department': 'Department_875', 'designation': 'Designation_875'},
        {'name': 'Name_876', 'email': 'easy-trash-mail.com',
            'department': 'Department_876', 'designation': 'Designation_876'},
        {'name': 'Name_877', 'email': 'easynetwork.info',
            'department': 'Department_877', 'designation': 'Designation_877'},
        {'name': 'Name_878', 'email': 'easytrashmail.com',
            'department': 'Department_878', 'designation': 'Designation_878'},
        {'name': 'Name_879', 'email': 'eatmea2z.club',
            'department': 'Department_879', 'designation': 'Designation_879'},
        {'name': 'Name_880', 'email': 'eay.jp',
            'department': 'Department_880', 'designation': 'Designation_880'},
        {'name': 'Name_881', 'email': 'ebbob.com',
            'department': 'Department_881', 'designation': 'Designation_881'},
        {'name': 'Name_882', 'email': 'ebeschlussbuch.de',
            'department': 'Department_882', 'designation': 'Designation_882'},
        {'name': 'Name_883', 'email': 'ecallheandi.com',
            'department': 'Department_883', 'designation': 'Designation_883'},
        {'name': 'Name_884', 'email': 'ecolo-online.fr',
            'department': 'Department_884', 'designation': 'Designation_884'},
        {'name': 'Name_885', 'email': 'edgex.ru',
            'department': 'Department_885', 'designation': 'Designation_885'},
        {'name': 'Name_886', 'email': 'edinburgh-airporthotels.com',
            'department': 'Department_886', 'designation': 'Designation_886'},
        {'name': 'Name_887', 'email': 'edv.to',
            'department': 'Department_887', 'designation': 'Designation_887'},
        {'name': 'Name_888', 'email': 'ee1.pl',
            'department': 'Department_888', 'designation': 'Designation_888'},
        {'name': 'Name_889', 'email': 'ee2.pl',
            'department': 'Department_889', 'designation': 'Designation_889'},
        {'name': 'Name_890', 'email': 'eeedv.de',
            'department': 'Department_890', 'designation': 'Designation_890'},
        {'name': 'Name_891', 'email': 'eelmail.com',
            'department': 'Department_891', 'designation': 'Designation_891'},
        {'name': 'Name_892', 'email': 'efxs.ca',
            'department': 'Department_892', 'designation': 'Designation_892'},
        {'name': 'Name_893', 'email': 'egzones.com',
            'department': 'Department_893', 'designation': 'Designation_893'},
        {'name': 'Name_894', 'email': 'einmalmail.de',
            'department': 'Department_894', 'designation': 'Designation_894'},
        {'name': 'Name_895', 'email': 'einrot.com',
            'department': 'Department_895', 'designation': 'Designation_895'},
        {'name': 'Name_896', 'email': 'einrot.de',
            'department': 'Department_896', 'designation': 'Designation_896'},
        {'name': 'Name_897', 'email': 'eintagsmail.de',
            'department': 'Department_897', 'designation': 'Designation_897'},
        {'name': 'Name_898', 'email': 'elearningjournal.org',
            'department': 'Department_898', 'designation': 'Designation_898'},
        {'name': 'Name_899', 'email': 'electro.mn',
            'department': 'Department_899', 'designation': 'Designation_899'},
        {'name': 'Name_900', 'email': 'elitevipatlantamodels.com',
            'department': 'Department_900', 'designation': 'Designation_900'},
        {'name': 'Name_901', 'email': 'elki-mkzn.ru',
            'department': 'Department_901', 'designation': 'Designation_901'},
        {'name': 'Name_902', 'email': 'email-fake.cf',
            'department': 'Department_902', 'designation': 'Designation_902'},
        {'name': 'Name_903', 'email': 'email-fake.com',
            'department': 'Department_903', 'designation': 'Designation_903'},
        {'name': 'Name_904', 'email': 'email-fake.ga',
            'department': 'Department_904', 'designation': 'Designation_904'},
        {'name': 'Name_905', 'email': 'email-fake.gq',
            'department': 'Department_905', 'designation': 'Designation_905'},
        {'name': 'Name_906', 'email': 'email-fake.ml',
            'department': 'Department_906', 'designation': 'Designation_906'},
        {'name': 'Name_907', 'email': 'email-fake.tk',
            'department': 'Department_907', 'designation': 'Designation_907'},
        {'name': 'Name_908', 'email': 'email-jetable.fr',
            'department': 'Department_908', 'designation': 'Designation_908'},
        {'name': 'Name_909', 'email': 'email-lab.com',
            'department': 'Department_909', 'designation': 'Designation_909'},
        {'name': 'Name_910', 'email': 'email-temp.com',
            'department': 'Department_910', 'designation': 'Designation_910'},
        {'name': 'Name_911', 'email': 'email.com',
            'department': 'Department_911', 'designation': 'Designation_911'},
        {'name': 'Name_912', 'email': 'email.edu.pl',
            'department': 'Department_912', 'designation': 'Designation_912'},
        {'name': 'Name_913', 'email': 'email.it',
            'department': 'Department_913', 'designation': 'Designation_913'},
        {'name': 'Name_914', 'email': 'email.net',
            'department': 'Department_914', 'designation': 'Designation_914'},
        {'name': 'Name_915', 'email': 'email.omshanti.edu.in',
            'department': 'Department_915', 'designation': 'Designation_915'},
        {'name': 'Name_916', 'email': 'email.ucms.edu.pk',
            'department': 'Department_916', 'designation': 'Designation_916'},
        {'name': 'Name_917', 'email': 'email1.pro',
            'department': 'Department_917', 'designation': 'Designation_917'},
        {'name': 'Name_918', 'email': 'email60.com',
            'department': 'Department_918', 'designation': 'Designation_918'},
        {'name': 'Name_919', 'email': 'emailage.cf',
            'department': 'Department_919', 'designation': 'Designation_919'},
        {'name': 'Name_920', 'email': 'emailage.ga',
            'department': 'Department_920', 'designation': 'Designation_920'},
        {'name': 'Name_921', 'email': 'emailage.gq',
            'department': 'Department_921', 'designation': 'Designation_921'},
        {'name': 'Name_922', 'email': 'emailage.ml',
            'department': 'Department_922', 'designation': 'Designation_922'},
        {'name': 'Name_923', 'email': 'emailage.tk',
            'department': 'Department_923', 'designation': 'Designation_923'},
        {'name': 'Name_924', 'email': 'emailate.com',
            'department': 'Department_924', 'designation': 'Designation_924'},
        {'name': 'Name_925', 'email': 'emailcu.icu',
            'department': 'Department_925', 'designation': 'Designation_925'},
        {'name': 'Name_926', 'email': 'emaildienst.de',
            'department': 'Department_926', 'designation': 'Designation_926'},
        {'name': 'Name_927', 'email': 'emaildrop.io',
            'department': 'Department_927', 'designation': 'Designation_927'},
        {'name': 'Name_928', 'email': 'emailfake.com',
            'department': 'Department_928', 'designation': 'Designation_928'},
        {'name': 'Name_929', 'email': 'emailfake.ml',
            'department': 'Department_929', 'designation': 'Designation_929'},
        {'name': 'Name_930', 'email': 'emailfreedom.ml',
            'department': 'Department_930', 'designation': 'Designation_930'},
        {'name': 'Name_931', 'email': 'emailgenerator.de',
            'department': 'Department_931', 'designation': 'Designation_931'},
        {'name': 'Name_932', 'email': 'emailgo.de',
            'department': 'Department_932', 'designation': 'Designation_932'},
        {'name': 'Name_933', 'email': 'emailias.com',
            'department': 'Department_933', 'designation': 'Designation_933'},
        {'name': 'Name_934', 'email': 'emailigo.de',
            'department': 'Department_934', 'designation': 'Designation_934'},
        {'name': 'Name_935', 'email': 'emailinfive.com',
            'department': 'Department_935', 'designation': 'Designation_935'},
        {'name': 'Name_936', 'email': 'emailisvalid.com',
            'department': 'Department_936', 'designation': 'Designation_936'},
        {'name': 'Name_937', 'email': 'emaillime.com',
            'department': 'Department_937', 'designation': 'Designation_937'},
        {'name': 'Name_938', 'email': 'emailmiser.com',
            'department': 'Department_938', 'designation': 'Designation_938'},
        {'name': 'Name_939', 'email': 'emailna.co',
            'department': 'Department_939', 'designation': 'Designation_939'},
        {'name': 'Name_940', 'email': 'emailnax.com',
            'department': 'Department_940', 'designation': 'Designation_940'},
        {'name': 'Name_941', 'email': 'emailo.pro',
            'department': 'Department_941', 'designation': 'Designation_941'},
        {'name': 'Name_942', 'email': 'emailondeck.com',
            'department': 'Department_942', 'designation': 'Designation_942'},
        {'name': 'Name_943', 'email': 'emailportal.info',
            'department': 'Department_943', 'designation': 'Designation_943'},
        {'name': 'Name_944', 'email': 'emailproxsy.com',
            'department': 'Department_944', 'designation': 'Designation_944'},
        {'name': 'Name_945', 'email': 'emailresort.com',
            'department': 'Department_945', 'designation': 'Designation_945'},
        {'name': 'Name_946', 'email': 'emails.ga',
            'department': 'Department_946', 'designation': 'Designation_946'},
        {'name': 'Name_947', 'email': 'emailsecurer.com',
            'department': 'Department_947', 'designation': 'Designation_947'},
        {'name': 'Name_948', 'email': 'emailsensei.com',
            'department': 'Department_948', 'designation': 'Designation_948'},
        {'name': 'Name_949', 'email': 'emailsingularity.net',
            'department': 'Department_949', 'designation': 'Designation_949'},
        {'name': 'Name_950', 'email': 'emailspam.cf',
            'department': 'Department_950', 'designation': 'Designation_950'},
        {'name': 'Name_951', 'email': 'emailspam.ga',
            'department': 'Department_951', 'designation': 'Designation_951'},
        {'name': 'Name_952', 'email': 'emailspam.gq',
            'department': 'Department_952', 'designation': 'Designation_952'},
        {'name': 'Name_953', 'email': 'emailspam.ml',
            'department': 'Department_953', 'designation': 'Designation_953'},
        {'name': 'Name_954', 'email': 'emailspam.tk',
            'department': 'Department_954', 'designation': 'Designation_954'},
        {'name': 'Name_955', 'email': 'emailsy.info',
            'department': 'Department_955', 'designation': 'Designation_955'},
        {'name': 'Name_956', 'email': 'emailtech.info',
            'department': 'Department_956', 'designation': 'Designation_956'},
        {'name': 'Name_957', 'email': 'emailtemporanea.com',
            'department': 'Department_957', 'designation': 'Designation_957'},
        {'name': 'Name_958', 'email': 'emailtemporanea.net',
            'department': 'Department_958', 'designation': 'Designation_958'},
        {'name': 'Name_959', 'email': 'emailtemporar.ro',
            'department': 'Department_959', 'designation': 'Designation_959'},
        {'name': 'Name_960', 'email': 'emailtemporario.com.br',
            'department': 'Department_960', 'designation': 'Designation_960'},
        {'name': 'Name_961', 'email': 'emailthe.net',
            'department': 'Department_961', 'designation': 'Designation_961'},
        {'name': 'Name_962', 'email': 'emailtmp.com',
            'department': 'Department_962', 'designation': 'Designation_962'},
        {'name': 'Name_963', 'email': 'emailto.de',
            'department': 'Department_963', 'designation': 'Designation_963'},
        {'name': 'Name_964', 'email': 'emailure.net',
            'department': 'Department_964', 'designation': 'Designation_964'},
        {'name': 'Name_965', 'email': 'emailwarden.com',
            'department': 'Department_965', 'designation': 'Designation_965'},
        {'name': 'Name_966', 'email': 'emailxfer.com',
            'department': 'Department_966', 'designation': 'Designation_966'},
        {'name': 'Name_967', 'email': 'emailz.cf',
            'department': 'Department_967', 'designation': 'Designation_967'},
        {'name': 'Name_968', 'email': 'emailz.ga',
            'department': 'Department_968', 'designation': 'Designation_968'},
        {'name': 'Name_969', 'email': 'emailz.gq',
            'department': 'Department_969', 'designation': 'Designation_969'},
        {'name': 'Name_970', 'email': 'emailz.ml',
            'department': 'Department_970', 'designation': 'Designation_970'},
        {'name': 'Name_971', 'email': 'emeil.in',
            'department': 'Department_971', 'designation': 'Designation_971'},
        {'name': 'Name_972', 'email': 'emeil.ir',
            'department': 'Department_972', 'designation': 'Designation_972'},
        {'name': 'Name_973', 'email': 'emeraldwebmail.com',
            'department': 'Department_973', 'designation': 'Designation_973'},
        {'name': 'Name_974', 'email': 'emil.com',
            'department': 'Department_974', 'designation': 'Designation_974'},
        {'name': 'Name_975', 'email': 'emkei.cf',
            'department': 'Department_975', 'designation': 'Designation_975'},
        {'name': 'Name_976', 'email': 'emkei.ga',
            'department': 'Department_976', 'designation': 'Designation_976'},
        {'name': 'Name_977', 'email': 'emkei.gq',
            'department': 'Department_977', 'designation': 'Designation_977'},
        {'name': 'Name_978', 'email': 'emkei.ml',
            'department': 'Department_978', 'designation': 'Designation_978'},
        {'name': 'Name_979', 'email': 'emkei.tk',
            'department': 'Department_979', 'designation': 'Designation_979'},
        {'name': 'Name_980', 'email': 'eml.pp.ua',
            'department': 'Department_980', 'designation': 'Designation_980'},
        {'name': 'Name_981', 'email': 'emlhub.com',
            'department': 'Department_981', 'designation': 'Designation_981'},
        {'name': 'Name_982', 'email': 'emlpro.com',
            'department': 'Department_982', 'designation': 'Designation_982'},
        {'name': 'Name_983', 'email': 'emltmp.com',
            'department': 'Department_983', 'designation': 'Designation_983'},
        {'name': 'Name_984', 'email': 'empireanime.ga',
            'department': 'Department_984', 'designation': 'Designation_984'},
        {'name': 'Name_985', 'email': 'emstjzh.com',
            'department': 'Department_985', 'designation': 'Designation_985'},
        {'name': 'Name_986', 'email': 'emz.net',
            'department': 'Department_986', 'designation': 'Designation_986'},
        {'name': 'Name_987', 'email': 'enayu.com',
            'department': 'Department_987', 'designation': 'Designation_987'},
        {'name': 'Name_988', 'email': 'enterto.com',
            'department': 'Department_988', 'designation': 'Designation_988'},
        {'name': 'Name_989', 'email': 'envy17.com',
            'department': 'Department_989', 'designation': 'Designation_989'},
        {'name': 'Name_990', 'email': 'eoffice.top',
            'department': 'Department_990', 'designation': 'Designation_990'},
        {'name': 'Name_991', 'email': 'eoopy.com',
            'department': 'Department_991', 'designation': 'Designation_991'},
        {'name': 'Name_992', 'email': 'epb.ro',
            'department': 'Department_992', 'designation': 'Designation_992'},
        {'name': 'Name_993', 'email': 'ephemail.net',
            'department': 'Department_993', 'designation': 'Designation_993'},
        {'name': 'Name_994', 'email': 'ephemeral.email',
            'department': 'Department_994', 'designation': 'Designation_994'},
        {'name': 'Name_995', 'email': 'eposta.buzz',
            'department': 'Department_995', 'designation': 'Designation_995'},
        {'name': 'Name_996', 'email': 'eposta.work',
            'department': 'Department_996', 'designation': 'Designation_996'},
        {'name': 'Name_997', 'email': 'eqiluxspam.ga',
            'department': 'Department_997', 'designation': 'Designation_997'},
        {'name': 'Name_998', 'email': 'ericjohnson.ml',
            'department': 'Department_998', 'designation': 'Designation_998'},
        {'name': 'Name_999', 'email': 'ero-tube.org',
            'department': 'Department_999', 'designation': 'Designation_999'},
        {'name': 'Name_1000', 'email': 'esbano-ru.ru',
            'department': 'Department_1000', 'designation': 'Designation_1000'},
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


def send_emails_by_group(groups, department_config, templates_dir):
    """Send emails group by group."""
    global emailed_candidates
    emailed_candidates = []

    try:
        for group in groups:
            config = department_config[group['config']]
            print(f"Processing group: {group['config']}")

            # Load the template for the group
            with open(os.path.join(templates_dir, config['template'])) as f:
                email_template = f.read()

            send_emails_in_batches(
                start_idx=group['start'],
                end_idx=group['end'],
                config=config,
                templates_dir=templates_dir,
                email_template=email_template,
                batch_size=5,  # 5 emails per batch
                email_delay=2,  # 2 seconds between emails
                batch_delay=15  # 15 seconds between batches
            )

            # Clean up after finishing a group
            gc.collect()  # Release memory
            time.sleep(10)  # 10 seconds delay before the next group

    except Exception as e:
        print(f"Error in processing groups: {str(e)}")


def send_emails_in_batches(start_idx, end_idx, config, templates_dir, email_template, batch_size, email_delay, batch_delay):
    """Send emails in smaller batches with delays."""
    from_email = config['email']
    password = config['password']
    email_subject = config['subject']
    action_name = config['action_name']
    training_link = "https://trial-ria-app.vercel.app/phishing_test/common_training_link"  # Common link

    try:
        with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
            server.starttls()
            server.login(from_email, password)

            for i in range(start_idx, end_idx, batch_size):
                # Query the batch
                batch = Colleagues.query.filter(
                    Colleagues.id >= i + 1,
                    Colleagues.id < i + batch_size + 1
                ).options(load_only(Colleagues.id, Colleagues.name, Colleagues.email, Colleagues.designation)).all()

                if not batch:
                    break  # Stop if no more records

                for colleague in batch:
                    to_email = colleague.email
                    msg = MIMEMultipart('related')
                    msg['Subject'] = email_subject
                    msg['From'] = from_email
                    msg['To'] = to_email

                    # Replace placeholders in the email template
                    body = email_template.replace(
                        "{{recipient_name}}", colleague.name)
                    body = body.replace("{{action_link}}", training_link)
                    body = body.replace("{{action_name}}", action_name)
                    body = body.replace("{{email_subject}}", email_subject)

                    html_content = f"""
                    <html>
                        <body>
                            {body}
                        </body>
                    </html>
                    """
                    msg.attach(MIMEText(html_content, 'html'))

                    try:
                        server.send_message(msg)
                        print(f"Email sent to {colleague.email}")

                        # Log email sent
                        update_email_log(colleague)
                        emailed_candidates.append({
                            'name': colleague.name,
                            'email': colleague.email,
                            'designation': colleague.designation
                        })

                    except Exception as e:
                        print(
                            f"Failed to send email to {colleague.email}: {str(e)}")

                    # Delay between emails
                    time.sleep(email_delay)

                # Clean up after processing a batch
                gc.collect()
                time.sleep(batch_delay)

    except Exception as e:
        print(f"Error in sending emails: {str(e)}")


# Example group configuration
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

# Start email processing
send_emails_by_group(groups, department_config, templates_dir)


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
