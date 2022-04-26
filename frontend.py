import PySimpleGUI as sg

def create_frontend():


    new_student_tab = [
        [sg.Text("Please fill out the following details:")],
        [sg.Text("Name", size=(15,1)), sg.InputText(key="name")],
        [sg.Text("Hourly Rate", size=(15,1)), sg.InputText(key="hourly_rate")],
        [sg.Text("Platform", size=(15,1)), sg.InputText(key="platform")],
        [sg.Text("Type", size=(15,1)), sg.InputText(key="type")],
        # [sg.Text("Date Acquired", size=(15,1)), sg.InputText(key="Date Acquired")],
        [sg.CalendarButton('Select Date', close_when_date_chosen=True, no_titlebar=False), sg.Input("Date acquired", key='date_acquired', size=(15,1))],
        [sg.Button("Save Student")]
    ]


    new_lesson_tab = [
        [sg.Text("Please fill out information about the lesson.")], 
        [sg.Text("Name of Student", key=None), sg.Combo(["Marie", "Maria", "Yannick", "Christian"], key="Student Name")],
        [sg.Button("Save Lesson")] 
    ]


    db_conn_keys = ["dsn_driver", "dsn_database", "dsn_hostname", "dsn_port", "dsn_protocol", "dsn_uid" , "dsn_pwd", "dsn_security"]
    db_conn_tab = [[sg.Text(i, size=(10,1)), sg.InputText(key=i)] for i in db_conn_keys]


    tab_grp = [[sg.TabGroup([[
        sg.Tab("New Student", new_student_tab),
        sg.Tab("New Lesson", new_lesson_tab),
        sg.Tab("Database Connection Settings", db_conn_tab)
    ]]), sg.Button("Close"), sg.Button("Save Database Info")]]


    window = sg.Window("App", tab_grp)
    
    return window