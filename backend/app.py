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


# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
# app.config['SECRET_KEY'] = "anuragiitmadras"

# DATABASE_URL = 'sqlite:///database.sqlite3'  # Replace with your actual DB URL
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL')  # Use full URL from Render
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
        {'name': 'Aaron Joseph Dionisio Santos', 'email': 'aaron.santos@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Aaronn Justin Gerard Alcantara Pimentel', 'email': 'aj.pimentel@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Adrian Steven Quevada', 'email': 'adrian.quevada@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},      
        {'name': 'Littianne Aira David Ambrocio', 'email': 'aira.ambrocio@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Aladiah Mehriel Pedrero Fulminar', 'email': 'aladiah.fulminar@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Alexander Bagas Penalba', 'email': 'alexander.penalba@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},  
        {'name': 'Alleb Jimeno Castro', 'email': 'alleb.castro@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},       
        {'name': 'Allen Christian Manalapaz Manansala', 'email': 'allen.manansala@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Andreau Orona Aranton', 'email': 'andreau.aranton@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},      
        {'name': 'Andrei Laborte Salvador', 'email': 'andrei.salvador@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},    
        {'name': 'Angel Troy Malana Reyes', 'email': 'troy.reyes@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Angelica Elaine Limkico', 'email': 'angelicaelaine.limkico@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Anjelico-Riz Chan Dumlao', 'email': 'anjelicoriz.dumlao@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},{'name': 'Gertrude Anne Andrada Llanora', 'email': 'gertrude.llanora@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Apraem Cayle Francisco Mabaga', 'email': 'apraem.mabaga@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},{'name': 'April Laverne Hedia Encinares', 'email': 'laverne.encinares@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Arjel Joseph Escal Aya-ay', 'email': 'arjel.ayaay@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},     
        {'name': 'Arvin Dale Dajon Llego', 'email': 'arvin.llego@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},        
        {'name': 'Arvin Jerald Liwanag Angeles', 'email': 'arvinjerald.angeles@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Ava Julia Leaño Norada', 'email': 'ava.norada@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Benedict Dec', 'email': 'ben.edict@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Benjamin Julien Cuison Roque', 'email': 'benjamin.roque@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},{'name': 'Bill Eros Ablan Castillo', 'email': 'bill.castillo@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'}, 
        {'name': 'Brenan Jake Pastoral Murillo', 'email': 'brenan.murillo@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Brent Timothy Carreon Utana', 'email': 'brent.utana@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},{'name': 'Brian Paul Gallardo Arriola', 'email': 'brian.arriola@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'}, 
        {'name': 'Briant Alonzo Morales', 'email': 'briant.morales@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},       
        {'name': 'Bryan Oser Maglanoc', 'email': 'bryan.maglanoc@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},     
        {'name': 'Celeena Caleon Alonzo', 'email': 'celeena.alonzo@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Celestino Rosell Ranili Jr.', 'email': 'celestino.ranili@riaadvisory.com', 'department': 'Developer', 'designation': 'Facilities and Administrative Officer'},
        {'name': 'Charlene Yee Quiz', 'email': 'charlene.quiz@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Chester Tañafranca Castillo', 'email': 'chester.castillo@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Chester John Que Heath', 'email': 'chester.heath@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},   
        {'name': 'Christian Carlos Himpil Casino', 'email': 'christian.casino@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Christian Rey Balberan Doctolero', 'email': 'christian.doctolero@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Christopher "EJ" Buenviaje Sanchez', 'email': 'christopher.sanchez@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Clark Andrew Correa Rodriguez', 'email': 'clark.rodriguez@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Danica Mariz Leona Gonzales', 'email': 'danica.gonzales@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Daniel Teodoro Gonzales Tudtud', 'email': 'daniel.tudtud@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Danniel Joseph Doctor Manalaysay', 'email': 'danniel.manalaysay@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Darren Reyes Tee', 'email': 'darren.tee@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Den Mark Marcelo Rodis', 'email': 'denmark.rodis@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},      
        {'name': 'Denise Anne Camacho Soriano', 'email': 'denise.soriano@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'Deselle Jandoc', 'email': 'deselle.jandoc@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Dhane-Jyn Gonzales Lising', 'email': 'jyn.lising@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},       
        {'name': 'Dominique Europa Dagunton', 'email': 'dominique.dagunton@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Don Ivan Pasigna Silvan', 'email': 'ivan.silvan@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},    
        {'name': 'Dranel Allen Mabuti Papa', 'email': 'dranel.papa@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},       
        {'name': 'Ellen Joy Dela Torre Padilla', 'email': 'ellen.padilla@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Epilyn Cagurangan Angoluan', 'email': 'epilyn.angoluan@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Eric John Cubian Leron', 'email': 'eric.leron@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},      
        {'name': 'Eric Miguel Parma', 'email': 'miguel.parma@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Erick Baclit Abad', 'email': 'erick.abad@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Felicidad Cruz Shih', 'email': 'felicidad.shih@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},        
        {'name': 'Francis Donald Pasco Alfonso', 'email': 'francis.alfonso@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Franz Jeffrey Seril Taguines', 'email': 'franzjeffrey.taguines@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Gabriel James Manalo Tecson', 'email': 'gabriel.tecson@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'Genesis Bayron Soriano', 'email': 'genesis.soriano@riaadvisory.com', 'department': 'Developer', 'designation': 'Administrative Support'},
        {'name': 'Hazel Marife Canta Segubre', 'email': 'hazel.segubre@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Ian Carlo Robles Santos', 'email': 'ian.santos@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},     
        {'name': 'Ian Langley Labios Lim', 'email': 'ianlangley.lim@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},  
        {'name': 'Irvin Randell Daniel Moraga', 'email': 'irvin.moraga@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},   
        {'name': 'Isaac Carin Villareal', 'email': 'isaac.villareal@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},      
        {'name': 'Ivan Alexci Tamayo Goyagoy', 'email': 'ivan.goyagoy@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},{'name': 'Jackielyn Jane Tagata Yogawin', 'email': 'jackielyn.yogawin@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Jah-Lee Rosal Nerpio', 'email': 'jah-lee.nerpio@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Jake Howell Susi Lubrica', 'email': 'jakehowell.lubrica@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},{'name': 'James Noah Alberto Santos', 'email': 'jamesnoah.santos@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'Jan Carl Labarrete Camerino', 'email': 'jancarl.camerino@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Jan Melvin Jimenez Jimenez', 'email': 'melvin.jimenez@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},  
        {'name': 'Jan Michael Sih Hung', 'email': 'jan.hung@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},   
        {'name': 'Janeric Enthusias Ferrer Madrid', 'email': 'janeric.madrid@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Jaymie Jean Llanes Cusay', 'email': 'jaymie.cusay@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},  
        {'name': 'Jenah Frances Molina Velasquez', 'email': 'jenah.velasquez@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Jenirose Poyaoan Lozano', 'email': 'jenirose.lozano@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},{'name': 'Jenna Karla Calibara Tardio', 'email': 'jenna.tardio@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Jennifer Jasa Addawe', 'email': 'jennifer.addawe@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Jeremie Francis Perez Briones', 'email': 'jeremie.briones@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Jeremie Jun Canapi Viray', 'email': 'jeremiejun.viray@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Jeric Ermita Calma', 'email': 'jeric.calma@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Jerome Jerico Tiongco Ramos', 'email': 'jerome.ramos@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},  
        {'name': 'Jerssey Pajaron Brania', 'email': 'jerssey.brania@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Jesse John Viste Senen', 'email': 'jesse.senen@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Jhennie Sombilon Fernandez', 'email': 'jhennie.fernandez@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Jhon Jhon Dantes Danor', 'email': 'jhon.danor@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Jimuel Ace Rodriguez Sarmiento', 'email': 'jimuel.sarmiento@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Jiro Mark Guzman Garcia', 'email': 'jiro.garcia@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},        
        {'name': 'Joaquin Francisco Mayo Roman', 'email': 'joaquinfrancisco.roman@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Joefrey Cyruz Larisma Alvarez', 'email': 'joefreycyruz.alvarez@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Joey Malecdan Addawe', 'email': 'joey.addawe@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},{'name': 'John Cris Berroya Santos', 'email': 'johncris.santos@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},   
        {'name': 'John Kevin Gonzaga Villacorta', 'email': 'kevin.villacorta@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'John Manuel Fernandez Tala', 'email': 'johnmanuel.tala@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'John Mari Reyes Alcausin', 'email': 'johnmari.alcausin@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'John Mark Arellano Fabros', 'email': 'john.fabros@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},      
        {'name': 'John Martin Banasihan Malana', 'email': 'martin.malana@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'John Nicholas Portillo Felix', 'email': 'john.felix@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},    
        {'name': 'John Paul Bamba Viñas', 'email': 'johnpaul.vinas@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},       
        {'name': 'John Reniel Francial Geronimo', 'email': 'johnreniel.geronimo@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Joseph Ermita Calma', 'email': 'joseph.calma@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Joshua Mark Arceo Esguerra', 'email': 'joshua.esguerra@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'Joyce Malimit San Juan', 'email': 'joyce.sanjuan@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},      
        {'name': 'Juan Kristoffer Gonzaga Villacorta', 'email': 'juan.villacorta@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Juan Rene Sebuado Goco', 'email': 'jr.goco@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},  
        {'name': 'Jude Patrick Requinto Ortega', 'email': 'jude.ortega@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Jun Zedrick Tolentino Fajardo', 'email': 'zedrick.fajardo@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Justine Mike Valenzuela', 'email': 'justine.valenzuela@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'Karl Matheu Bernardo Muyot', 'email': 'karl.muyot@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},     
        {'name': 'Kate Lorraine Infante Bulong', 'email': 'kate.bulong@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},   
        {'name': 'Kenneth Ang Chua', 'email': 'kenneth.chua@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},   
        {'name': 'Kenneth Jhon Acosta Bolusan', 'email': 'kenneth.bolusan@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Krissianne Mae Argame Casacop', 'email': 'krissianne.casacop@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Kurt Lawrence Dagohoy Torregoza', 'email': 'lawrence.torregoza@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Lawrence Jude San Juan Cabuhat', 'email': 'lawrencejude.cabuhat@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Leyen Decker De Guzman Santiago', 'email': 'leyendecker.santiago@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Lucky Espiritu Cruz', 'email': 'lucky.cruz@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Ma. Andrea Clariza Canaria Ferrer', 'email': 'clariza.ferrer@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Mac Charl Rivera Villaseñor', 'email': 'mac.villasenor@riaadvisory.com', 'department': 'Developer', 'designation': 'Database Administrator'},
        {'name': 'Marc Kenneth Deloy Apole', 'email': 'marckenneth.apole@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Marcel Joseph Gapac Hermocilla', 'email': 'marcel.hermocilla@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Marcelino Gozun Esguerra', 'email': 'marcelino.esguerra@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},{'name': 'Marco Antonino Meriales Juan', 'email': 'marco.juan@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},{'name': 'Maria Angelika Hernandez Tensuan', 'email': 'maria.tensuan@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Marion Paul Atog Mahilum', 'email': 'marion.mahilum@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},{'name': 'Marjorie Tomboc Roxas', 'email': 'marjorie.roxas@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},      
        {'name': 'Mark Guadalupe Advincula', 'email': 'mark.advincula@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},    
        {'name': 'Mark Angelo Tayson Serrano', 'email': 'mark.serrano@riaadvisory.com', 'department': 'Developer', 'designation': 'Database Administrator'},
        {'name': 'Mark Christopher Reyes Vizcarra', 'email': 'mark.vizcarra@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Mark Lester Malig-on Cubil', 'email': 'mark.cubil@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},  
        {'name': 'Marlon Baniega Tarrayo', 'email': 'marlon.tarrayo@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},  
        {'name': 'Mary Mae Nioko Serino', 'email': 'marymae.serino@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},       
        {'name': 'Mary Raphaelle Cinco Huela', 'email': 'mary.huela@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},  
        {'name': 'Marychelle Zafe Ramos', 'email': 'marychelle.ramos@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'}, 
        {'name': 'Mel Jordan Fullante Castro', 'email': 'mel.castro@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},      
        {'name': 'Melissa Gay Urbi Fule', 'email': 'melissa.fule@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Carmelita Santos Sacdalan', 'email': 'carmelita.sacdalan@riaadvisory.com', 'department': 'Developer', 'designation': 'Project Manager'},{'name': 'Michelle Ann Samson Magano', 'email': 'michelle.magano@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Mikyla Biel Villaflor Gallego', 'email': 'mikyla.gallego@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Mitzi Jumamil delos Santos', 'email': 'mitzi.delossantos@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Moises Guro Adolfo', 'email': 'moises.adolfo@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},       
        {'name': 'Monica Eugene Bragado De Ocampo', 'email': 'monica.deocampo@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Nathan Andrei Agena Galang', 'email': 'nathan.galang@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},   
        {'name': 'Nathan Zoe Codamon Licyayo', 'email': 'nathan.licyayo@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},  
        {'name': 'Neil Chester Eufeminiano Egalla', 'email': 'neil.egalla@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Jeanica Marie Fernandez', 'email': 'jeanica.fernandez@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Nica Mae Balangat Canteros', 'email': 'nica.canteros@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Nina Elaiza Factor De Castro', 'email': 'nina.decastro@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Oliver Anbochi Militante', 'email': 'oliver.militante@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Pamela Samson David', 'email': 'pamela.david@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},{'name': 'Patricia Marie Mallari Aguilar', 'email': 'patricia.aguilar@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Patricia Alesna Medina', 'email': 'patricia.medina@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},     
        {'name': 'Patrick Johnpaul Magaling Bautista', 'email': 'patrick.bautista@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Patrick Nikko Iloco Calvo', 'email': 'nikko.calvo@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},      
        {'name': 'Queenie Marie Manalo Celebrado', 'email': 'queenie.celebrado@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Rafael Matthew Panganiban Teberio', 'email': 'rafaelmatthew.teberio@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Rani Rain Salamera Rotairo', 'email': 'rani.rotairo@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},   
        {'name': 'Raquelle Mae Laraya Gueta', 'email': 'raquelle.gueta@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Raymond Aliwalas Caliguiran', 'email': 'raymond.caliguiran@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Rea Pino Catibag', 'email': 'rea.catibag@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Rebecca Sechong Liceralde', 'email': 'rebecca.liceralde@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Redalyn Articona Pamplina', 'email': 'redalyn.pamplina@riaadvisory.com', 'department': 'Developer', 'designation': 'Practice Director'},{'name': 'Renelle Fernandez Carlos', 'email': 'renelle.carlos@riaadvisory.com', 'department': 'Developer', 'designation': 'Sr Principal Consultant'},
        {'name': 'Rica Mae Marasigan Bristol', 'email': 'rica.bristol@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},    
        {'name': 'Ricci Diorrisni Go Kwok-Suarez', 'email': 'ricci.kwok-suarez@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Roberto Crisostomo Gerona Jr.', 'email': 'roberto.gerona@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Roland Jerome Ensomo Olayvar', 'email': 'roland.olayvar@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},{'name': 'Rommel Molo Santos', 'email': 'rommel.santos@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},       
        {'name': 'Ronen Gangan Santos', 'email': 'ronen.santos@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Roselyn Romanillos Cruz', 'email': 'roselyn.cruz@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},   
        {'name': 'Rudy Lee Lim Tuprio', 'email': 'rudylee.tuprio@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Samuel John Quimbo Maligad', 'email': 'samueljohn.maligad@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Sharmaine Bautista Dantes', 'email': 'sharmaine.dantes@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Tristan Angelo Pandi Manalad', 'email': 'tristan.manalad@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Vanessa Anne Samante Melegrito', 'email': 'vanessa.melegrito@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Victor John Labutong Abrenica', 'email': 'victorjohn.abrenica@riaadvisory.com', 'department': 'Developer', 'designation': 'Project Manager'},
        {'name': 'Vienna Blessilda Villalon Rom', 'email': 'vienna.rom@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Vince Geoffrey Reyes Legaspi', 'email': 'vince.legaspi@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'}, 
        {'name': 'William Agustin Anganangan', 'email': 'william.anganangan@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Wilson Tubera Magaoay', 'email': 'wilson.magaoay@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},       
        {'name': 'Zahra Jamielle Endrenal Lacerona', 'email': 'zahra.lacerona@riaadvisory.com', 'department': 'Developer', 'designation': 'Staff Consultant'},
        {'name': 'Maria Niña Trinidad Comia', 'email': 'nina.comia@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Krishna Manoj Chaudhari', 'email': 'krishna.chaudhari@riaadvisory.com', 'department': 'Internal IT and Cloud Ops', 'designation': 'Associate Consultant'},
        {'name': 'Aadesh Borgaonkar', 'email': 'aadesh.borgaonkar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},       
        {'name': 'Aakansha Rathore', 'email': 'aakansha.rathore@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},      
        {'name': 'Abdur Rafey', 'email': 'abdur.rafey@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Abhay Godara', 'email': 'abhay.godara@riaadvisory.com', 'department': 'Developer', 'designation': 'Junior Software Development Engineer (SDE1)'},
        {'name': 'Abhigyan Biswas', 'email': 'abhigyan.biswas@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Abhijeet Shriram Kulkarni', 'email': 'abhijeet.kulkarni@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Abhijit Bhusare', 'email': 'abhijit.bhusare@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Abhijit Rane', 'email': 'abhijit.rane@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},       
        {'name': 'Abhilash L J', 'email': 'abhilash.lj@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Abhinandan Patil', 'email': 'abhinandan.patil@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Abhinav Jha', 'email': 'abhinav.jha@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Abhinav Pahariya', 'email': 'abhinav.pahariya@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Abhishek Adhav', 'email': 'abhishek.adhav@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Abhishek Sharma', 'email': 'abhishek.sharma@riaadvisory.com', 'department': 'Developer', 'designation': 'Junior Software Developer (SDE1)'},
        {'name': 'Abhishek Shrivastava', 'email': 'abhishek.shrivastava@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Director'},
        {'name': 'Abhishek Shukla', 'email': 'abhishek.shukla@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},        
        {'name': 'Abhishek Singh', 'email': 'abhishek.singh@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Adam Jernigan', 'email': 'adam.jernigan@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Adarsh Inginshetty', 'email': 'adarsh.inginshetty@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Adil Banekar', 'email': 'adil.banekar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Adithya Suresh', 'email': 'adithya.suresh@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Adwait Snehal Kadam', 'email': 'adwait.kadam@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},       
        {'name': 'Afrin Ibrahim Mulla', 'email': 'afrin.athanikar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Agney Arun Bhople', 'email': 'agney.bhople@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Aishwarya C', 'email': 'aishwarya.c@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Aishwarya Ravindra Jorve', 'email': 'aishwarya.jorve@riaadvisory.com', 'department': 'Developer', 'designation': 'Spring boot Developer'},
        {'name': 'Ajay Ajay', 'email': 'ajay@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Ajay Borude', 'email': 'ajay.borude@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Ajay Bharat Ghosade', 'email': 'ajay.ghosade@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Ajinkya Satish Kulkarni', 'email': 'ajinkya.kulkarni@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Ajith KS', 'email': 'ajith.k@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Akanksha Tripathi', 'email': 'akanksha.tripathi@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},    
        {'name': 'Akash Daryanani', 'email': 'akash.daryanani@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Software Engineer (SDE4)'},
        {'name': 'Akash Shripal Jain', 'email': 'akash.jain@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'AKASH PATIL', 'email': 'akash.patil@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'AKSHATA MAGDUM', 'email': 'akshata.magdum@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Akshay Lakhotiya', 'email': 'akshay.lakhotiya@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Akshay Limaye', 'email': 'akshay.limaye@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Director Consulting'},      
        {'name': 'Akshay Ulhe', 'email': 'akshay.ulhe@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Software Engineer (SDE4)'},  
        {'name': 'Akshaya H', 'email': 'akshaya.h@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Akshaya Kapoor', 'email': 'akshaya.k@riaadvisory.com', 'department': 'Developer', 'designation': 'Managing Director'},
        {'name': 'Akshit Kumar Dhiman', 'email': 'akshit.dhiman@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},      
        {'name': 'Alekya Devata', 'email': 'alekya.devata@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Allan Mirpuri', 'email': 'allan.mirpuri@riaadvisory.com', 'department': 'Developer', 'designation': 'Functional Architect'},
        {'name': 'Amar Laxmikant Maurya', 'email': 'amar.maurya@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},      
        {'name': 'Amarja Kumbhar', 'email': 'amarja.kumbhar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Ameya Bokil', 'email': 'amey.bokil@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Amit Jadhav', 'email': 'amit.jadhav@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Amit Ranjan', 'email': 'amit.ranjan@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Amit Dhanjibhai Unagar', 'email': 'amit.unagar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Amit Upadhyay', 'email': 'amit.upadhyay@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Amitabh Ajaya Biswal', 'email': 'amitabh.biswal@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Amitesh Anirudhan', 'email': 'amitesh.anirudhan@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Amogh Milind Dharmapurikar', 'email': 'amogh.dharmapurikar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Amol Shashishekhar Bhagwat', 'email': 'amol.bhagwat@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},{'name': 'Amrita Sinha', 'email': 'amrita.sinha@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Project Manager'},        
        {'name': 'Amruta Deshmukh', 'email': 'amruta.deshmukh@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Software Development Engineer (SDE3)'},
        {'name': 'Amruta Shrikrishna Kulkarni', 'email': 'amruta.kulkarni@riaadvisory.com', 'department': 'Developer', 'designation': 'Project Manager'}, 
        {'name': 'Anand Raghunath Godbole', 'email': 'anand.godbole@riaadvisory.com', 'department': 'Developer', 'designation': 'Project Manager'},       
        {'name': 'Andre Marais', 'email': 'andre.marais@riaadvisory.com', 'department': 'Developer', 'designation': 'Director  Consulting'},
        {'name': 'Aniket Fand', 'email': 'aniket.fand@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Anil Sarjerao Patil', 'email': 'anil.patil@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Anjali Agrawal', 'email': 'anjali.agrawal@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Software Developer (SD3)'},
        {'name': 'Anjali Mali', 'email': 'anjali.mali@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Anjali Taran', 'email': 'anjali.taran@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Ankit Ganesh Agrawal', 'email': 'ankit.agrawal@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},     
        {'name': 'Ankit Khare', 'email': 'ankit.khare@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Ankit Kumar', 'email': 'ankit.kumar@riaadvisory.com', 'department': 'Developer', 'designation': 'Junior Software Development Engineer (SDE1)'},
        {'name': 'Ankit Modi', 'email': 'ankit.modi@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Ankur Kumar Sharma', 'email': 'ankur.sharma@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},        
        {'name': 'Anmol Dutta', 'email': 'anmol.dutta@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Anuj Sanjeev Thakare', 'email': 'anuj.thakare@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},      
        {'name': 'Anujitsinh Bhosale', 'email': 'anujitsinh.bhosale@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Anupama Vasudev Joshi', 'email': 'anupama.joshi@riaadvisory.com', 'department': 'Developer', 'designation': 'Solution Architect'},      
        {'name': 'Anuprita Sachin Shukre', 'email': 'anuprita.shukre@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Anurag Tiwari', 'email': 'anurag.tiwari@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Director'},
        {'name': 'Anusha Dhani', 'email': 'anusha.dhani@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Anusha Ilangovan', 'email': 'anusha.i@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Manager'},
        {'name': 'Apeksha Lal', 'email': 'apeksha.lal@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Software Developer (SDE3)'},    
        {'name': 'Apurva Uday Acharya', 'email': 'apurva.acharya@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},     
        {'name': 'Apurva Ashok Puranik', 'email': 'apurva.puranik@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Manager'},      
        {'name': 'Arati Wayase', 'email': 'arati.wayase@riaadvisory.com', 'department': 'Developer', 'designation': 'Software Development Engineer (SDE2)'},
        {'name': 'Archana Alagandula', 'email': 'archana.alagandula@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Arjun Vijaykumar Sharma', 'email': 'arjun.sharma@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},      
        {'name': 'Arpit Dixit', 'email': 'arpit.dixit@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Arpita Singha', 'email': 'arpita.singha@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Arya Gupta', 'email': 'arya.gupta@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Asha Kolagunda Nagappa Shetty', 'email': 'asha.shetty@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Asheesh Kumar Jain', 'email': 'asheesh.jain@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Manager - QA'},
        {'name': 'Ashvini Mopkar', 'email': 'ashvini.mopkar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Ashwini Vasu Dornal', 'email': 'ashwini.dornal@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Ashwini Wyawahare', 'email': 'ashwini.wyawahare@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},    
        {'name': 'Atharva Bhagwat', 'email': 'atharva.bhagwat@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},        
        {'name': 'Atul Vijay Kale', 'email': 'atul.kale@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Aurelio Rodrigo Lobatón', 'email': 'aurelio.lobaton@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Aviral Mehrotra', 'email': 'aviral.mehrotra@riaadvisory.com', 'department': 'Developer', 'designation': 'Junior Software Developer (SDE1)'},
        {'name': 'Aviral Raman', 'email': 'aviral.raman@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Avishkar Sunil Mulik', 'email': 'avishkar.mulik@riaadvisory.com', 'department': 'Developer', 'designation': 'Junior Software Developer (SDE1)'},
        {'name': 'Ayeesha Begame L', 'email': 'ayeesha.liyahath@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Bhakti Bharat Baliwant', 'email': 'bhakti.baliwant@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Bhavana Shankar Badgujar', 'email': 'bhavana.badgujar@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Bijal Gunderia', 'email': 'bijal.gunderia@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consulting Manager'},     
        {'name': 'Bikash Pattanayak', 'email': 'bikash.pattanayak@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},    
        {'name': 'Bincy Kannankandiyil', 'email': 'bincy.kannankandiyil@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Bosco Javier Alvarado Ayala', 'email': 'bosco.alvarado@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},       
        {'name': 'Brenda Contreras', 'email': 'brenda.contreras@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Carmen Garduño', 'email': 'carmen.garduno@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Cerin George', 'email': 'cerin.george@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Chaitali Arun More', 'email': 'chaitali.more@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Chaitanya Rothe', 'email': 'chaitanya.rothe@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Chandni Sharma', 'email': 'chandni.sharma@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Chandrima Sahu', 'email': 'chandrima.sahu@riaadvisory.com', 'department': 'Developer', 'designation': 'Software Development Engineer (SDE2)'},
        {'name': 'Chaynita Sharma', 'email': 'chaynita.sharma@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Chintaman Dudharam Waghare', 'email': 'chintaman.waghare@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Choon Hoong Ding', 'email': 'choonhoong.ding@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Director'},
        {'name': 'Christo Groenewald', 'email': 'christo.groenewald@riaadvisory.com', 'department': 'Developer', 'designation': 'Director'},
        {'name': 'Conrad Chan', 'email': 'conrad.chan@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Solution Architect'},
        {'name': 'Ana Cristina Dávila Guerrero', 'email': 'cristina.davila@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},     
        {'name': 'Darius Green', 'email': 'darius.green@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Darshan Yogeshbhai Dhandhukiya', 'email': 'darshan.dhandhukiya@riaadvisory.com', 'department': 'Developer', 'designation': 'Software Development Engineer (SDE2)'},
        {'name': 'Darshan Gunagi', 'email': 'darshan.gunagi@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Darshana Hutke', 'email': 'darshana.hutke@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Deepak Gupta', 'email': 'deepak.gupta@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Deepak Sukumar Nair', 'email': 'deepak.nair@riaadvisory.com', 'department': 'Developer', 'designation': 'Delivery Project Manager'},    
        {'name': 'Deon Sunny', 'email': 'deon.sunny@riaadvisory.com', 'department': 'Developer', 'designation': 'Software Development Engineer (SDE2)'},  
        {'name': 'Devashree Kalkundrikar', 'email': 'devashree.kalkundrikar@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Devyani Surendra Gaikwad', 'email': 'devyani.gaikwad@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},  
        {'name': 'Dhairyashil Shinde', 'email': 'dhairyashil.shinde@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},  
        {'name': 'Dhanashree Mahadev Kankanwade', 'email': 'dhanashree.kankanwade@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Dipali Mulye', 'email': 'dipali.mulye@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Divya Mohan Hemalatha', 'email': 'divya.mohan@riaadvisory.com', 'department': 'Developer', 'designation': 'Business Analyst Functional Consultant'},
        {'name': 'Rekha Donkada', 'email': 'rekha.donkada@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Edith Hanson', 'email': 'edie.hanson@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Gandhi Adurthi', 'email': 'gandhi.adurthi@riaadvisory.com', 'department': 'Developer', 'designation': 'Director'},
        {'name': 'Gargee Vasudeo Athalye', 'email': 'gargee.athalye@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},  
        {'name': 'Gaurav Chandekar', 'email': 'gaurav.chandekar@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},      
        {'name': 'Gayatri Satish Aurangabadkar', 'email': 'gayatri.aurangabadkar@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Gayatri Santosh Desai', 'email': 'gayatri.desai@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},    
        {'name': 'Geetharani G', 'email': 'geetharani.g@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Technical Manager'},      
        {'name': 'Gokulakrishnan Karuppiah', 'email': 'gokul.karuppiah@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Senior Manager'},
        {'name': 'Gopi Yarlagadda', 'email': 'gopi.yarlagadda@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},        
        {'name': 'Greeshma Santhosh', 'email': 'greeshma.santhosh@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Software Development Engineer (SDE3)'},
        {'name': 'Guru Vamsi', 'email': 'guru.vamsi@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Guruprasad Dastane', 'email': 'guruprasad.dastane@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},  
        {'name': 'Happy Maganbhai Limbasiya', 'email': 'happy.limbasiya@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},        
        {'name': 'Harish Hanumant Gawade', 'email': 'harish.gawade@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},   
        {'name': 'Harish Kumar Madishetty', 'email': 'harish.madishetty@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Director Consulting'},
        {'name': 'Harsh Solanki', 'email': 'harsh.solanki@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Harshal Kishor Chaudhari', 'email': 'harshal.chaudhari@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Hemant Manral', 'email': 'hemant.manral@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Project Manager'},
        {'name': 'Himaja Narina', 'email': 'himaja.narina@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Hrishikesh Deshpande', 'email': 'hrishikesh.deshpande@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Hrushikesh Pande', 'email': 'hrushikesh.pande@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Isaiah Gage', 'email': 'isaiah.gage@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Isha Ranade', 'email': 'isha.ranade@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Ishan Majumdar', 'email': 'ishan.majumdar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Jacek Ziabicki', 'email': 'jacek.ziabicki@riaadvisory.com', 'department': 'Developer', 'designation': 'Director  Consulting'},
        {'name': 'Jai Soni', 'email': 'jai.soni@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Jaishree Anup Khadatkar', 'email': 'jaishree.khadatkar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Architect'}, 
        {'name': 'Jayanti Pratik Kore', 'email': 'jayanti.khutwad@riaadvisory.com', 'department': 'Developer', 'designation': 'Software Development Engineer (SDE2)'},
        {'name': 'Jaydeep Patil', 'email': 'jaydeep.patil@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Jayesh Ugalmugale', 'email': 'jayesh.ugalmugale@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},       
        {'name': 'Jayjeet Dhar', 'email': 'jayjeet.dhar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Jaywant Kishor Kadam', 'email': 'jaywant.kadam@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},     
        {'name': 'Jidnyasa Jankar', 'email': 'jidnyasa.jankar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Joy Karow', 'email': 'joy.karow@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Jyothi Tamma', 'email': 'jyothi.tamma@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},       
        {'name': 'Kajal Deshmane', 'email': 'kajal.deshmane@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Kalyani Jagdale', 'email': 'kalyani.jagdale@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},        
        {'name': 'Kamalakar Dagade', 'email': 'kamalakar.dagade@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},      
        {'name': 'Kamlesh Rajendra Patil', 'email': 'kamlesh.patil@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Kapil Suri', 'email': 'kapil.suri@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Director'},
        {'name': 'Karan Mehta', 'email': 'karan.mehta@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Karthik Murthy', 'email': 'karthik.murthy@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Kartikeya Kumar', 'email': 'kartikeya.kumar@riaadvisory.com', 'department': 'Developer', 'designation': 'Software Development Engineer (SDE2)'},
        {'name': 'Kaustubh Gajanan Dange', 'email': 'kaustubh.dange@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Kavita Ravindra Gangele', 'email': 'kavita.gangele@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},    
        {'name': 'Kenneth Chan', 'email': 'kenneth.chan@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Director'},
        {'name': 'Ketan Joshi', 'email': 'ketan.joshi@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Khandu Ram Ghuge', 'email': 'khandu.ghuge@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Khushi Pagariya', 'email': 'khushi.pagariya@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},        
        {'name': 'Khushii Pathak Mishra', 'email': 'khushii.pathakmishra@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},{'name': 'Kimberly Schafer', 'email': 'kim@validos.com', 'department': 'Developer', 'designation': 'Contractor'},
        {'name': 'Kiran Sudam Udar', 'email': 'kiran.udar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consulting Manager'},       
        {'name': 'Komal Bhise', 'email': 'komal.bhise@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Komal Ganesh Iyer', 'email': 'komal.iyer@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Krishna Patel', 'email': 'krishna.patel@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Kshitija Joshi', 'email': 'kshitija.joshi@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Kumar Subramanian', 'email': 'kumar.subramanian@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},       
        {'name': 'Kunal Girishrao Hedau', 'email': 'kunal.hedau@riaadvisory.com', 'department': 'Developer', 'designation': 'Director  Information Systems'},
        {'name': 'Kunal Malhotra', 'email': 'kunal.malhotra@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Lakhan Bansode', 'email': 'lakhan.bansode@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'},
        {'name': 'Lavanya Moorthy', 'email': 'lavanya.moorthy@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Leelakrishna Voggu', 'email': 'leelakrishna.voggu@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},  
        {'name': 'Lekshmi B G', 'email': 'lekshmi.bg@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Leonel Devaldemar', 'email': 'leonel.devaldemar@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Linta Shivaji Shewale', 'email': 'linta.shewale@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Lisa Kabra', 'email': 'lisa.kabra@riaadvisory.com', 'department': 'Developer', 'designation': 'Project Manager'},
        {'name': 'Lokesh Bhardwaj', 'email': 'lokesh.bhardwaj@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'}, 
        {'name': 'Lauren Jeanne Slatko', 'email': 'lori.slatko@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Manager'},
        {'name': 'Madhu Parameswaran', 'email': 'madhu.parameswaran@riaadvisory.com', 'department': 'Developer', 'designation': 'Director'},
        {'name': 'Madhuri Agarwal', 'email': 'madhuri.agarwal@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},        
        {'name': 'Madhuri Limgude', 'email': 'madhuri.limgude@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Madhuri Nirvikar', 'email': 'madhuri.nirvikar@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},      
        {'name': 'MahalakshmiAbinaya Kumarakrishnan', 'email': 'mahalakshmi.abinaya@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},
        {'name': 'Mahinder Partap Singh', 'email': 'mahinder.singh@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},   
        {'name': 'Greeshma Mamidi', 'email': 'greeshma.mamidi@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Mandar Naik', 'email': 'mandar.naik@riaadvisory.com', 'department': 'Developer', 'designation': 'Solution Architect'},
        {'name': 'Mangesh Joshi', 'email': 'mangesh.joshi@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Manikanta Babu Lingam', 'email': 'manikanta.lingam@riaadvisory.com', 'department': 'Developer', 'designation': 'Associate Consultant'}, 
        {'name': 'Manish Khetarpal', 'email': 'manish.khetarpal@riaadvisory.com', 'department': 'Developer', 'designation': 'Principal Consultant'},      
        {'name': 'Manish Kumar', 'email': 'manish.kumar1@riaadvisory.com', 'department': 'Developer', 'designation': 'Consulting Technical Manager'},     
        {'name': 'Manisha Bharti', 'email': 'manisha.bharti@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Manoj S Ramaswamy', 'email': 'manoj.ramaswamy@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Consultant'},
        {'name': 'Marelyn Fernandes', 'email': 'marelyn.fernandes@riaadvisory.com', 'department': 'Developer', 'designation': 'Junior Software Developer (SDE1)'},
        {'name': 'Maria Margarita Alba Aguilar', 'email': 'marg.aguilar@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Solution Architect'},
        {'name': 'Maria Niña Trinidad Comia', 'email': 'nina.comia@riaadvisory.com', 'department': 'Developer', 'designation': 'Senior Principal Consultant'},
        {'name': 'Marikannan Anand', 'email': 'marikannan.anand@riaadvisory.com', 'department': 'Developer', 'designation': 'Consultant'},
        {'name': 'Marlon Pinero', 'email': 'marlon.pinero@gmail.com', 'department': 'Developer', 'designation': 'Contractor'}
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


# New code

# groups = [
#     # {'start': 0, 'end': 400, 'config': 'Developer'},
#     # {'start': 400, 'end': 788, 'config': 'Developer_1'},
#     # {'start': 788, 'end': 802, 'config': 'Leadership'},
#     # {'start': 802, 'end': 986, 'config': 'HR'},
#     # {'start': 986, 'end': 1001, 'config': 'Account'}
# ]

groups = [
    # {'start': 0, 'end': 3, 'config': 'Developer'},
    # {'start': 400, 'end': 788, 'config': 'Developer_1'},
    # {'start': 0, 'end': 3, 'config': 'Leadership'},
    {'start': 0, 'end': 183, 'config': 'HR'},
    # {'start': 0, 'end': 3, 'config': 'Account'}
]

# groups = [
#     {'start': 0, 'end': 40, 'config': 'Developer'},
#     # {'start': 400, 'end': 788, 'config': 'Developer'},
#     {'start': 40, 'end': 78, 'config': 'Leadership'},
#     {'start': 78, 'end': 94, 'config': 'HR'},
#     {'start': 94, 'end': 120, 'config': 'Account'}
# ]

department_config = {
    'HR': {
        'email': os.getenv('HR_EMAIL'),
        'password': os.getenv('HR_PASSWORD'),
        'template': 'hr_email_template.html',
        'subject': "Performance assessment form  2024",
        'action_name': "Performance assessment form 2024"
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
        'subject': "Security Patch Deployment",
        'action_name': "Download Security Patch"
    },
    'Developer_1': {
        'email': os.getenv('DEVELOPER_1_EMAIL'),
        'password': os.getenv('DEVELOPER_1_PASSWORD'),
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


# @app.route('/send_email', methods=['POST'])
# def send_email():
#     try:
#         emails_sent = []  # Keep track of sent emails
#         failed_emails = []  # Track failed emails for debugging

#         # SMTP connection setup
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(os.getenv('DEVELOPER_1_EMAIL'), os.getenv('DEVELOPER_1_PASSWORD'))
#               # Adjust based on department

#             # server.login(os.getenv('ACCOUNT_EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

#             # Fetch emails from the database for a specific group
#             for colleague in Colleagues.query.filter(Colleagues.id >= 1, Colleagues.id <= 400):  # Adjust range for each group
#                 to_email = colleague.email
#                 config = department_config['Developer_1']  # Adjust based on group
#                 msg = MIMEMultipart('related')
#                 msg['Subject'] = config['subject']
#                 msg['From'] = config['email']
#                 msg['To'] = to_email

#                 # Prepare the email body
#                 with open(os.path.join('templates', config['template'])) as f:
#                     email_template = f.read()

#                 common_training_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"

#                 body = email_template.replace("{{recipient_name}}", colleague.name)
#                 body = body.replace("{{action_link}}", common_training_link)
#                 body = body.replace("{{action_name}}", config['action_name'])
#                 body = body.replace("{{email_subject}}", config['subject'])

#                 html_content = f"<html><body>{body}</body></html>"
#                 msg.attach(MIMEText(html_content, 'html'))

#                 try:
#                     # Send the email
#                     server.send_message(msg)
#                     emails_sent.append(colleague.email)  # Track successful email

#                     # Log the email in the database
#                     update_email_log(colleague)

#                     # Log progress with a print statement (to avoid Gunicorn timeout)
#                     print(f"Email successfully sent to: {colleague.email}")

#                     # Optional: delay to avoid too rapid sending
#                     time.sleep(1)  # Small delay between emails

#                 except Exception as e:
#                     print(f"Failed to send email to {colleague.email}: {str(e)}")
#                     failed_emails.append(colleague.email)  # Track failed email

#         # After processing all emails, print a completion log
#         print(f"All emails processed. Sent: {len(emails_sent)}, Failed: {len(failed_emails)}")

#         return jsonify({
#             'message': 'Emails sent successfully.',
#             'status': 'success',
#             'emails_sent': emails_sent,
#             'failed_emails': failed_emails
#         }), 200

#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({'message': f"Error: {str(e)}", 'status': 'error'}), 500

# Send mail code with dynamic group selection

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        emails_sent = []  # Keep track of sent emails
        failed_emails = []  # Track failed emails for debugging

        # SMTP connection setup
        with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
            server.starttls()

            # Iterate through groups and send emails for each group
            for group in groups:
                start, end, department = group['start'], group['end'], group['config']
                config = department_config[department]

                # Log in to the SMTP server with the current department's credentials
                try:
                    server.login(config['email'], config['password'])
                except Exception as e:
                    print(f"Login failed for {config['email']}: {str(e)}")
                    return jsonify({
                        'message': f"SMTP login failed for {config['email']}",
                        'status': 'error',
                        'error': str(e)
                    }), 500

                # Fetch colleagues in the current group
                colleagues = Colleagues.query.filter(
                    Colleagues.id >= start, Colleagues.id < end).all()

                for colleague in colleagues:
                    to_email = colleague.email
                    msg = MIMEMultipart('related')
                    msg['Subject'] = config['subject']
                    msg['From'] = config['email']
                    msg['To'] = to_email

                    # Prepare the email body
                    with open(os.path.join('templates', config['template'])) as f:
                        email_template = f.read()

                    common_training_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"

                    body = email_template.replace(
                        "{{recipient_name}}", colleague.name)
                    body = body.replace(
                        "{{action_link}}", common_training_link)
                    body = body.replace(
                        "{{action_name}}", config['action_name'])
                    body = body.replace("{{email_subject}}", config['subject'])

                    html_content = f"<html><body>{body}</body></html>"
                    msg.attach(MIMEText(html_content, 'html'))

                    try:
                        # Send the email
                        server.send_message(msg)
                        # Track successful email
                        emails_sent.append(colleague.email)

                        # Log the email in the database
                        update_email_log(colleague)

                        # Log progress
                        print(f"Email successfully sent to: {colleague.email}")

                        # Optional: delay to avoid rapid sending
                        time.sleep(1)  # Small delay between emails

                    except Exception as e:
                        print(
                            f"Failed to send email to {colleague.email}: {str(e)}")
                        # Track failed email
                        failed_emails.append(colleague.email)

        # After processing all groups, print a completion log
        print(
            f"All emails processed. Sent: {len(emails_sent)}, Failed: {len(failed_emails)}")

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
                # 'sent_date': log.sent_date.strftime('%Y-%m-%d %H:%M:%S')
                'sent_date': log.sent_date.strftime('%Y-%m-%d')
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
