import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import popup
from numpy import ModuleDeprecationWarning

from windows import *
from users import Users
from pacemakers import Pacemakers
from egram import Egram


def main():
    welcome_win = create_welcome_window()
    login_win = None
    register_win = None
    main_win = None
    egram_win = None
    users = Users()
    pacemakers = Pacemakers()

    while True:
        window, event, values = sg.read_all_windows()
        # print(window, event, values)
        if window == welcome_win:
            if event in (sg.WIN_CLOSED, "Exit"):
                break
            elif event == "Login":
                welcome_win.hide()
                login_win = create_login_window()
            elif event == "Register":
                welcome_win.hide()
                register_win = create_register_window()

        if window == login_win:
            if event in (sg.WIN_CLOSED, "Exit"):
                login_win.close()
                login_win = None
                welcome_win.un_hide()
            elif event == "Login":
                if users.login(values):
                    # Go to main window
                    sg.popup("Going to main window...")
                    login_win.close()
                    login_win = None
                    main_win = create_main_window()
                    main_win["-NAME-"].update(users.get_active()["username"])

        if window == register_win:
            if event in (sg.WIN_CLOSED, "Exit"):
                register_win.close()
                register_win = None
                welcome_win.un_hide()
            elif event == "Save":
                if values["-CPASSWORD-"] != values["-PASSWORD-"]:
                    sg.popup("Inconsistent password", background_color="red", text_color="darkblue")
                    continue
                if users.register(values):
                    # Go to main window
                    sg.popup("Going to main window...")
                    register_win.close()
                    register_win = None
                    main_win = create_main_window()
                    user_active = users.get_active()
                    main_win["-NAME-"].update(user_active["username"])
                    

        if window == main_win:
            if event in (sg.WIN_CLOSED, "Exit"):
                main_win.close()
                main_win = None
                welcome_win.un_hide()

            if event == "Connect":
                main_win["-COM-"].update("ON")
                # params = pacemakers.get_param()
                params = pacemakers.get_param_com()
                print(params)
                for key in params:
                    main_win[key].update(params[key] if params[key] else "N/A")

            if event == "-PM_IN_LIST-":
                main_win["-PM_IN-"].update(values["-PM_IN_LIST-"][0])

            if event == "Save":
                # print(values)
                if pacemakers.set_param(values):
                    params = pacemakers.get_param()
                    for key in params:
                        main_win[key].update(params[key] if params[key] else "N/A")
                    sg.popup("Saved!")
            
            if event == "Get Parameters":
                params = pacemakers.get_param_com()
                for key in params:
                    main_win[key].update(params[key] if params[key] else "N/A")
            
            if event == "Set Parameters":
                pacemakers.set_param_com()
                sg.popup("Sent parameters!")
        
            if event in ("Atrial", "Ventricle", "Both"):
                main_win.hide()
                egram_win = create_egram_window()
                mode = event
                
                
        if window == egram_win:
            canvas = egram_win["-CANVAS-"].TKCanvas
            egram = Egram(canvas, mode)
            while True:
                event_e, value_e = egram_win.read(timeout=1)
                if event_e in (sg.WIN_CLOSED, "Exit"):
                    break
                egram.draw_graph()
            egram_win.close()
            egram_win = None
            main_win.un_hide()
                
               


    welcome_win.close()            

if __name__ == "__main__":
    main()
