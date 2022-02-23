from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import serial
import struct
from random import randint

from pacemakers import Pacemakers


class Egram:

    def __init__(self, canvas, mode):
        # self.t = []
        self.atr = []
        self.vent = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = canvas
        self.canvas_agg = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_agg.draw()
        self.canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.mode = mode

    def update_data(self):
        with serial.Serial(Pacemakers.PORT, Pacemakers.RATE, timeout=1) as ser:
            ser.write(struct.pack("<BB35B", *Pacemakers.COM_GET_H, *([0]*35)))
            if self.mode == "Atrial":
                self.atr.append(struct.unpack(Pacemakers.COM_FORMAT,ser.read(51))[-2])
            elif self.mode == "Ventricle":
                self.vent.append(struct.unpack(Pacemakers.COM_FORMAT,ser.read(51))[-1])
            elif self.mode == "Both":
                data = struct.unpack(Pacemakers.COM_FORMAT,ser.read(51))
                self.atr.append(data[-2])
                self.vent.append(data[-1])
        self.clip()

    # def update_data(self):
    #     self.atr.append(randint(0,10))
    #     self.vent.append(randint(0,10))
    #     self.clip()

    def clip(self):
        self.atr = self.atr[-99:] if len(self.atr) > 100 else self.atr
        self.vent = self.vent[-99:] if len(self.vent) > 100 else self.vent

    def draw_graph(self):
        self.update_data()
        # print(self.atr)
        atr_data = self.atr if len(self.atr) == 100 else (self.atr + [0]*(100-len(self.atr)))
        vent_data = self.vent if len(self.vent) == 100 else (self.vent + [0]*(100-len(self.vent)))
        # print(atr_data)
        # atr_data = self.atr if len(self.atr) == 100 else self.atr.extend([0]*(99-len(self.atr)))
        self.ax.clear()
        self.ax.grid()
        if self.mode == "Atrial":
            self.ax.plot(range(100), atr_data, color="purple", label="Atrial signal")
        elif self.mode == "Ventricle":
            self.ax.plot(range(100), vent_data, color="blue", label="Ventricle signal")
        elif self.mode == "Both":
            self.ax.plot(range(100), atr_data, color="purple", label="Atrial signal")
            self.ax.plot(range(100), vent_data, color="blue", label="Ventricle signal")
        self.ax.legend(loc="upper left")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("ATR/VENT signal")
        self.ax.set_title("Egram")
        self.canvas_agg.draw()

if __name__ == "__main__":
    sg.theme("DarkBlue1")
    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))
    layout = [  
        [sg.Canvas(size=(640, 480), key='-CANVAS-')],
        [sg.Button('Exit', size=(30, 1), pad=((280, 0), 3), font='Helvetica 14')]
    ]
    window = sg.Window('Egram', layout, finalize=True)
    canvas = window["-CANVAS-"].TKCanvas
    egram = Egram(canvas, "Both")
    # for i in range(10):
    #     egram.draw_graph()
    
    while True:
        event, values = window.read(timeout=0)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        egram.draw_graph()    
    window.close()