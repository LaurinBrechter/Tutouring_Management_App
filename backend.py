from genericpath import exists
import PySimpleGUI as sg
import pandas as pd
import sqlite3
from datetime import datetime
import os
import sqlalchemy
import ibm_db
import ibm_db_dbi
from frontend import create_frontend
from connect_db import conn_db_from_file


password_path = "password.txt"
if exists(password_path):
    with open(password_path, "r") as f:
        passw = f.read()
        
    for i in range(3,0,-1):
        if passw == sg.popup_get_text("Please enter your password"):
            sg.popup("Passwort Correct")
            break
        else:
            sg.popup("Incorrect password, remaining tries: "+ str(i-1))
    else:
        quit()

else:
    password_init = sg.popup_get_text("Please set an initial password")
    with open(password_path, "w") as f:
        f.write(password_init)
    
# create the frontend for our app
window = create_frontend()

# try connecting to the Database once we start the app
connected, pcon, conn = conn_db_from_file()

print(pcon, conn)

# main event loop
while True:
    event,values = window.read()
    # give info about db connection
    print(event)
    if connected == True:
        print(ibm_db.active(conn))
    
    if event == "Save Database Info":
        db_conn_keys = ["dsn_driver", "dsn_database", "dsn_hostname", "dsn_port", "dsn_protocol", "dsn_uid" , "dsn_pwd", "dsn_security"]
        db_info = {i: values[i] for i in db_conn_keys}
        dsn = (
        "DRIVER={0};"
        "DATABASE={1};"
        "HOSTNAME={2};"
        "PORT={3};"
        "PROTOCOL={4};"
        "UID={5};"
        "PWD={6};"        
        "SECURITY={7};").format(*[db_info[i] for i in db_conn_keys])
        
        try:
            conn = ibm_db.connect(dsn, "", "")
            server = ibm_db.server_info(conn)
            connected = True
            pcon = ibm_db_dbi.Connection(conn)
            with open("tutouring_application\\database_conn.txt", "w") as f:
                f.write(dsn)
        except:
            connected = False
            
        if connected == True:
            sg.popup("Connected to Database: {}".format(server.DB_NAME))
        else:
            sg.popup("Failed connecting to New Database")
            connected, pcon, conn = conn_db_from_file()
    
    if event == sg.WIN_CLOSED or event == "Close":
        if connected == True:
            ibm_db.close(conn)
        break
    
    if event == "Submit" or event =="Save":
        print(values)
        sg.popup("Data saved!")
    
    
    if event == "Save Student":
        if connected == True:
            print(values)
            data = {i:values[i] for i in ["name", "hourly_rate", "platform", "type", "date_acquired"]}
            data["active"] = True
            print(data)
            
            try:
                float(data["hourly_rate"])
            
            # ins_query = "INSERT INTO STUDENTS_NEW VALUES ('Hanna', 18, 'Apprentus', 'Python', '2020-04-12', TRUE)"
                ins_query = f"INSERT INTO STUDENTS_NEW VALUES ('{data['name']}', '{data['hourly_rate']}', '{data['platform']}', '{data['type']}', '{data['date_acquired'].split()[0]}', TRUE)"
                print(ins_query)
                ibm_db.exec_immediate(conn, ins_query)
                
            except:
                window["hourly_rate"].update("Please enter a valid number.")
            
        else:
            sg.popup("Please first connect to the Database")
        
    if event == "Save Lesson":
        print(values)