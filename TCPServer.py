import socket, threading
import socket
import os
from DataBase import savePatient, send_mail_dose1,send_mail_dose2,send_mail_cert, timeslot_dose, compare_time
from werkzeug.security import generate_password_hash,check_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Admin:admin@aubcovax.h441n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

DataBase = client["DataBase"]
MedicalPersonnel = DataBase["Medical Personnel"]
Patient = DataBase["Patient"]
Admin = DataBase["Admin"]
Timeslot= DataBase["TimeSlots"]
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,Socket,bufferSize):
        threading.Thread.__init__(self)
        self.Socket = Socket
        self.bufferSize = bufferSize
        print ("New connection added: ", clientAddress)
    def run(self):
        data = self.Socket.recv(self.bufferSize).decode("utf-8")
        data = data.split("$")
        action = data[0]
        type = data[1]
        if(action == "Sign In"):
            username = data[2]
            password = data[3]
            if(type == "Admin"):
                if (Admin.count_documents({"username": username}) == 0):
                        self.Socket.send(str.encode("This username doesn't exist")) 
                else:
                    user = Admin.find_one({"username":username})
                    if (check_password_hash(user["password"],password)==True):
                        self.Socket.send(str.encode("LogIn Successful"))
                    else:
                        self.Socket.send(str.encode("Incorrect Password"))
            elif(type == "Medical Personnel"):
                if (MedicalPersonnel.count_documents({"username": username}) == 0):
                    self.Socket.send(str.encode("This username doesn't exist"))
                else:
                    user = MedicalPersonnel.find_one({"username": username})
                    if (check_password_hash(user["password"],password)==True):
                        self.Socket.send(str.encode("LogIn Successful"))
                    else:
                        self.Socket.send(str.encode("Incorrect Password"))
            elif(type == "Patient"):
                if (Patient.count_documents({"username": username}) == 0):
                    self.Socket.send(str.encode("This username doesn't exist"))
                else:
                    user = Patient.find_one({"username": username})
                    if (check_password_hash(user["password"],password)==True):
                        self.Socket.send(str.encode("LogIn Successful"))
                    else:
                        self.Socket.send(str.encode("Incorrect Password"))
        elif(action=="Sign Up"):
            username = data[2]
            password = data[3]
            fullName = data[4]
            birthDate = data[5]
            ID = data[6]
            phoneNumber = data[7]
            email = data[8]
            location = data[9]
            medicalConditions = data[10]
            if (Patient.count_documents({"username": username}) != 0):
                self.Socket.send(str.encode("This username already exists!"))
            else:
                timeslot = timeslot_dose()
                savePatient(fullName, birthDate, ID,
                            phoneNumber, email, location,
                            medicalConditions, username, password,timeslot,"")
                self.Socket.send(str.encode("Sign Up Successful"))
                send_mail_dose1("AUBCOVAX@gmail.com","AUBCOVAX123@#", email,fullName,timeslot,"AUBCOVAX Dose 1 Date Confirmation")
        #elif(action=="Forgot Password"): optional/implement later if we still have time
        elif(action == "Search"):
            search_object = data[2]
            if(type == "Admin"):
                if (Patient.count_documents({"Full name": search_object}) == 0 and Patient.count_documents({"Phone Number": search_object}) == 0):
                    if (MedicalPersonnel.count_documents({"Full name": search_object}) == 0 and MedicalPersonnel.count_documents({"ID": search_object}) == 0):
                        self.Socket.send(str.encode("This Person doesn't exist"))
                if(MedicalPersonnel.count_documents({"Full name": search_object}) != 0):
                    user = MedicalPersonnel.find_one({"Full name":search_object})
                    self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "ID: " + user["ID"] + "\n\n" + "Email: " + user["Email"] + "\n\n" + "Phone Number: " + user["Phone Number"] + "\n\n")) 
                if(MedicalPersonnel.count_documents({"ID": search_object}) != 0):
                    user = MedicalPersonnel.find_one({"ID": search_object})
                    self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "ID: " + user["ID"] + "\n\n" + "Email: " + user["Email"] + "\n\n" + "Phone Number: " + user["Phone Number"] + "\n\n" )) 
                elif(Patient.count_documents({"Full name": search_object}) != 0):
                    user = Patient.find_one({"Full name":search_object})
                    self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "ID: " + user["ID"] + "\n\n" + "Email: " + user["Email"] + "\n\n" + "Phone Number: " + user["Phone Number"] + "\n\n" +  "Location: " + user["Location"] + "\n\n" + "Birth Date: " + user["Birth Date"] + "\n\n" + "Medical Conditions: " + user["Medical Conditions"] + "\n\n" + "Dose 1: " + user["Dose 1"] + "\n\n" + "Dose 2: " + user["Dose 2"] + "\n\n" )) 
                elif(Patient.count_documents({"Phone Number": search_object}) != 0):
                    user = Patient.find_one({"Phone Number":search_object})
                    self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "ID: " + user["ID"] + "\n\n" + "Email: " + user["Email"] + "\n\n" + "Phone Number: " + user["Phone Number"] + "\n\n" +  "Location: " + user["Location"] + "\n\n" + "Birth Date: " + user["Birth Date"] + "\n\n" + "Medical Conditions: " + user["Medical Conditions"] + "\n\n" + "Dose 1: " + user["Dose 1"] + "\n" + "Dose 2: " + user["Dose 2"] + "\n\n")) 
            elif(type == "Personnel"):
                if(Patient.count_documents({"Phone Number": search_object}) == 0):
                    self.Socket.send(str.encode("This patient doesn't exist!")) 
                else:
                    user = Patient.find_one({"Phone Number":search_object})
                    self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "Dose 1: " + user["Dose 1"] + "\n\n"+ "Dose 2: " + user["Dose 2"] + "\n\n" )) 
            elif(type =="Patient"):
                user = Patient.find_one({"username":search_object})
                self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "Username: " + user["username"] + "\n\n"+ "ID: " + user["ID"] + "\n\n" + "Email: " + user["Email"] + "\n\n" + "Phone Number: " + user["Phone Number"] + "\n\n" +  "Location: " + user["Location"] + "\n\n" + "Birth Date: " + user["Birth Date"] + "\n\n" + "Medical Conditions: " + user["Medical Conditions"] + "\n\n" + "Dose 1: " + user["Dose 1"] + "\n\n" + "Dose 2: " + user["Dose 2"] + "\n\n" ))    
        elif(action == "Book"):
            search_object = data[2]
            user = Patient.find_one({"Phone Number":search_object})
            if(user["Dose 2"] != ""):
                self.Socket.send(str.encode("This patient already took Dose 2!"))
            elif(compare_time(user["Dose 1"]) == "higher"):
                self.Socket.send(str.encode("This patient didn't take Dose 1 yet!"))
            else:
                timeslot = timeslot_dose()
                parameter = {"Phone Number": search_object}
                new = { "$set": { "Dose 2": timeslot }}
                Patient.update_one(parameter, new)
                user = Patient.find_one({"Phone Number":search_object})
                self.Socket.send(str.encode("Full Name: " + user["Full name"] + "\n\n" + "Dose 1: " + user["Dose 1"] + "\n\n"+ "Dose 2: " + user["Dose 2"] + "\n\n" )) 
                send_mail_dose2("AUBCOVAX@gmail.com","AUBCOVAX123@#", user["Email"],user["Full name"],timeslot,"AUBCOVAX Dose 2 Date Confirmation")
        self.Socket.close()
IP = "0.0.0.0"
PORT = 3389
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock,1024)
    newthread.start()
