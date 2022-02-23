import PySimpleGUI as sg
from json import (load as jsonload, dump as jsondump)
from os import path

"""
    Users information management module. Save and load users information for login and register.
"""
class Users:
    USERS_FILE = path.join(path.dirname(__file__), r'users.json')
    DEFAULT_USER = {'username': 'admin', 'password': 'admin'}
    # "Map" from the user dictionary keys to the window's element keys
    USER_KEYS_TO_ELEMENT_KEYS = {'username': '-USERNAME-', 'password': '-PASSWORD-'}

    users_active = {}
    # Singleton
    _users_inst = None    
    def __new__(cls):
        if cls._users_inst is None:
            cls._users_inst = super(Users, cls).__new__(cls)
            cls._users_inst.load_users(cls.USERS_FILE, cls.DEFAULT_USER)
        return cls._users_inst

    ##################### Load/Save Users File #####################
    def load_users(self, users_file, default_user):
        try:
            with open(users_file, 'r') as f:
                self.info = jsonload(f)
        except Exception as e:
            sg.popup_quick_message(f'exception {e}', 'No users file found... will create one for you', keep_on_top=True, background_color='red', text_color='darkblue')
            self.info = [default_user]
            self.save_users(users_file)

    def save_users(self, users_file):
        with open(users_file, 'w') as f:
            jsondump(self.info, f, indent=4)

    def get_active(self):
        return self.users_active

    def login(self, values):
        user = {key : values[self.USER_KEYS_TO_ELEMENT_KEYS[key]] 
                for key in self.USER_KEYS_TO_ELEMENT_KEYS 
                if values}
        for existing_user in self.info:
            if user["username"] == existing_user["username"] and user["password"] == existing_user["password"]:
                self.users_active = existing_user
                return True        
        sg.popup("Please try again.", background_color="red", text_color="darkblue")
        return False

    def register(self, values):
        # check maximum users
        if len(self.info) > 9:
            sg.popup("No more users can be registered.", background_color="red", text_color="darkblue")
            return False
        if values:      # if there are stuff specified by another window, fill in those values
            # check empty entries
            if not all(values.values()):
                sg.popup("Entries can't be empty.", background_color="red", text_color="darkblue")
                return False
            new_user = {}
            for key in self.USER_KEYS_TO_ELEMENT_KEYS:
                try:
                    value = values[self.USER_KEYS_TO_ELEMENT_KEYS[key]]
                    # check duplicate names
                    if key == "username" and any([value == user["username"] for user in self.info]):
                        sg.popup("Name already existed.", background_color="red", text_color="darkblue")
                        return False
                    new_user[key] = value
                except Exception as e:
                    print(f'Problem saving user from window values. Key = {key}')
        if new_user:
            self.users_active = new_user
            self.info.append(new_user)
            self.save_users(self.USERS_FILE)
            sg.popup("Registered", background_color="green", text_color="darkblue")

        return new_user        

if __name__ == "__main__":
    users = Users()
    values  = {"-USERNAME-":"tony", "-PASSWORD-":"1234"}
    print(users.login(values))
    