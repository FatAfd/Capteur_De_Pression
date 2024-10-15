# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:30:38 2024

@author: Inesd
"""


# User interface for data analysis 

from tkinter import * # 'import tkinter' doesn't work
from tkinter import filedialog 
from customtkinter import *
import math
import csv
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from tkinter import ttk 
import numpy as np
import pandas as pd

# Create the window

window = Tk()
window.title("Data Analysis Interface")
window.geometry ( '800x500' ) # window size

# App Icon

app_icon = PhotoImage(file='Icon.png')
window.iconphoto(True,app_icon)
window.config(background='white')

def calculate_mean(file, column):
     total = 0
     number_of_lines = 0
     valeur=0

     with open(file, newline='') as csvfile:
         reader = csv.reader(csvfile)
         for line in reader:
             try:
                 valeur = float(line[column])
                 total += valeur
                 number_of_lines += 1
             except ValueError:
                 pass

     if number_of_lines > 0:
         mean = total / number_of_lines
         return mean
     else:
         return None   
     
def maximum(file, column):
     maximum_value = 0
     number_of_lines = 0

     with open(file, newline='') as csvfile:
         reader = csv.reader(csvfile)
         for line in reader:
             try :
                 if float(line[column])>=maximum_value :
                     maximum_value = float(line[column])
                 else : 
                     maximum_value = maximum_value
             except ValueError :
                 pass
         return maximum_value   

def minimum(file, column):
     minimum_value = maximum(file,column)
     number_of_lines = 0

     with open(file, newline='') as csvfile:
         reader = csv.reader(csvfile)
         for line in reader:
             try :
                 if float(line[column])<=minimum_value :
                     minimum_value = float(line[column])
                 else : 
                     minimum_value = minimum_value
             except ValueError :
                 pass
         return minimum_value 


def calculate_standard_deviation(file, column):
    total = 0
    number_of_lines = 0
    mean = calculate_mean(file, column)

    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile) # reader 
        for line in reader:
            try:
                valeur = float(line[column])
                total += (valeur - mean)**2
                number_of_lines += 1
            except ValueError:
                pass

    if number_of_lines > 0:
        standard_deviation = math.sqrt((1/number_of_lines)*total)
        return standard_deviation
    else:
        return None
    
def save_choosen_value():
    sensor=int(entry_field.get())
    plot(csv_file,sensor)
    return None

def save_a_csv(): 
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
    maxi=0
    mini=0
    data = {
        "Sensor": [],
        "Mean": [],
        "Standard deviation": [],
        "Maximum": [],
        "Minimum": []
    }
    
    if file_path:
            for i in range(len(tab_used_sensors)):
                mean_value = calculate_mean(csv_file, tab_used_sensors[i])
                standard_deviation = calculate_standard_deviation(csv_file, tab_used_sensors[i])
                maxi=maximum(csv_file, tab_used_sensors[i])
                mini=minimum(csv_file, tab_used_sensors[i])
                data["Sensor"].append(tab_used_sensors[i])
                data["Mean"].append(mean_value)
                data["Standard deviation"].append(standard_deviation)
                data["Maximum"].append(maxi)
                data["Minimum"].append(mini)
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, sep=";")
            print("Fichier CSV créé avec succès :", file_path)
        #except Exception as e:
            #print("Erreur lors de l'écriture du fichier CSV :", str(e))
        #else:
        #print("Opération annulée.")


def display_analysis():
    label.pack_forget()
    #label_1.pack_forget()
    label_2.pack_forget()
    label_3.pack_forget()
    #button_1.pack_forget()
    button_2.pack_forget()
    global text_4
    global label_4
    text_4 = Text(window)
    label_4 = CTkLabel(window, text = "Significant values for the used sensors :\n", font=("Keyboard",14))
    label_4.pack(padx=4,pady=20)
    #print("The mean for the used sensors")
    #global frame
    #frame=CTkFrame(window,width=400, height=400, corner_radius=10, border_color="black", fg_color="#FFC688" )
    #frame.pack()
    #tab_letters=""
    tab = ttk.Treeview(window, columns=(1, 2, 3, 4, 5), show="headings")
    tab.heading(1, text='Sensor')
    tab.heading(2, text='Mean')
    tab.heading(3, text='Standard deviation')
    tab.heading(4, text='Maximum')
    tab.heading(5, text='Minimum')
    tab.insert('', 'end', values=(' ', ' ', ' '))
    maxi=0
    mini=0
    for i in range(0,len(tab_used_sensors)):
        mean_value = calculate_mean(csv_file, tab_used_sensors[i])
        maxi=maximum(csv_file, tab_used_sensors[i])
        mini=minimum(csv_file, tab_used_sensors[i])
        standard_deviation = calculate_standard_deviation(csv_file, tab_used_sensors[i])
        tab.insert('', 'end', values=(tab_used_sensors[i], mean_value, standard_deviation, maxi, mini))
        #tab_letters += f"Sensor {tab_used_sensors[i]} - Mean : {mean_value} pF,"+" "
        #tab_letters += f"Standard deviation : {standard_deviation} pF\n"
        #print(f"For sensor number {i} : The mean is {calculate_mean(csv_file,tab_used_sensors[i])} pF.")
        #print(f"The standard deviation is {calculate_standard_deviation(csv_file,tab_used_sensors[i])} pF.")
    tab.column(1, anchor='center', width=80)
    tab.column(2, width=150)
    tab.column(3, width=150)
    tab.column(4, width=150)
    tab.column(5, width=150)
    tab.pack()
    #text_5 = Text(frame)
    #label_5 = CTkLabel(frame, text = tab_letters, font=("Keyboard",12), justify="left")
    #label_5.place(relx=0, anchor='w') # move the text to the left side of frame
    #label_5.pack(padx=4,pady=20)
    global button_7
    button_7 = CTkButton(window, text="Save the values in a .CSV file", fg_color="#E0984B",text_color="black", command=save_a_csv)
    button_7.pack(pady=10)
    global entry_field
    entry_field = Entry()
    entry_field.pack(padx=10,pady=15)
    global button_8
    button_8 = CTkButton(window, text="Plot the graph", fg_color="#E0984B",text_color="black", command=save_choosen_value)
    button_8.pack(padx=10)
    
    return None





def find_used_sensors(file) : 
    label_0.pack_forget()
    button_0.pack_forget() 
    #button_02.pack_forget() 
    total = 0
    number_of_lines = 0
    tab_average=[]
    global tab_used_sensors
    tab_used_sensors=[]

    with open(file, newline='') as csvfile :
        reader = csv.reader(csvfile)
        for k in range(0,36) : 
            mean_column = calculate_mean(file,k)
            tab_average.append(mean_column)
    for i in range(0,len(tab_average)) : 
        if tab_average[i] >= 10:
            tab_used_sensors.append(i)
    global text_2
    global label_2
    text_2 = Text(window)
    label_2 = CTkLabel(window, text = "Sensor map and corresponding columns on the .CSV file",font=("Keyboard",18))
    label_2.pack(padx=4, pady=20)
    global img 
    img = PhotoImage(file='map.png')
    global label
    label=Label(window, image=img)
    label.pack()
    global text_3
    global label_3
    text_3 = Text(window, height = 5, width = 52)
    label_3 = CTkLabel(window, text = f"The used sensors must be the sensors number {tab_used_sensors}.", font=("Keyboard",12))
    label_3.pack(padx=4, pady=10)
    global button_2
    button_2 = CTkButton(window, text="Analyse data for the used sensors", fg_color="#E0984B",text_color="black", command=display_analysis)
    button_2.pack(padx=4, pady=20)
    return tab_used_sensors, tab_average

def chose_file():
    #label_0.pack_forget()
    #button_0.pack_forget() 
    #global text_1
    #text_1 = Text(window, height = 5, width = 52)
    #global label_1
    #label_1 = CTkLabel(window, text = "Choose a .CSV file to analyse", font=("Keyboard",14))
    #label_1.pack(padx=4, pady=20)
    #global button_1
    #button_1 = CTkButton(window, text="Load a file", fg_color="#E0984B",text_color="black", command=welcome_window())
    #button_1.pack()
    global csv_file
    csv_file = filedialog.askopenfilename(filetypes=(("Fichiers CSV", "*.csv"),))
    find_used_sensors(csv_file)
    return csv_file

def plot(file,column):
    x = []
    y = []
    time=0
    with open(file, 'r') as file:
        lines_reader = csv.reader(file, delimiter=',')
        for line in lines_reader:
            time+=1/3
            y.append(float(line[column]))
            x.append(time)
    plt.plot(x, y, label=f'Sensor {column}')
    plt.xlabel('Time in s')
    plt.ylabel('Capacity in pF')
    plt.title('Capacity through time')
    plt.legend()  # Ajoutez une légende
    plt.grid(True)
    plt.show()



def welcome_window():
    global img_1
    img_1 = PhotoImage(file='pressure_sensors.png')
    global label_0
    label_0=Label(window, image=img_1)
    label_0.pack()
    global button_0
    button_0 = CTkButton(window, text="Automatic analysis : load a file", fg_color="#E0984B",text_color="black", width=200, command=chose_file)
    button_0.pack(pady=30)
    #global button_02
    #button_02 = CTkButton(window, text="Choose a column", fg_color="#E0984B",text_color="black", width=200, command=chose_file)
    #button_02.pack()
    return None


welcome_window()






window.mainloop() # maintain the window



