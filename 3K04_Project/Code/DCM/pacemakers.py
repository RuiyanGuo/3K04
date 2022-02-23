# Manipulate the hostory of configurations of pacemaker
from ctypes.wintypes import PSMALL_RECT
import numpy as np
import PySimpleGUI as sg
import serial
import struct

from datetime import datetime
from json import (load as jsonload, dump as jsondump)
from os import path

class Pacemakers:
    MODE = ("AOO", "AOOR", "VOO", "VOOR", "AAI",
            "AAIR", "VVI", "VVIR", "DOO", "DOOR" )

    DEFAULT_PARAM = {
        "PacingMode" : None,
        "LowerRateLimit" : None,
        "UpperRateLimit" : None,
        "MaximumSensorRate": None,
        "AVDelay": None,
        "AtrialAmplitude" : None,
        "VentricularAmplitude" : None,
        "AtrialPulseWidth" : None,
        "VentricularPulseWidth" : None,
        "AtrialSensitivity" : None,
        "VentricularSensitivity" : None,
        "VRP" : None,
        "ARP" : None,
        "ActivityThreshold" : None,
        "ReactionTime" : None,
        "ResponseFactor" : None,
        "RecoveryTime" : None
    }
    PARAM_KEYS_TO_ELE_KEYS = {
        'PacingMode': '-PM-', 
        'LowerRateLimit': '-LRL-',
        "UpperRateLimit" : "-URL-",
        "MaximumSensorRate": "-MSR-",
        "AVDelay": "-AVD-",
        "AtrialAmplitude" : "-AA-",
        "VentricularAmplitude" : "-VA-",
        "AtrialPulseWidth" : "-APW-",
        "VentricularPulseWidth" : "-VPW-",
        "AtrialSensitivity" : "-AS-",
        "VentricularSensitivity" : "-VS-",
        "ARP" : "-ARP-",
        "VRP" : "-VRP-",
        "ActivityThreshold" : "-ATH-",
        "ReactionTime" : "-RAT-",
        "ResponseFactor" : "-RF-",
        "RecoveryTime" : "-RCT-"
    }
    PARAM_KEYS_TO_ELE_KEYS_IN = {
        'PacingMode': '-PM_IN-', 
        'LowerRateLimit': '-LRL_IN-',
        "UpperRateLimit" : "-URL_IN-",
        "MaximumSensorRate": "-MSR_IN-",
        "AVDelay": "-AVD_IN-",
        "AtrialAmplitude" : "-AA_IN-",
        "VentricularAmplitude" : "-VA_IN-",
        "AtrialPulseWidth" : "-APW_IN-",
        "VentricularPulseWidth" : "-VPW_IN-",
        "AtrialSensitivity" : "-AS_IN-",
        "VentricularSensitivity" : "-VS_IN-",
        "ARP" : "-ARP_IN-",
        "VRP" : "-VRP_IN-",
        "ActivityThreshold" : "-ATH_IN-",
        "ReactionTime" : "-RAT_IN-",
        "ResponseFactor" : "-RF_IN-",
        "RecoveryTime" : "-RCT_IN-"
    }
    # ELEMENT_KEYS_TO_PACEMAKER_KEYS = {v:k for k, v in PACEMAKER_KEYS_TO_ELEMENT_KEYS.items()}
    MODE_TO_ELE_KEYS = {
        "AOO" : ("-PM-", "-LRL-", "-URL-", "-AA-", "-APW-"),
        "VOO" : ("-PM-", "-LRL-", "-URL-", "-VA-", "-VPW-"),
        "AAI" : ("-PM-", "-LRL-", "-URL-", "-AA-", "-APW-", "-AS-", "-ARP-"),
        "VVI" : ("-PM-", "-LRL-", "-URL-", "-VA-", "-VPW-", "-VS-", "-VRP-"),
        "DOO" : ("-PM-", "-LRL-", "-URL-", "-AVD-", "-AA-", "-APW-", "-VA-", "-VPW-"),
        "AOOR" : ("-PM-", "-LRL-", "-URL-", "-MSR-", "-AA-", "-APW-", "-ATH-", "-RAT-", "-RF-", "-RCT-"),
        "VOOR" : ("-PM-", "-LRL-", "-URL-", "-MSR-", "-VA-", "-VPW-", "-ATH-", "-RAT-", "-RF-", "-RCT-"),
        "AAIR" : ("-PM-", "-LRL-", "-URL-", "-MSR-", "-AA-", "-APW-", "-AS-", "-ARP-", "-ATH-", "-RAT-", "-RF-", "-RCT-"),
        "VVIR" : ("-PM-", "-LRL-", "-URL-", "-MSR-", "-VA-", "-VPW-", "-VS-", "-VRP-", "-ATH-", "-RAT-", "-RF-", "-RCT-"),
        "DOOR" : ("-PM-", "-LRL-", "-URL-", "-MSR-", "-AVD-", "-AA-", "-APW-", "-VA-", "-VPW-", "-ATH-", "-RAT-", "-RF-", "-RCT-")
    }

    MODE_TO_PARAM_KEYS = {
        "AOO" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "AtrialAmplitude", "AtrialPulseWidth"),
        "VOO" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "VentricularAmplitude", "VentricularPulseWidth"),
        "AAI" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "AtrialAmplitude", "AtrialPulseWidth", "AtrialSensitivity", "ARP"),
        "VVI" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "VentricularAmplitude", "VentricularPulseWidth", "VentricularSensitivity", "VRP"),
        "DOO" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "AVDelay", "AtrialAmplitude", "AtrialPulseWidth", "VentricularAmplitude", "VentricularPulseWidth"),
        "AOOR" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "MaximumSensorRate", "AtrialAmplitude", "AtrialPulseWidth", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime"),
        "VOOR" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "MaximumSensorRate", "VentricularAmplitude", "VentricularPulseWidth", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime"),
        "AAIR" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "MaximumSensorRate", "AtrialAmplitude", "AtrialPulseWidth", "AtrialSensitivity", "ARP", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime"),
        "VVIR" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "MaximumSensorRate", "VentricularAmplitude", "VentricularPulseWidth", "VentricularSensitivity", "VRP", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime"),
        "DOOR" : ("PacingMode", "LowerRateLimit", "UpperRateLimit", "MaximumSensorRate", "AVDelay", "AtrialAmplitude", "AtrialPulseWidth", "VentricularAmplitude", "VentricularPulseWidth", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime")
    }

    PACEMAKERS_FILE = path.join(path.dirname(__file__), r'pacemakers.json')

    # For communication
    PORT = "COM5" # modify according to host
    RATE = 115200
    COM_ORDER = ("PacingMode", "LowerRateLimit", "MaximumSensorRate", "ARP", "VRP", "AtrialAmplitude", "VentricularAmplitude", "AtrialPulseWidth", "VentricularPulseWidth",
                "AtrialSensitivity", "VentricularSensitivity", "ActivityThreshold", "ResponseFactor", "ReactionTime", "RecoveryTime", "AVDelay", "UpperRateLimit")
    COM_FORMAT = "<3B2H2f2B3f3BHB2d" # compatible with struct

    COM_PARAM_SIZE = 51

    COM_GET_H = (0x16, 0x22)
    COM_SET_H = (0x16, 0x55)


    _pacemakers_inst = None
    # pacemaker_active = DEFAULT_PACEMAKER.copy()
    def __new__(cls):
        if cls._pacemakers_inst is None:
            cls._pacemakers_inst = super(Pacemakers, cls).__new__(cls)
            cls._pacemakers_inst.load_pacemakers()
        return cls._pacemakers_inst

    def load_pacemakers(self, pacemakers_file=PACEMAKERS_FILE):
        # Get pacemaker history and set current pacemaker profile
        try:
            with open(pacemakers_file, 'r') as f:
                self.pacemaker_history = jsonload(f)
                self.pacemaker_current = self.pacemaker_history[-1]
        except Exception as e:
            # sg.popup_quick_message(f'exception {e}', 'No pacemakers file found... will create one for you', keep_on_top=True, background_color='red', text_color='darkblue')
            self.pacemaker_current = self.DEFAULT_PARAM
            self.pacemaker_history = [self.pacemaker_current]
            self.save_pacemakers(pacemakers_file)
    
    def save_pacemakers(self, pacemakers_file=PACEMAKERS_FILE):
        with open(pacemakers_file, 'w') as f:
            jsondump(self.pacemaker_history, f, indent=4)


    def get_param(self):
        # print(self.pacemaker_current)
        values = {
            self.PARAM_KEYS_TO_ELE_KEYS[key] : self.pacemaker_current[key]
            for key in self.PARAM_KEYS_TO_ELE_KEYS
        }
        # print(values)
        return values

    def set_param(self, values):
        param = {}
        # print(values.get("-PM_IN-") in self.MODE)
        if values.get("-PM_IN-") and values.get("-PM_IN-") in self.MODE:
            param["PacingMode"] = values["-PM_IN-"]
            # print(param["PacingMode"])
            for key in self.PARAM_KEYS_TO_ELE_KEYS_IN:
                # print(self.MODE_TO_PARAM_KEYS.get(param["PacingMode"]))
                if key in self.MODE_TO_PARAM_KEYS.get(param["PacingMode"]): # and key != "PacingMode":
                    value = values.get(self.PARAM_KEYS_TO_ELE_KEYS_IN[key])
                    if value and self.validate_keys(key, value):
                        param[key] = self.type_converter(key,value)
                    else:
                        sg.popup(f"Please input valid {key}", background_color="red")
                        return False
                else:
                    param[key] = None
            if int(param["UpperRateLimit"]) < int(param["LowerRateLimit"]):
                sg.popup("Please input valid upper limits", background_color="red")
                return False
            if "R" in param["PacingMode"] and int(param["UpperRateLimit"]) < int(param["MaximumSensorRate"]):
                sg.popup("Please input valid upper limits", background_color="red")
                return False
            self.pacemaker_current = param
            self.pacemaker_history.append(self.pacemaker_current)
            self.save_pacemakers()
            return True
        else:
            sg.popup("Pleasr input valid pacing mode", background_color="red")
            return False

    def validate_keys(self, key, value):
        if key == "PacingMode":
            return value in self.MODE
        elif key == "LowerRateLimit":
            if "." not in value:
                return int(value) in list(range(30,51,5)) + list(range(50, 91, 1)) + list(range(90, 176,5))
            return False
        elif key in ("UpperRateLimit", "MaximumSensorRate"):
            if "." not in value:
                return int(value) in list(range(50, 176, 5))
            return False
        elif key == "AVDelay":
            if "." not in value:    
                return int(value) in list(range(70, 310, 10))
            return False
        elif key in ("AtrialAmplitude", "VentricularAmplitude"):
            return round(float(value),1) in list(map(lambda x: round(x, 1), np.arange(0.1, 5.1, 0.1)))
        elif key in ("AtrialPulseWidth", "VentricularPulseWidth"):
            if "." not in value:
                return int(value) in list(range(1,31,1))
            return False
        elif key in ("AtrialSensitivity", "VentricularSensitivity"):
            return round(float(value),1) in list(map(lambda x: round(x, 1), np.arange(0.0, 5.1, 0.1)))
        elif key in ("ARP", "VRP"):
            if "." not in value:
                return int(value) in list(range(150,510,10))
            return False
        elif key == "ActivityThreshold":
            return round(float(value),1) in list(map(lambda x: round(x, 1), np.arange(0.0, 7.0, 0.1))) #TODO
        elif key == "ReactionTime":
            if "." not in value:
                return int(value) in list(range(10,60,10))
            return False
        elif key == "ResponseFactor":
            if "." not in value:
                return int(value) in list(range(1,17,1))
            return False
        elif key == "RecoveryTime":
            if "." not in value:
                return int(value) in list(range(2,17,1))
            return False

    def get_current(self):
        return self.pacemaker_current

    def get_history(self):
        return self.pacemaker_history

    def type_converter(self, key, value):
        if key == "PacingMode":
            return value
        elif key == "LowerRateLimit":
            return int(value)
        elif key in ("UpperRateLimit", "MaximumSensorRate"):
            return int(value)
        elif key == "AVDelay":
            return int(value)
        elif key in ("AtrialAmplitude", "VentricularAmplitude"):
            return round(float(value),1)
        elif key in ("AtrialPulseWidth", "VentricularPulseWidth"):
            return int(value)
        elif key in ("AtrialSensitivity", "VentricularSensitivity"):
            return round(float(value),1)
        elif key in ("ARP", "VRP"):
            return int(value)
        elif key == "ActivityThreshold":
            return round(float(value),1)
        elif key == "ReactionTime":
            return int(value)
        elif key == "ResponseFactor":
            return int(value)
        elif key == "RecoveryTime":
            return int(value)


    def get_param_com(self):    
        # padding = [0]*17
        # size = 51
        arr = []
        with serial.Serial(self.PORT, self.RATE, timeout=1) as ser:
            ser.write(struct.pack("<BB35B", *self.COM_GET_H, *([0]*35)))
            data = ser.read(self.COM_PARAM_SIZE)
            arr = struct.unpack(self.COM_FORMAT, data)
        param = {}
        # print(arr)
        param["PacingMode"] = self.MODE[arr[0]-1]
        for i in range(1, len(arr)-2):
            key = self.COM_ORDER[i]
            if key in self.MODE_TO_PARAM_KEYS.get(param["PacingMode"]):
                param[key] = self.type_converter(key, arr[i])
            else:
                param[key] = None
        
        values = {
            self.PARAM_KEYS_TO_ELE_KEYS[key] : param[key]
            for key in param
        }
        return values    
        
    def set_param_com(self):
        set_param = (0x16, 0x55)
        params = []
        inst = self.pacemaker_current
        for key in self.COM_ORDER:
            if key == "PacingMode":
                params.append(self.MODE.index(inst[key])+1)
            else:
                params.append(inst.get(key) if inst.get(key) else 0)
        print(params)
        with serial.Serial(self.PORT, self.RATE, timeout=1) as ser:
            ser.write(struct.pack("<BB3B2H2f2B3f3BHB", *set_param, *params))
            # ser.read(1)
        return params  

        
        
        
if __name__ == "__main__":
    pacemaker = Pacemakers()
    
    print(pacemaker.get_param_com())