import socket
import os
from DataBase import savePatient
from werkzeug.security import generate_password_hash,check_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Admin:admin@aubcovax.h441n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

DataBase = client["DataBase"]
MedicalPersonnel = DataBase["Medical Personnel"]
Patient = DataBase["Patient"]
Admin = DataBase["Admin"]
IP = "0.0.0.0"
Port   = 8000
bufferSize  = 1024
Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
Socket.bind((IP, Port))
while(True):
    action = Socket.recvfrom(bufferSize)[0]
    type = Socket.recvfrom(bufferSize) 
    if(action.decode() == "Sign In"):
        username = Socket.recvfrom(bufferSize)[0]
        password = Socket.recvfrom(bufferSize)[0]
        if(type[0].decode() == "Admin"):
            if (Admin.count_documents({"username": username.decode()}) == 0):
                    Socket.sendto(str.encode("This username doesn't exist"),type[1]) 
            else:
                user = Admin.find_one({"username":username.decode()})
                if (check_password_hash(user["password"],password.decode())==True):
                    Socket.sendto(str.encode("LogIn Successful"),type[1])
                else:
                    Socket.sendto(str.encode("Incorrect Password"),type[1])
        elif(type[0].decode() == "Medical Personnel"):
            if (MedicalPersonnel.count_documents({"username": username.decode()}) == 0):
                Socket.sendto(str.encode("This username doesn't exist"),type[1])
            else:
                user = MedicalPersonnel.find_one({"username": username.decode()})
                if (check_password_hash(user["password"],password.decode())==True):
                    Socket.sendto(str.encode("LogIn Successful"),type[1])
                else:
                    Socket.sendto(str.encode("Incorrect Password"),type[1])
        elif(type[0].decode() == "Patient"):
            if (Patient.count_documents({"username": username.decode()}) == 0):
                Socket.sendto(str.encode("This username doesn't exist"),type[1])
            else:
                user = Patient.find_one({"username": username.decode()})
                if (check_password_hash(user["password"],password.decode())==True):
                    Socket.sendto(str.encode("LogIn Successful"),type[1])
                else:
                    Socket.sendto(str.encode("Incorrect Password"),type[1])
    elif(action.decode()=="Sign Up"):
        username = Socket.recvfrom(bufferSize)[0]
        password = Socket.recvfrom(bufferSize)[0]
        fullName = Socket.recvfrom(bufferSize)[0]
        birthDate = Socket.recvfrom(bufferSize)[0]
        ID = Socket.recvfrom(bufferSize)[0]
        phoneNumber = Socket.recvfrom(bufferSize)[0]
        email = Socket.recvfrom(bufferSize)[0]
        location = Socket.recvfrom(bufferSize)[0]
        medicalConditions = Socket.recvfrom(bufferSize)[0]
        if (Patient.count_documents({"username": username.decode()}) != 0):
            Socket.sendto(str.encode("This username already exists!"),type[1])
        else:
            savePatient(fullName.decode(), birthDate.decode(), ID.decode(),
                        phoneNumber.decode(), email.decode(), location.decode(),
                        medicalConditions.decode(), username.decode(), password.decode())
            Socket.sendto(str.encode("Sign Up Successful"),type[1])
    #elif(action.decode()=="Forgot Password"): optional/implement later if we still have time
    else:
        Socket.sendto(str.encode("Invalid request"),type[1])
#elif(sendAvailableTimeout):
    #implement TimeSlots and Admin/Personnel Access Pages
