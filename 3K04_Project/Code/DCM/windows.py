import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button
from numpy.core.fromnumeric import size

from users import Users
from pacemakers import Pacemakers

#################### Make a welcom window #####################
def create_welcome_window():
    sg.theme("DarkBlue1")
    col_login = [
        [sg.Text("Have an account?")],
        [sg.Button("Login", size=(10,2))]
    ]
    col_reg = [
        [sg.Text("New user?")],
        [sg.Button("Register", size=(10,2))]
    ]
    layout = [
        [sg.Text("Welcome to Group25 Pacemaker Monitor", justification="center", size=(40,2), font=("Any", 20, "bold"))],
        [sg.Column(col_login, justification="center"), sg.VSeperator(), sg.Column(col_reg, justification="center")],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Welcome", layout, finalize=True)
    
    return window

#################### Make a register window #####################
def create_register_window():
    sg.theme("DarkBlue1")

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  
        [sg.Text('Register', font='Any 15')],
        [TextLabel('User Name'), sg.Input(key='-USERNAME-')],
        [TextLabel('Password'),sg.Input(key='-PASSWORD-', password_char="*")],
        [TextLabel('Confirm Password'),sg.Input(key='-CPASSWORD-', password_char="*")],
        [sg.Button('Save'), sg.Button('Exit')]  
    ]

    window = sg.Window('Register', layout, finalize=True)

    return window

#################### Make a login window #####################
def create_login_window():
    sg.theme("DarkBlue1")

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  
        [sg.Text('Login', font='Any 15')],
        [TextLabel('User Name'), sg.Input(key='-USERNAME-')],
        [TextLabel('Password'),sg.Input(key='-PASSWORD-', password_char="*")],
        [sg.Button('Login'), sg.Button('Exit')]  
    ]

    window = sg.Window('Login', layout, finalize=True)

    return window

#################### Make a main window #####################
def create_main_window():
    sg.theme("DarkBlue1")
    def TextLabel(text): return sg.Text(text+':', justification='r', size=(25,1))
    # Status tab: review the parameters
    status_col_left = [
        [TextLabel("Pacing Mode"), sg.Text("N/A", key="-PM-")],
        [TextLabel("Lower Rate Limit(ppm)"), sg.Text("N/A", key="-LRL-")],
        [TextLabel("Atrial Amplitude(V)"), sg.Text("N/A", key="-AA-")],
        [TextLabel("Atrial Pulse Width(ms)"), sg.Text("N/A", key="-APW-")],
        [TextLabel("Atrial Sensitivity(mV)"), sg.Text("N/A", key="-AS-")],
        [TextLabel("ARP(ms)"), sg.Text("N/A", key="-ARP-")]
    ]
    status_col_right = [
        [TextLabel("AV Delay(ms)"), sg.Text("N/A", key="-AVD-")],
        [TextLabel("Upper Rate Limit(ppm)"), sg.Text("N/A", key="-URL-")],
        [TextLabel("Ventricular Amplitude(V)"), sg.Text("N/A", key="-VA-")],
        [TextLabel("Ventricular Pulse Width(ms)"), sg.Text("N/A", key="-VPW-")],
        [TextLabel("Ventricular Sensitivity(mV)"), sg.Text("N/A", key="-VS-")],
        [TextLabel("VRP(ms)"), sg.Text("N/A", key="-VRP-")]
    ]
    # egram_col = [
    #     [sg.Button("Atrial")],
    #     [sg.Button("Ventricle")],
    #     [sg.Button("Both")]
    # ]
    status_tab = [
        [sg.Column(status_col_left, justification="c"), sg.VSeparator(), sg.Column(status_col_right, justification="c")],
        [sg.Text("Rate Adaptive Paramters", justification="c", text_color="lightblue")],
        [TextLabel("Maximum Sensor Rate"), sg.Text("N/A", key="-MSR-")],
        [TextLabel("Activity Threshold"), sg.Text("N/A", key="-ATH-")],
        [TextLabel("Reaction Time(s)"), sg.Text("N/A", key="-RAT-")],
        [TextLabel("Response Factor"), sg.Text("N/A", key="-RF-")],
        [TextLabel("Recovery Time(min)"), sg.Text("N/A", key="-RCT-")],
        [TextLabel("Egram"), sg.Button("Atrial"), sg.Button("Ventricle"), sg.Button("Both")],
        [sg.Button("Get Parameters")]
    ]

    # Modification tab: modify the parameters
    mod_col_left = [
        [TextLabel("Pacing Mode"), sg.Input(key="-PM_IN-"), sg.Listbox(Pacemakers.MODE, size=(20,4), enable_events=True, key="-PM_IN_LIST-")],
        [TextLabel("Lower Rate Limit(ppm)"), sg.Input("60", key="-LRL_IN-")],
        [TextLabel("Atrial Amplitude(V)"), sg.Input("5", key="-AA_IN-")],
        [TextLabel("Atrial Pulse Width(ms)"), sg.Input("1", key="-APW_IN-")],
        [TextLabel("Atrial Sensitivity(mV)"), sg.Input(key="-AS_IN-")],
        [TextLabel("ARP(ms)"), sg.Input("250", key="-ARP_IN-")]
    ]
    mod_col_right = [
        [TextLabel("AV Delay(ms)"), sg.Input("150", key="-AVD_IN-")],
        [TextLabel("Upper Rate Limit(ppm)"), sg.Input("120", key="-URL_IN-")],
        [TextLabel("Ventricular Amplitude(V)"), sg.Input("5", key="-VA_IN-")],
        [TextLabel("Ventricular Pulse Width(ms)"), sg.Input("1", key="-VPW_IN-")],
        [TextLabel("Ventricular Sensitivity(mV)"), sg.Input(key="-VS_IN-")],
        [TextLabel("VRP(ms)"), sg.Input("320", key="-VRP_IN-")]
    ]
    mod_tab = [
        [sg.Column(mod_col_left, justification="c"), sg.VSeparator(), sg.Column(mod_col_right, justification="c")],
        [sg.Text("Rate Adaptive Paramters", justification="c", text_color="lightblue")],
        [TextLabel("Maximum Sensor Rate"), sg.Input("120", key="-MSR_IN-")],
        [TextLabel("Activity Threshold"), sg.Input(key="-ATH_IN-")],
        [TextLabel("Reaction Time(s)"), sg.Input("30", key="-RAT_IN-")],
        [TextLabel("Response Factor"), sg.Input("8", key="-RF_IN-")],
        [TextLabel("Recovery Time(min)"), sg.Input("5", key="-RCT_IN-")],
        [sg.Button("Save")],
        [sg.Button("Set Parameters")]
    ]

    # make window
    layout = [
        [sg.TabGroup(
            [[
                sg.Tab("Status", status_tab, key="-STAT-", element_justification="c"),
                sg.Tab("Modify", mod_tab, key="-MOD-", element_justification="c")
            ]],
            key="-MAIN-", title_color="red", selected_title_color="green",
            tab_location="top"
        )],
        [TextLabel("Communication"), sg.Text("OFF", key="-COM-"), sg.Button("Connect")],
        [TextLabel("Username"), sg.Text("N/A", key="-NAME-")],
        [sg.Button("Exit")]
    ]

    window = sg.Window("DCM G25", layout, finalize=True)

    return window

def create_egram_window():
    sg.theme("DarkBlue1")

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  
        [sg.Canvas(size=(640, 480), key='-CANVAS-')],
        [sg.Button('Start', size=(30, 1), pad=((280, 0), 3), font='Helvetica 14')],
        [sg.Button('Exit', size=(15, 1), pad=((280, 0), 3), font='Helvetica 14')]
    ]

    window = sg.Window('Egram', layout, finalize=True)

    return window

# def create_p_register_win():
#     sg.theme("DarkBlue1")
#     def TextLabel(text): return sg.Text(text+':', justification='r', size=(25,1))
#     col_left = [
#         [TextLabel("Pacing Mode"), sg.Input(key="-PM_IN-"), sg.Listbox(Pacemakers.MODE, size=(20,4), enable_events=True, key="-PM_IN_LIST-")],
#         [TextLabel("Lower Rate Limit(ppm)"), sg.Input(key="-LRL_IN-")],
#         [TextLabel("Atrial Amplitude(V)"), sg.Input(key="-AA_IN-")],
#         [TextLabel("Atrial Pulse Width(ms)"), sg.Input(key="-APW_IN-")],
#         [TextLabel("ARP(ms)"), sg.Input(key="-ARP_IN-")]
#     ]
#     col_right = [
#         [TextLabel("Pacemaker Name"), sg.Text(key="-PN_IN-")],
#         [sg.Text("")],
#         [TextLabel("Upper Rate Limit(ppm)"), sg.Input(key="-URL_IN-")],
#         [TextLabel("Ventricular Amplitude(V)"), sg.Input(key="-VA_IN-")],
#         [TextLabel("Ventricular Pulse Width(ms)"), sg.Input(key="-VPW_IN-")],
#         [TextLabel("VRP(ms)"), sg.Input(key="-VRP_IN-")]
#     ]

#     layout = [
#         [sg.Column(col_left, justification="c"), sg.VSeparator(), sg.Column(col_right, justification="c")],
#         [sg.Button("Register"), sg.Button("Cancel")]
#     ]

#     window = sg.Window("Register a new pacemaker", layout, finalize=True)

#     return window




if __name__ == "__main__":
    window = create_main_window()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
    window.close()
