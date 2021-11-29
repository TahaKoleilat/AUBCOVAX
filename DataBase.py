from werkzeug.security import generate_password_hash,check_password_hash
from pymongo import MongoClient
import smtplib
from datetime import datetime, timedelta,date
import pytz
from email.mime.text import MIMEText

client = MongoClient("mongodb+srv://Admin:admin@aubcovax.h441n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

DataBase = client["DataBase"]
MedicalPersonnel = DataBase["Medical Personnel"]
Patient = DataBase["Patient"]
Admin = DataBase["Admin"]
TimeSlots= DataBase["TimeSlots"]
def saveMedicalPersonnel(fullName,username, password, email, ID, PhoneNumber):
    password_encrypted = generate_password_hash(password)  # reference to https://blog.teclado.com/learn-python-encrypting-passwords-python-flask-and-passlib/ for implementing how to encrypt the passwords in the database
    MedicalPersonnel.insert_one({'Full name': fullName, 'Phone Number' : PhoneNumber,'username': username, 'Email': email, 'password': password_encrypted, 'ID': ID})
def savePatient(fullName, birthDate, ID, phoneNumber, email, location, medicalConditions, username, password, dose_1,dose_2):
    password_encrypted = generate_password_hash(password)
    Patient.insert_one(
        {'Full name': fullName,'username': username, 'password': password_encrypted, 'Birth Date': birthDate, 'ID': ID,
         'Phone Number': phoneNumber, 'Email': email, 'Location': location, 'Medical Conditions': medicalConditions, 'Dose 1': dose_1, 'Dose 2': dose_2})
def saveAdmin(username, password):
    password_encrypted = generate_password_hash(password)
    Admin.insert_one(
        {'username': username, 'password': password_encrypted})
#got help from https://www.youtube.com/watch?v=Y_tnWTjTfzY and https://stackoverflow.com/questions/39540043/how-to-add-a-subject-to-an-email-being-sent-with-gmail for sending an email through python
def send_mail_dose1(sender,password,receiver,receiver_name,timeslot,subject):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(sender,password)
    message = MIMEText('Dear ' + receiver_name + ",\n\n" + "You have been assigned the following timeslot for your dose 1: " + timeslot + '\n\n' + "Thank you for registering on the AUBCOVAX app!")
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    server.sendmail(sender,receiver,message.as_string())
    server.quit()
def send_mail_dose2(sender,password,receiver,receiver_name,timeslot,subject):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(sender,password)
    message = MIMEText('Dear ' + receiver_name + ",\n\n" + "You have been assigned the following timeslot for your dose 2: " + timeslot + '\n\n')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    server.sendmail(sender,receiver,message.as_string())
    server.quit()
def send_mail_cert(sender,password,receiver,receiver_name,timeslot,subject):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(sender,password)
    message = MIMEText('Dear ' + receiver_name + ",\n\n" + "You have successfully completed your vaccination. Kindly find attached your certificate")
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    server.sendmail(sender,receiver,message.as_string())
    server.quit()
def timeslot_dose():
    tz_BEY = pytz.timezone('Asia/Beirut') 
    datetime_BEY = datetime.now(tz_BEY)
    hour = datetime_BEY.hour
    date_1 = date(day=datetime_BEY.today().day, month=datetime_BEY.today().month,year=datetime_BEY.today().year)
    minutes = datetime_BEY.minute
    if(hour > 17 or (hour == 17 and minutes > 30)):
        end_date = date_1 + timedelta(days=1)
        while(TimeSlots.count_documents({"Day":end_date.day}) > 20):
            end_date = end_date + timedelta(days=1)
        if(TimeSlots.count_documents({"Day":end_date.day}) == 0):
            time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":8,"Minutes":00,"TimeType":"AM"}
            TimeSlots.insert_one(time)
            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+ "8:00 AM")
        else:
            previous_user = TimeSlots.find_one({"Day":end_date.day,"Month":end_date.month,"Year":end_date.year},sort=[("Hour", -1),("Minutes",-1),("Day",-1),("Month",-1),("Year",-1)])
            time_slot = datetime(year = end_date.year,month = end_date.month,day = end_date.month,hour=previous_user["Hour"],minute=previous_user["Minutes"]) + timedelta(minutes=30)
            if(time_slot.hour<=12):
                if(time_slot.hour == 12):
                    time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"PM"}
                else:
                    time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"AM"}
                TimeSlots.insert_one(time)
                if(time["Minutes"] == 0):
                    x = str(time["Minutes"]) +"0"
                    return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+ x + " "+ time["TimeType"])
                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
            else:
                time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"PM"}
                TimeSlots.insert_one(time)
                if(time["Minutes"] == 0):
                    x = str(time["Minutes"]) +"0"
                    return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+x+ " "+ time["TimeType"])
                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+str(time["Minutes"])+ " "+ time["TimeType"])
    else:
        if(TimeSlots.count_documents({"Day":date_1.day}) < 20):
            if(TimeSlots.count_documents({"Day":date_1.day}) == 0):
                time = {"Month":date_1.month,"Day":date_1.day,"Year":date_1.year,"Hour":8,"Minutes":00}
                TimeSlots.insert_one(time)
                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+ "8:00 AM")
            else:
                now = datetime.now(tz_BEY)
                round = time_ceil(now.hour,now.minute)
                round = round.split(".")
                rounded_hour = int(round[0])
                rounded_minute = int(round[1])
                end_slot = datetime(hour = rounded_hour,year = date_1.year,month=date_1.month,minute=rounded_minute,day=date_1.day)
                while(TimeSlots.count_documents({"Hour":end_slot.hour,"Minutes":end_slot.minute,"Year":date_1.year,"Month":date_1.month,"Day":date_1.day})!=0):
                    if(end_slot.hour == 18):
                        break
                    end_slot = end_slot + timedelta(minutes=30)
                if(end_slot.hour ==18):
                    end_date = date_1 + timedelta(days=1)
                    while(TimeSlots.count_documents({"Day":end_date.day}) > 20):
                        end_date = date_1 + timedelta(days=1)
                    if(TimeSlots.count_documents({"Day":end_date.day}) == 0):
                        time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":8,"Minutes":00,"TimeType":"AM"}
                        TimeSlots.insert_one(time)
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+ "8:00 AM")
                    else:
                        previous_user = TimeSlots.find_one({"Day":end_date.day,"Month":end_date.month,"Year":end_date.year},sort=[("Hour", -1),("Minutes",-1),("Day",-1),("Month",-1),("Year",-1)])
                        time_slot = datetime(year = end_date.year,month = end_date.month,day = end_date.month,hour=previous_user["Hour"],minute=previous_user["Minutes"]) + timedelta(minutes=30)
                        if(time_slot.hour<12):
                            time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"AM"}
                            TimeSlots.insert_one(time)
                            if(time["Minutes"] == 0):
                                x = str(time["Minutes"]) +"0"
                                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+ x + " "+ time["TimeType"])
                            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                        elif(time_slot.hour == 12):
                            time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"PM"}
                            TimeSlots.insert_one(time)
                            if(time["Minutes"] == 0):
                                x = str(time["Minutes"]) +"0"
                                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+ x + " "+ time["TimeType"])
                            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                        else:
                            time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"PM"}
                            TimeSlots.insert_one(time)
                            if(time["Minutes"] == 0):
                                x = str(time["Minutes"]) +"0"
                                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+x+ " "+ time["TimeType"])
                            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                else:
                    if(end_slot.hour<12):
                        time = {"Month":date_1.month,"Day":date_1.day,"Year":date_1.year,"Hour":end_slot.hour,"Minutes":end_slot.minute,"TimeType":"AM"}
                        TimeSlots.insert_one(time)
                        if(time["Minutes"] == 0):
                            x = str(time["Minutes"]) +"0"
                            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+ x + " "+ time["TimeType"])
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                    elif(end_slot.hour == 12):
                        time = {"Month":date_1.month,"Day":date_1.day,"Year":date_1.year,"Hour":end_slot.hour,"Minutes":end_slot.minute,"TimeType":"PM"}
                        TimeSlots.insert_one(time)
                        if(time["Minutes"] == 0):
                            x = str(time["Minutes"]) +"0"
                            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+ x + " "+ time["TimeType"])
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                    else:
                        time = {"Month":date_1.month,"Day":date_1.day,"Year":date_1.year,"Hour":end_slot.hour,"Minutes":end_slot.minute,"TimeType":"PM"}
                        TimeSlots.insert_one(time)
                        if(time["Minutes"] == 0):
                            x = str(time["Minutes"]) +"0"
                            return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+x+ " "+ time["TimeType"])
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+str(time["Minutes"])+ " "+ time["TimeType"])
        else:
            end_date = date_1 + timedelta(days=1)
            while(TimeSlots.count_documents({"Day":end_date.day}) > 20):
                end_date = date_1 + timedelta(days=1)
            if(TimeSlots.count_documents({"Day":end_date.day}) == 0):
                time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":8,"Minutes":00}
                TimeSlots.insert_one(time)
                return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+ "8:00 AM")
            else:
                previous_user = TimeSlots.find_one({"Day":end_date.day,"Month":end_date.month,"Year":end_date.year},sort=[("Hour", -1),("Minutes",-1),("Day",-1),("Month",-1),("Year",-1)])
                time_slot = datetime(year=end_date.year,month=end_date.month,day=end_date.day,hour=previous_user["Hour"],minute=previous_user["Minutes"]) + timedelta(minutes=30)
                if(time_slot.hour<12):
                    time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"AM"}
                    TimeSlots.insert_one(time)
                    if(time["Minutes"] == 0):
                        x = str(time["Minutes"]) +"0"
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+x+ " "+ time["TimeType"])
                    return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                elif(time_slot.hour == 12):
                    time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"PM"}
                    TimeSlots.insert_one(time)
                    if(time["Minutes"] == 0):
                        x = str(time["Minutes"]) +"0"
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+x+ " "+ time["TimeType"])
                    return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"])+":"+str(time["Minutes"])+ " "+ time["TimeType"])
                else:
                    time = {"Month":end_date.month,"Day":end_date.day,"Year":end_date.year,"Hour":time_slot.hour,"Minutes":time_slot.minute,"TimeType":"PM"}
                    TimeSlots.insert_one(time)
                    if(time["Minutes"] == 0):
                        x = str(time["Minutes"]) +"0"
                        return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+x+ " "+ time["TimeType"])
                    return date(day=time["Day"], month=time["Month"], year=time["Year"]).strftime('%A %d %B %Y') + str(" at "+str(time["Hour"]-12)+":"+str(time["Minutes"])+ " "+ time["TimeType"])
def time_ceil(hour,minute):
    if(0<= minute <=30):
        rounded_time = str(hour)+"."+"30"
    elif(30 < minute <= 59):
        rounded_time = str(hour+1)+"."+"00"
    return rounded_time
def compare_time(date1):
    tz_BEY = pytz.timezone('Asia/Beirut') 
    datetime_BEY = datetime.now(tz_BEY)
    datetime_object = datetime.strptime(date1, '%A %d %B %Y at %I:%M %p')
    if(datetime_object.replace(tzinfo=None) < datetime_BEY.replace(tzinfo=None)):
        return "lower"
    else:
        return "higher"
