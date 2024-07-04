#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:21:24 2023

@author: ashishm
"""

from __future__ import print_function, division
import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
import csv
import matplotlib.pyplot as plt
import math
import datetime
from PyAstronomy import pyasl
import subprocess, shlex
import time
import signal


# Default values for sky_temp and ground_temp
sky_temp = 5
ground_temp = 300
recording = False
# Variables to store selected points for receiver temperature correction
point1 = None
point2 = None

# Lists to store checkboxes and their states
states = []
buttons = []
currentFolder = None

# Dictionary to store the plotted data
plot_data_dict = {}

# Global variables to store the observatory latitude, longitude, and altitude
observatory_latitude = None
observatory_longitude = None
observatory_altitude = None

# Global variable to store the source coordinates (RA and DEC)
source_coordinates = None

# Global variable to store the source date and time
source_date_time = None
override_date_time = False

# Global variable to store the messages
messages = []

# Function to update the status bar with the current message
def update_status_bar():
    current_message = messages[-1] if messages else ""
    status_var.set(current_message)

# Function to add a message to the messages list and update the status bar
def add_message(message):
    messages.append(message)
    update_status_bar()

# Function to update the messages display in the "Messages" tab
def update_messages_display():
    messages.config(state=tk.NORMAL)
    messages.delete(1.0, tk.END)
    for message in messages:
        messages.insert(tk.END, message + '\n')
    messages.config(state=tk.DISABLED)

def startTimer(timeleft):
    t = timeleft
    if not recording:
        start_freq_entry.config(state='normal')
        stop_freq_entry.config(state='normal')
        bin_sz_entry.config(state='normal')
        gain_entry.config(state='normal')
        int_time_entry.config(state='normal')
        int_time_entry.delete(0, tk.END)
        int_time_entry.insert(0, str(t))
        time_left_label.config(text=f"Time left:".ljust(16,' '))
        record_data_button.config(text="Record Data".ljust(14,' '))
        root_window.update()
    elif recording:
        time_left_label.config(text=f"Time left: {timeleft} s".ljust(16,' '))
        start_freq_entry.config(state='disabled')
        stop_freq_entry.config(state='disabled')
        bin_sz_entry.config(state='disabled')
        gain_entry.config(state='disabled')
        int_time_entry.delete(0, tk.END)
        int_time_entry.insert(0, f"Recording {t}s of data")
        int_time_entry.config(state='disabled')
        root_window.update()
        while timeleft > 0:
            if not recording:
                break
            time.sleep(1)
            timeleft -= 1
            time_left_label.config(text=f"Time left: {timeleft} s".ljust(16,' '))
            root_window.update()
        start_freq_entry.config(state='normal')
        stop_freq_entry.config(state='normal')
        bin_sz_entry.config(state='normal')
        gain_entry.config(state='normal')
        int_time_entry.config(state='normal')
        int_time_entry.delete(0, tk.END)
        int_time_entry.insert(0, str(t))
        time_left_label.config(text=f"Time left:".ljust(16,' '))
        record_data_button.config(text="Record Data".ljust(14,' '))
        root_window.update()

def record_and_plot_data():
    global p
    global recording

    if recording:
        p.terminate()
        p.wait()
        # print(p.pid)
        # os.kill(p.pid, signal.SIGKILL)
        recording = False
        # record_data_button.config(text="Record Data")
        startTimer(60)
        root_window.update()

    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            os.chdir(file_dir)

            # enter start frequency
            start_freq = start_freq_entry.get()
            stop_freq = stop_freq_entry.get()
            bin_sz = bin_sz_entry.get()
            gain = gain_entry.get()
            int_time = int_time_entry.get()

            command = 'rtl_power -f '+start_freq+':'+stop_freq+':'+bin_sz+' -g '+gain+' -i '+int_time+' -1 '+file_name
            args = shlex.split(command)
            
            p = subprocess.Popen(args, start_new_session=True)
            record_data_button.config(text="Stop Recording")
            recording = True
            startTimer(int(int_time))
            time.sleep(2)

            #with open(file_name, mode ='r')as file:
            csvFile = pd.read_csv(file_path, header=None)
            
                
            x_start = csvFile.iloc[0, 2] / 1e6
            x_stop = csvFile.iloc[0, 3] / 1e6
            x_data = np.linspace(x_start, x_stop, num=len(csvFile.columns) - 6)
            y_data = csvFile.iloc[0, 6:].values.astype(float)
            
            ax.plot(x_data,y_data)
            ax.set_xlabel('Frequency (MHz)')
            ax.set_ylabel('Power (dBm)')
            ax.set_title('Recorded Data')
            canvas.draw()
            message = f"Data recorded and plotted from {file_name}"
            add_message(message)

def clear_plot():
    # Clear the plot in the first tab
    ax.clear()
    canvas.draw()

    # Update the file name label
    file_name_label.config(text="")

    # Clear the messages and update the messages display
    global messages
    messages = []
    update_messages_display()
        
def open_file_and_record():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path, header=None)
        message = f"Data recorded and plotted from {file_path}"
        add_message(message)

def open_file_and_plot(file_type, ax, filegiven=None, multiple=False):
    if filegiven is None:
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    else:
        file_path = filegiven
    if file_path:
        df = pd.read_csv(file_path, header=None)
        x_start = df.iloc[0, 2] / 1e6
        x_stop = df.iloc[0, 3] / 1e6
        x_data = np.linspace(x_start, x_stop, num=len(df.columns) - 6)
        y_data = df.iloc[0, 6:].values.astype(float)
        y_data = (10 ** (y_data / 10)) / 1000
        file_name = file_path.split("/")[-1]

        # Store source date and time in the global variable
        global source_date_time
        source_date_time_str = df.iloc[0, 0] + " " + df.iloc[0, 1]
        source_date_time = datetime.datetime.strptime(source_date_time_str, '%Y-%m-%d %H:%M:%S')

        if multiple:
            plot_multiple_data(x_data, y_data, ax, file_name)
            message = f"Data plotted from {file_path}"
            add_message(message)
        else:    
            plot_data(file_type, x_data, y_data, ax, file_name, multiple)
            message = f"{file_type} data plotted from {file_path}"
            add_message(message)


def open_multiple_files_and_plot():
    global states
    global buttons
    multiple_ax_temperature.cla()
    multiple_canvas_temperature.draw()
    # print([val.get() for val in states])
    for i in range(len(buttons)):
        if states[i].get() == 1:
            filename = buttons[i].cget("text")
            filepath = currentFolder+"/"+filename
            try:
                open_file_and_plot(None, multiple_ax_temperature,filepath,multiple=True)
            except:
                continue

def open_folder():
    folderpath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    folderpath = os.path.dirname(folderpath)
    global buttons
    global states
    global currentFolder
    if folderpath:
        currentFolder = folderpath
        for button in buttons:
            button.pack_forget()
        buttons = []
        for file in os.listdir(folderpath):
            if file.endswith('.csv'):
                temp_var = tk.IntVar()
                temp = tk.Checkbutton(plot_multiple_tab, text=file, variable=temp_var)
                temp.pack(side=tk.LEFT)
                buttons.append(temp)
                states.append(temp_var)
            else:
                continue
    root_window.update()

def plot_multiple_data(x_data, y_data, ax, file_name):
    ax.plot(x_data, y_data, label=file_name)
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Power (Watts)')
    ax.set_title('CSV Data Plot')
    ax.legend()
    multiple_canvas_temperature.draw()

def plot_data(file_type, x_data, y_data, ax, file_name, multiple):
    if file_type in plot_data_dict:
        plot_data_dict[file_type]['line'].remove()
    plot_data_dict[file_type] = {'x_data': x_data, 'y_data': y_data, 'line': None}
    plot_data_dict[file_type]['line'], = ax.plot(x_data, y_data, label=file_name + " (" + file_type + ")")
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Power (Watts)')
    ax.set_title('CSV Data Plot')
    ax.legend()
    if multiple:
        multiple_canvas_temperature.draw()
    else:
        canvas_temperature.draw()

def set_sky_temperature():
    global sky_temp
    sky_temp = float(sky_temp_entry.get())
    message = f"Sky temperature set to: {sky_temp}"
    add_message(message)


def set_ground_temperature():
    global ground_temp
    ground_temp = float(ground_temp_entry.get())
    message = f"Ground temperature set to: {ground_temp}"
    add_message(message)

def calculate_receiver_temp():
    global point1, point2
    point1 = None
    point2 = None
    if 'Ground' in plot_data_dict and 'Sky' in plot_data_dict:
        ground_data = plot_data_dict['Ground']['y_data']
        sky_data = plot_data_dict['Sky']['y_data']
        p1 = ground_data / sky_data
        Tr_original = (sky_temp * p1 - ground_temp) / (1 - p1)
        ax_temperature2.clear()
        ax_temperature2.plot(plot_data_dict['Ground']['x_data'], Tr_original, label='Original Receiver Temperature (Tr)')
        ax_temperature2.set_xlabel('Frequency (MHz)')
        ax_temperature2.set_ylabel('Temperature (K)')
        ax_temperature2.set_title('Receiver and Source Temperature')
        ax_temperature2.legend()
        canvas_temperature2.draw()
        plot_data_dict['Tr_original'] = {'x_data': plot_data_dict['Ground']['x_data'], 'y_data': Tr_original, 'line': None}
        Tr_corrected = Tr_original.copy()
        if point1 is not None and point2 is not None:
            m = (point2[1] - point1[1]) / (point2[0] - point1[0])
            b = point1[1] - m * point1[0]
            x_min = min(point1[0], point2[0])
            x_max = max(point1[0], point2[0])
            indices_to_replace = np.logical_and(
                plot_data_dict['Ground']['x_data'] >= x_min,
                plot_data_dict['Ground']['x_data'] <= x_max
            )
            Tr_corrected[indices_to_replace] = m * plot_data_dict['Ground']['x_data'][indices_to_replace] + b
        plot_data_dict['Tr'] = {'x_data': plot_data_dict['Ground']['x_data'], 'y_data': Tr_corrected, 'line': None}
        ax_temperature2.plot(plot_data_dict['Ground']['x_data'], Tr_corrected, label='Corrected Receiver Temperature (Tr)')
        canvas_temperature2.draw()
        message = "Receiver temperature calculated."
        add_message(message)
    else:
        message = "Both Ground and Sky data must be plotted first."
        add_message(message)

def calculate_ts():
    if 'Ground' in plot_data_dict and 'Source' in plot_data_dict:
        ground_data = plot_data_dict['Ground']['y_data']
        source_data = plot_data_dict['Source']['y_data']
        p2 = ground_data / source_data
        Tr = plot_data_dict['Tr']['y_data']
        Ts = ((ground_temp + Tr) / p2) - Tr - sky_temp
        plot_data_dict['Ts'] = {'x_data': plot_data_dict['Ground']['x_data'], 'y_data': Ts, 'line': None}
        ax_temperature2.plot(plot_data_dict['Ground']['x_data'], Ts, label='Source Temperature (Ts)')
        canvas_temperature2.draw()
        message = "Source temperature calculated."
        add_message(message)
    else:
        message = "Both Ground and Source data must be plotted first."
        add_message(message)

def on_tr_click(event):
    global point1, point2
    if event.inaxes == ax_temperature2:
        x_val = event.xdata
        y_val = event.ydata
        if point1 is None:
            point1 = (x_val, y_val)
            ax_temperature2.plot(x_val, y_val, 'ro', markersize=10)
        elif point2 is None:
            point2 = (x_val, y_val)
            ax_temperature2.plot(x_val, y_val, 'ro', markersize=10)
            ax_temperature2.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r--')
            ground_data = plot_data_dict['Ground']['y_data']
            sky_data = plot_data_dict['Sky']['y_data']
            p1 = ground_data / sky_data
            Tr = (sky_temp * p1 - ground_temp) / (1 - p1)
            m = (point2[1] - point1[1]) / (point2[0] - point1[0])
            b = point1[1] - m * point1[0]
            x_min = min(point1[0], point2[0])
            x_max = max(point1[0], point2[0])
            indices_to_replace = np.logical_and(
                plot_data_dict['Ground']['x_data'] >= x_min,
                plot_data_dict['Ground']['x_data'] <= x_max
            )
            Tr[indices_to_replace] = m * plot_data_dict['Ground']['x_data'][indices_to_replace] + b
            plot_data_dict['Tr'] = {'x_data': plot_data_dict['Ground']['x_data'], 'y_data': Tr, 'line': None}
            ax_temperature2.plot(plot_data_dict['Ground']['x_data'], Tr, label='Receiver Temperature (Tr)')
            point1 = None
            point2 = None
            canvas_temperature2.draw()

def on_tr_leave(event):
    global point1, point2
    if event.inaxes == ax_temperature2:
        if point1 is not None:
            ax_temperature2.lines[-1].remove()
            ax_temperature2.plot(point1[0], point1[1], 'ro', markersize=10)
        if point2 is not None:
            ax_temperature2.lines[-1].remove()
            ax_temperature2.plot(point2[0], point2[1], 'ro', markersize=10)

def calculate_brightness_temperature():
    global brightness_temp
    if 'Ts' in plot_data_dict:
        Ts = plot_data_dict['Ts']['y_data']
        offset = (Ts[:10].mean() + Ts[-10:].mean()) / 2
        brightness_temp = Ts - offset
        plot_data_dict['Brightness Temperature'] = {'x_data': plot_data_dict['Ground']['x_data'], 'y_data': brightness_temp, 'line': None}
        ax_temperature2.plot(plot_data_dict['Ground']['x_data'], brightness_temp, label='Brightness Temperature (K)')
        ax_temperature2.legend()
        canvas_temperature2.draw()
        message = "Brightness temperature calculated."
        add_message(message)
    else:
        message = "Ts data must be calculated and plotted first."
        add_message(message)
        
def reset_tr():
    if 'Tr' in plot_data_dict:
        del plot_data_dict['Tr']
        calculate_receiver_temp()
        message = "Tr data reset."
        add_message(message)
    else:
        message = "Tr data is not available. Calculate Receiver Temperature first."
        add_message(message)

def save_data():
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if save_path:
        data_dict = {'Frequency (MHz)': plot_data_dict['Ground']['x_data'],
                     'Ground Data (Watts)': plot_data_dict['Ground']['y_data'],
                     'Sky Data (Watts)': plot_data_dict['Sky']['y_data'],
                     'Source Data (Watts)': plot_data_dict['Source']['y_data'],
                     'Original Receiver Temperature (Tr) (K)': plot_data_dict['Tr_original']['y_data'],
                     'Corrected Receiver Temperature (Tr) (K)': plot_data_dict['Tr']['y_data'],
                     'Source Temperature (Ts) (K)': plot_data_dict['Ts']['y_data'],
                     'Brightness Temperature (K)': brightness_temp}
        df = pd.DataFrame(data_dict)
        df.to_csv(save_path, index=False)
        message = f"Data saved to {save_path}"
        add_message(message)
        
def calculate_vlsr():
    # Get user inputs for observatory coordinates and source coordinates (RA and DEC)
    longitude = float(longitude_entry.get())
    latitude = float(latitude_entry.get())
    altitude = float(altitude_entry.get())

    source_coords = source_coords_entry.get()
    obs_ra_2000, obs_dec_2000 = pyasl.coordsSexaToDeg(source_coords)

    # Get the date and time from the global variable or from user input
    global source_date_time, override_date_time
    if override_date_time:
        date_time_str = date_time_entry.get()
        source_date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Time of observation converted to Julian Date
    jd = pyasl.jdcnv(source_date_time)


    # Calculate barycentric correction
    corr, hjd = pyasl.helcorr(longitude, latitude, altitude, obs_ra_2000, obs_dec_2000, jd, debug=False)

    # Calculate LSR correction
    v_sun = 20.5  # peculiar velocity (km/s) of sun w.r.t. LSR
    sun_ra = math.radians(270.2)  # solar apex
    sun_dec = math.radians(28.7)

    obs_dec = math.radians(obs_dec_2000)
    obs_ra = math.radians(obs_ra_2000)

    a = math.cos(sun_dec) * math.cos(obs_dec)
    b = (math.cos(sun_ra) * math.cos(obs_ra)) + (math.sin(sun_ra) * math.sin(obs_ra))
    c = math.sin(sun_dec) * math.sin(obs_dec)
    v_rs = v_sun * ((a * b) + c)

    v_lsr = corr + v_rs
    return -v_lsr
    message = f"VLSR calculated using date and time: {source_date_time}"
    add_message(message)
    
def toggle_override_date_time():
    global override_date_time
    override_date_time = not override_date_time
    if override_date_time:
        date_time_entry.config(state=tk.NORMAL)
        message = "Date and time override enabled."
    else:
        date_time_entry.delete(0, tk.END)
        date_time_entry.config(state=tk.DISABLED)
        message = "Date and time override disabled."
    add_message(message)
        
def plot_velocity_conversion():
    # Get data from the "Brightness Temperature" plot_data_dict
    if 'Brightness Temperature' in plot_data_dict:
        f0 = 1420.4057511
        c = 299792.458
        f = plot_data_dict['Brightness Temperature']['x_data']
        Ts = plot_data_dict['Brightness Temperature']['y_data']
        v = c * (1 - (f / f0))

        # Plot velocity vs brightness temperature
        ax_velocity_correction.clear()
        ax_velocity_correction.plot(v, Ts, label='Velocity Conversion')
        ax_velocity_correction.set_xlabel('Velocity (km/s)')
        ax_velocity_correction.set_ylabel('Brightness Temperature (K)')
        ax_velocity_correction.set_title('Velocity Conversion vs Brightness Temperature')
        ax_velocity_correction.legend()
        canvas_velocity_correction.draw()

def plot_velocity_correction():
    if observatory_latitude is None or observatory_longitude is None or observatory_altitude is None:
        message = "Please enter the observatory latitude, longitude, and altitude."
        add_message(message)
        return

    # Calculate vlsr
    vlsr = calculate_vlsr()

    # Get data from the "Brightness Temperature" plot_data_dict
    if 'Brightness Temperature' in plot_data_dict:
        f0 = 1420.4057511
        c = 299792.458
        f = plot_data_dict['Brightness Temperature']['x_data']
        Ts = plot_data_dict['Brightness Temperature']['y_data']
        v = c * (1 - (f / f0))

        # Subtract vlsr from velocity data
        v_corrected = v - vlsr

        # Plot velocity conversion (Overlay on the same plot window)
        plot_velocity_conversion()

        # Plot corrected data
        ax_velocity_correction.plot(v_corrected, Ts, label='Velocity Correction')
        ax_velocity_correction.set_xlabel('Velocity Corrected (km/s)')
        ax_velocity_correction.set_ylabel('Brightness Temperature (K)')
        ax_velocity_correction.set_title('Velocity Correction vs Brightness Temperature')
        ax_velocity_correction.legend()
        canvas_velocity_correction.draw()

def set_observatory_parameters():
    global observatory_latitude, observatory_longitude, observatory_altitude
    try:
        observatory_latitude = float(latitude_entry.get())
        observatory_longitude = float(longitude_entry.get())
        observatory_altitude = float(altitude_entry.get())
        message = "Observatory parameters set."
        add_message(message)
    except ValueError:
        message = "Invalid input. Please enter valid numbers for latitude, longitude, and altitude."
        add_message(message)

def save_plots_to_csv():
    if 'Brightness Temperature' in plot_data_dict:
        f0 = 1420.4057511
        c = 299792.458
        f = plot_data_dict['Brightness Temperature']['x_data']
        Ts = plot_data_dict['Brightness Temperature']['y_data']
        v = c * (1 - (f / f0))

        # Subtract vlsr from velocity data
        vlsr = calculate_vlsr()
        v_corrected = v - vlsr

        # Combine data into a dictionary
        data_dict = {
            'Velocity': v,
            'Brightness Temperature': Ts,
            'Velocity Corrected': v_corrected
        }

        # Convert dictionary to a DataFrame
        df = pd.DataFrame(data_dict)

        # Save DataFrame to a CSV file
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            df.to_csv(save_path, index=False)
            message = "Plots saved to CSV file: {save_path}"
            add_message(message)
        
def set_source_coordinates():
    global source_coordinates
    source_coords = source_coords_entry.get()
    ra, dec = pyasl.coordsSexaToDeg(source_coords)
    source_coordinates = (ra, dec)
    message = "Source coordinates set to: {source_coords}"
    add_message(message)


root_window = tk.Tk()
root_window.title("CSV Data Plotter")
# root_window.geometry("800x600")
# root_window.maxsize(800,600)

# Create a tabbed interface
tab_control = ttk.Notebook(root_window)
tab_control.pack(fill=tk.BOTH, expand=True)



# Create a status bar to display the current message
status_var = tk.StringVar()
status_bar = tk.Label(root_window, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# First tab: "Record Data" window
record_data_tab = ttk.Frame(tab_control)
tab_control.add(record_data_tab, text="Record Data")

# User input fields
start_freq_label = tk.Label(record_data_tab, text="Start Frequency:")
# start_freq_label.pack(anchor="w")
start_freq_label.grid(row=0,pady=(25,0))
start_freq_entry = tk.Entry(record_data_tab, width=20)
start_freq_entry.insert(0, '1419.405751M')
# start_freq_entry.pack(anchor="w")
start_freq_entry.grid(row=0,column=1,pady=(25,0))


stop_freq_label = tk.Label(record_data_tab, text="Stop Frequency:")
# stop_freq_label.pack(anchor="w")
stop_freq_label.grid(row=1)
stop_freq_entry = tk.Entry(record_data_tab, width=20)
stop_freq_entry.insert(0, '1421.405751M')
# stop_freq_entry.pack(anchor="w")
stop_freq_entry.grid(row=1,column=1)

bin_sz_label = tk.Label(record_data_tab, text="Bin Size:")
# bin_sz_label.pack(anchor="w")
bin_sz_label.grid(row=2)
bin_sz_entry = tk.Entry(record_data_tab, width=20)
bin_sz_entry.insert(0, '4k')
# bin_sz_entry.pack(anchor="w")
bin_sz_entry.grid(row=2,column=1)

gain_label = tk.Label(record_data_tab, text="Gain:")
# gain_label.pack(anchor="w")
gain_label.grid(row=3)
gain_entry = tk.Entry(record_data_tab, width=20)
gain_entry.insert(0, '50')
# gain_entry.pack(anchor="w")
gain_entry.grid(row=3,column=1)

int_time_label = tk.Label(record_data_tab, text="Integration Time:")
# int_time_label.pack(anchor="w")
int_time_label.grid(row=4)
int_time_entry = tk.Entry(record_data_tab, width=20)
int_time_entry.insert(0, '60')
# int_time_entry.pack(anchor="w")
int_time_entry.grid(row=4,column=1)

record_data_button = tk.Button(record_data_tab, text="Record Data".ljust(14,' '), command=record_and_plot_data)
# record_data_button.pack(side=tk.LEFT, padx=5, pady=5)
record_data_button.grid(row=0,column=3,sticky="w",rowspan=3)

# Add a "Clear Plot" button
clear_plot_button = tk.Button(record_data_tab, text="Clear Plot", command=clear_plot)
# clear_plot_button.pack(side=tk.LEFT, padx=5, pady=5)
clear_plot_button.grid(row=3,column=3,sticky="w",rowspan=2)

# Add a time left text
time_left_label = tk.Label(record_data_tab, text="Time left:".ljust(16,' '))
# time_left_label.pack(anchor="w")
time_left_label.grid(row=0,column=4,pady=30,padx=20,rowspan=5,sticky="w")
time_left_label.config(font=("Courier", 32))

# Create a container for the plot and toolbar
plot_frame = tk.Frame(record_data_tab)
# plot_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
plot_frame.grid(row=5,column=0,padx=10,pady=10,columnspan=5,sticky='nesw')

# Create a matplotlib figure
fig = Figure(figsize=(8, 3), dpi=100)
ax = fig.add_subplot(111)

# Create a canvas for the figure
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.get_tk_widget().grid(row=5,column=0,padx=20,pady=20,columnspan=5,sticky='nesw')

# Create a label to display the file name
file_name_label = tk.Label(record_data_tab, text="")
# file_name_label.pack(side=tk.LEFT, padx=5, pady=5)

# Second tab: "Plot Data" window
plot_data_tab = ttk.Frame(tab_control)
tab_control.add(plot_data_tab, text="Plot Data")

# Create a container for the plot and toolbar
plot_frame = tk.Frame(plot_data_tab)
plot_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Matplotlib figure and axis for the plot
fig_temperature = Figure(figsize=(2, 2), dpi=100)
ax_temperature = fig_temperature.add_subplot(111)

# Create a container for the plot
canvas_temperature = FigureCanvasTkAgg(fig_temperature, master=plot_frame)
canvas_temperature.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add NavigationToolbar for zooming and panning
toolbar_temperature = NavigationToolbar2Tk(canvas_temperature, plot_frame)
toolbar_temperature.update()
toolbar_temperature.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

# Create buttons for selecting plot type
plot_ground_button = tk.Button(plot_data_tab, text="Plot Ground Data", command=lambda: open_file_and_plot('Ground', ax_temperature))
plot_ground_button.pack(side=tk.LEFT, padx=5, pady=5)

plot_sky_button = tk.Button(plot_data_tab, text="Plot Sky Data", command=lambda: open_file_and_plot('Sky', ax_temperature))
plot_sky_button.pack(side=tk.LEFT, padx=5, pady=5)

plot_source_button = tk.Button(plot_data_tab, text="Plot Source Data", command=lambda: open_file_and_plot('Source', ax_temperature))
plot_source_button.pack(side=tk.LEFT, padx=5, pady=5)

# Second (a) tab: "Plot Multiple" window
plot_multiple_tab = ttk.Frame(tab_control)
tab_control.add(plot_multiple_tab, text="Plot Multiple")

# Create a container for the plot and toolbar
plot_multiple_frame = tk.Frame(plot_multiple_tab)
plot_multiple_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Matplotlib figure and axis for the plot
multiple_fig_temperature = Figure(figsize=(2, 2), dpi=100)
multiple_ax_temperature = multiple_fig_temperature.add_subplot(111)

# Create a container for the plot
multiple_canvas_temperature = FigureCanvasTkAgg(multiple_fig_temperature, master=plot_multiple_frame)
multiple_canvas_temperature.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add NavigationToolbar for zooming and panning
multiple_toolbar_temperature = NavigationToolbar2Tk(multiple_canvas_temperature, plot_multiple_frame)
multiple_toolbar_temperature.update()
multiple_toolbar_temperature.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

plot_multiple_source_button = tk.Button(plot_multiple_tab, text="Open folder", command=lambda: open_folder())
plot_multiple_source_button.pack(side=tk.LEFT, padx=5, pady=5)

plot_multiple_button = tk.Button(plot_multiple_tab, text="Plot", command=lambda: open_multiple_files_and_plot())
plot_multiple_button.pack(side=tk.LEFT, padx=5, pady=5)

# Third tab: "Temperature Calibration" window
temp_calibration_tab = ttk.Frame(tab_control)
tab_control.add(temp_calibration_tab, text="Temperature Calibration")

# Create a container for the plot and toolbar in the third tab
plot_frame2 = tk.Frame(temp_calibration_tab)
plot_frame2.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Matplotlib figure and axis for the second plot
fig_temperature2 = Figure(figsize=(2, 2), dpi=100)
ax_temperature2 = fig_temperature2.add_subplot(111)

# Create a container for the second plot
canvas_temperature2 = FigureCanvasTkAgg(fig_temperature2, master=plot_frame2)
canvas_temperature2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add NavigationToolbar for zooming and panning in the second plot
toolbar_temperature2 = NavigationToolbar2Tk(canvas_temperature2, plot_frame2)
toolbar_temperature2.update()
toolbar_temperature2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

# Bind the click and leave events for the second plot
canvas_temperature2.mpl_connect('button_press_event', on_tr_click)
canvas_temperature2.mpl_connect('axes_leave_event', on_tr_leave)

# Create buttons and labels for setting sky temperature and ground temperature
sky_temp_label = tk.Label(temp_calibration_tab, text="Sky Temperature (K):")
sky_temp_label.pack(padx=5, pady=5, anchor="w")

sky_temp_entry = tk.Entry(temp_calibration_tab)
sky_temp_entry.pack(padx=5, pady=5, anchor="w")

# Create the "Set Sky Temperature" button below the sky temperature entry
sky_temp_button = tk.Button(temp_calibration_tab, text="Set Sky Temperature", command=set_sky_temperature)
sky_temp_button.pack(padx=5, pady=5, anchor="w")

ground_temp_label = tk.Label(temp_calibration_tab, text="Ground Temperature (K):")
ground_temp_label.pack(padx=5, pady=5, anchor="w")

ground_temp_entry = tk.Entry(temp_calibration_tab)
ground_temp_entry.pack(padx=5, pady=5, anchor="w")

ground_temp_button = tk.Button(temp_calibration_tab, text="Set Ground Temperature", command=set_ground_temperature)
ground_temp_button.pack(padx=5, pady=5, anchor="w")

# Create buttons for receiver temperature calculation and source temperature calculation
calc_tr_button = tk.Button(temp_calibration_tab, text="Calculate Receiver Temperature", command=calculate_receiver_temp)
calc_tr_button.pack(padx=5, pady=5, anchor="w")

calc_ts_button = tk.Button(temp_calibration_tab, text="Calculate Source Temperature", command=calculate_ts)
calc_ts_button.pack(padx=5, pady=5, anchor="w")

# Create buttons for Tr, Ts and brightness temperature calculation
calc_brightness_temp_button = tk.Button(temp_calibration_tab, text="Calculate Brightness Temperature", command=calculate_brightness_temperature)
calc_brightness_temp_button.pack(padx=5, pady=5, anchor="w")

reset_tr_button = tk.Button(temp_calibration_tab, text="Reset Tr", command=reset_tr)
reset_tr_button.pack(padx=5, pady=5, anchor="w")

save_data_button = tk.Button(temp_calibration_tab, text="Save Data", command=save_data)
save_data_button.pack(padx=5, pady=5, anchor="w")

# Fourth tab: "Velocity Correction" window
velocity_correction_tab = ttk.Frame(tab_control)
tab_control.add(velocity_correction_tab, text="Velocity Correction")

# Create a container for the plot and toolbar in the fourth tab
plot_frame_velocity = tk.Frame(velocity_correction_tab)
plot_frame_velocity.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

canvas_velocity_correction = FigureCanvasTkAgg(plt.Figure(figsize=(2, 2), dpi=100), master=plot_frame_velocity)
canvas_velocity_correction.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
ax_velocity_correction = canvas_velocity_correction.figure.add_subplot(111)

# Create the "Velocity Conversion" and "Velocity Correction" buttons
conversion_button = tk.Button(velocity_correction_tab, text="Velocity Conversion", command=plot_velocity_conversion)
conversion_button.pack(side=tk.LEFT, padx=5, pady=5)

correction_button = tk.Button(velocity_correction_tab, text="Velocity Correction", command=plot_velocity_correction)
correction_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create input fields for observatory and source coordinates
input_frame = tk.Frame(velocity_correction_tab)
input_frame.pack(padx=10, pady=5)

# Create input fields for observatory parameters
latitude_label = tk.Label(velocity_correction_tab, text="Latitude:")
latitude_label.pack(padx=5, pady=5, anchor="w")
latitude_entry = tk.Entry(velocity_correction_tab, width=20)
latitude_entry.pack(padx=5, pady=5, anchor="w")

longitude_label = tk.Label(velocity_correction_tab, text="Longitude:")
longitude_label.pack(padx=5, pady=5, anchor="w")
longitude_entry = tk.Entry(velocity_correction_tab, width=20)
longitude_entry.pack(padx=5, pady=5, anchor="w")

altitude_label = tk.Label(velocity_correction_tab, text="Altitude:")
altitude_label.pack(padx=5, pady=5, anchor="w")
altitude_entry = tk.Entry(velocity_correction_tab, width=20)
altitude_entry.pack(padx=5, pady=5, anchor="w")

# Create the "Set Observatory Parameters" button
set_parameters_button = tk.Button(velocity_correction_tab, text="Set Observatory Parameters", command=set_observatory_parameters)
set_parameters_button.pack(padx=5, pady=5, anchor="w")

source_coords_label = tk.Label(input_frame, text="Source Coords (RA DEC):")
source_coords_label.grid(row=1, column=0, padx=5, pady=5)
source_coords_entry = tk.Entry(input_frame, width=20)
source_coords_entry.grid(row=1, column=1, columnspan=5, padx=5, pady=5)

# Create the "Set Source Coordinates" button
set_source_coords_button = tk.Button(input_frame, text="Set Source Coordinates", command=set_source_coordinates)
set_source_coords_button.grid(row=1, column=6, padx=5, pady=5)

# Create a frame for the date and time input
date_time_frame = tk.Frame(velocity_correction_tab)
date_time_frame.pack(padx=10, pady=5, fill=tk.X)

# Create a checkbox to toggle override date and time
override_date_time_var = tk.IntVar()
override_date_time_checkbox = tk.Checkbutton(date_time_frame, text="Override Date and Time", variable=override_date_time_var, command=toggle_override_date_time)
override_date_time_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

# Create an entry for the user to enter date and time
date_time_entry = tk.Entry(date_time_frame, width=20, state=tk.DISABLED)
date_time_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Create the "Save" button
save_button = tk.Button(velocity_correction_tab, text="Save Plots to CSV", command=save_plots_to_csv)
save_button.pack(padx=5, pady=5, anchor="w")

root_window.mainloop()
