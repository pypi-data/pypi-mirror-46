# Pip Modules
import tkinter as tk
from tkinter import ttk

from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import Frame
from tkinter import StringVar
from tkinter import OptionMenu

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random

import serial
from serial import SerialException
import serial.tools.list_ports

# Project Modules
from transvenous_pacing_gui.signals import Signals
from transvenous_pacing_gui.server import Server

from queue import Queue

class StudentGUI(tk.Frame):
    # Settings
    header_1_style = "TkDefaultFont 42 bold"
    header_2_style = "TkDefaultFont 18 bold"
    default_style  = "TkDefaultFont 14"

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.socket_queue = Queue()

        self.server = Server(port=25565)
        self.server.start(self.socket_queue)

        self.ecg_signals = Signals()

        self.hr = IntVar(self, value=80)
        self.threshold = IntVar(self, value=20)
        self.hr_paced = IntVar(self, value=80)

        self.position = IntVar(self, value=0)
        self.serial_position = IntVar(self, value='0')
        self.hr1 = StringVar(self, value='0')

        self.override_position = BooleanVar(self, value=False)

        self.pathway_1 = IntVar(self, value=0)
        self.pathway_2 = IntVar(self, value=0)
        self.is_paced = BooleanVar(self, value=False)

        self.plot_point = 0

        # Take care of plotting
        fig = plt.Figure(figsize=(14, 4.5), dpi=100,facecolor='k',edgecolor='k')

        self.new_x = [0.0]
        self.new_y = [0.0]

        self.last_x = 0
        self.last_x_lim = 0

        self.position_to_show = 0

        self.variation = 0

        self.flat_span = False
        self.end_flat = 0
        self.flat_span_y = 0

        Options=['']
        Options.extend(serial.tools.list_ports.comports())

        # GUI Utilisation
        self.wait_for_update = BooleanVar(self, value=False)
        self.wait_for_position = BooleanVar(self, value=False)
        self.wait_for_pathway_1 = BooleanVar(self, value=False)
        self.wait_for_pathway_2 = BooleanVar(self, value=False)
        
        self.s = 'RIP'
        self.ser = None

        # Main Grid Frames
        frame_signals = Frame(self, bg='black')
        frame_signals.pack(side=tk.LEFT)

        frame_values = Frame(self, bg='black')
        frame_values.pack(side=tk.RIGHT, padx=10)

        # Rest of setup
        tk.Label(frame_values, text="HR", font=self.header_2_style, bg="black", fg="lime green").pack()
        tk.Label(frame_values, textvariable=self.hr1,font=self.header_1_style,bg="black", fg="lime green").pack()
        
        canvas = FigureCanvasTkAgg(fig, master=frame_signals)
        canvas.get_tk_widget().grid(row=1, column=1)

        self.variable = StringVar(self)
        self.variable.set(Options[0]) #Default option

        w=OptionMenu(frame_signals, self.variable, *Options)
        w.grid(row=2, column=1)

        self.variable.trace('w', self.change_dropdown)

        # ===== ECG Signal Setup
        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(self.last_x_lim, 4)
        self.ax.set_ylim(-3.0, 3.0)
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.xaxis.set_tick_params(width=1, top=True)
        self.ax.set_facecolor('black')

        self.line, = self.ax.plot(0, 0)
        self.ax.get_lines()[0].set_color("xkcd:lime")
        self.ani = animation.FuncAnimation(fig, self.animate, interval=24, blit=True)

        # Polling Initialisation
        self.after(10, self.read_socket)

    def animate(self, i):
        # Set the position index value based on which source is responsible for the signal
        if self.override_position.get():
            position_index = self.position.get()
        else:
            position_index = self.serial_position.get()

        # Set initial heart rate to use
        hr_to_use = self.hr.get()

        # Adjust position and heart rate based on alternative pathways and pacer setting
        if position_index == 4:
            position_index = position_index + self.pathway_1.get()
        elif position_index == 6:
            position_index = position_index + self.pathway_2.get()

            if not position_index == 16 and self.is_paced.get():
                position_index = 26
                hr_to_use = self.hr_paced.get()
        else:
            position_index = position_index

        # Print what position is being printed
        print(self.ecg_signals.signal_index[position_index])

        # Display heart rate value on GUI
        if position_index == 0:
            self.hr1.set(0)
        else:
            self.hr1.set(hr_to_use)

        [x, y] = self.ecg_signals.get_signal(self.ecg_signals.signal_index[position_index], hr_to_use, self.variation)

        if not self.flat_span:
            x_val = self.last_x + x[self.plot_point]

            if x_val > self.new_x[-1]:
                self.new_x.append(x_val)
                self.new_y.append(y[self.plot_point])

                self.line.set_data(self.new_x, self.new_y)  # update the data
            
            if self.plot_point== 29:
                self.variation = random.randint(0, 1)
                self.last_x = self.new_x[-1]

                self.end_flat = (x[-1] - x[-2]) + self.new_x[-1]
                self.flat_span_y = y[-1]
                self.flat_span = True
                
            if self.plot_point == 29:
                self.plot_point = 0
            else:
                self.plot_point = self.plot_point + 1
        else:
            self.new_x.append(self.new_x[-1] + 0.05)
            self.new_y.append(self.flat_span_y)

            self.line.set_data(self.new_x, self.new_y)  # update the data

            if self.new_x[-1] >= self.end_flat:
                self.flat_span = False
                self.last_x = self.new_x[-1]
        
        if self.new_x[-1] >= self.last_x_lim + 5:
            self.last_x_lim += 5
            self.ax.set_xlim(self.last_x_lim, self.last_x_lim + 5)

        return self.line,

    def change_dropdown(self, *args):
        if not self.variable.get() == '':
            try:
                choice = self.variable.get().split(' -')
                self.ser = serial.Serial(choice[0], 9600)
                print('Connection established.')
                self.after(10, self.read_serial)
            except SerialException as e:
                print('Error: {}'.format(e))

    def read_socket(self):
        if not self.socket_queue.empty():
            message = self.socket_queue.get()

            print(message)

            if self.wait_for_update.get():
                result = [x.strip() for x in message.decode('utf-8').split(',')]

                self.hr.set(result[0])
                self.threshold.set(result[1])
                self.hr_paced.set(result[2])
                
                self.wait_for_update.set(False)
            elif self.wait_for_position.get():
                self.position.set(int(message.decode('utf-8')))
                self.wait_for_position.set(False)
                self.override_position.set(True)
            elif self.wait_for_pathway_1.get():
                self.pathway_1.set(int(message.decode('utf-8')))
                print(self.pathway_1.get())
                self.wait_for_pathway_1.set(False)
            elif self.wait_for_pathway_2.get():
                self.pathway_2.set(int(message.decode('utf-8')))
                print(self.pathway_2.get())
                self.wait_for_pathway_2.set(False)
            else:
                if message == b'update':
                    self.wait_for_update.set(True)
                elif message == b'start-pos':
                    self.wait_for_position.set(True)
                elif message == b'stop-pos':
                    self.override_position.set(False)
                elif message == b'manual-pos':
                    self.wait_for_position.set(True)
                elif message == b'chpa1':
                    self.wait_for_pathway_1.set(True)
                elif message == b'chpa2':
                    self.wait_for_pathway_2.set(True)
                elif message == b'close':
                    self.destroy()
                elif message == b'start-pace':
                    self.is_paced.set(True)
                elif message == b'stop-pace':
                    self.is_paced.set(False)
                elif message == b'cal':
                    self.write_serial(b'C')
                elif message == b'ressig':
                    self.position_to_show = 0
            
        self.after(10, self.read_socket)

    def pause_plot(self):
        self.ani.event_source.stop()

    def start_plot(self):
        self.ani.event_source.start()

    def write_serial(self, message):
        if not self.ser == None:
            try:
                self.ser.write(message)
                print(message)
            except Exception as e:
                print('Error: {}'.format(e))

    def read_serial(self):
        if not self.ser == None:
            try:
                if self.ser.in_waiting:
                    self.s = self.ser.read()
                    self.serial_position.set(int(self.s))
                    print(int(self.s))
                
            except Exception as e:
                print('Error: {}'.format(e))

        self.after(10, self.read_serial)

    def stop_gui(self):
        # Clean-up
        try:
            self.server.stop()
            self.ser.close()
        except Exception as e:
            print(e)
