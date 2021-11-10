from werkzeug.security import generate_password_hash,check_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Admin:admin@aubcovax.h441n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

DataBase = client["DataBase"]
MedicalPersonnel = DataBase["Medical Personnel"]
Patient = DataBase["Patient"]
Admin = DataBase["Admin"]

def saveMedicalPersonnel(username, password, email):
    password_encrypted = generate_password_hash(password)  # reference to https://blog.teclado.com/learn-python-encrypting-passwords-python-flask-and-passlib/ for implementing how to encrypt the passwords in the database
    MedicalPersonnel.insert_one({'username': username, 'Email': email, 'password': password_encrypted})


def savePatient(fullName, birthDate, ID, phoneNumber, email, location, medicalConditions, username, password):
    password_encrypted = generate_password_hash(password)
    Patient.insert_one(
        {'username': username, 'password': password_encrypted, 'Birth Date': birthDate, 'ID Card Number': ID,
         'Phone Number': phoneNumber, 'Email': email, 'Location': location, 'Medical Conditions': medicalConditions})
def saveAdmin(username, password):
    password_encrypted = generate_password_hash(password)
    Admin.insert_one(
        {'username': username, 'password': password_encrypted})
print(os.environ.get('PORT', 8000))