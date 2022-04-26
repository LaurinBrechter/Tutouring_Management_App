import ibm_db
import ibm_db_dbi
from genericpath import exists
import PySimpleGUI as sg

db_file = "database_conn.txt"
def conn_db_from_file():

    if exists("database_conn.txt"):
        try:
            dsn = open("database_conn.txt").read()
            conn = ibm_db.connect(dsn, "", "")
            server = ibm_db.server_info(conn)
            connected = True
            sg.popup("Connected to existing Database: {}".format(server.DB_NAME))
            pconn = ibm_db_dbi.Connection(conn)
        except:
            connected = False
            sg.popup("Failed Connecting to existing Database")
            pconn, conn = None, None
            
        
    else:
        sg.popup("No prior Database Information found")
        pconn, conn = None, None
        connected = False
        
    return connected, pconn, conn