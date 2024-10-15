#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
"""
Created on Wed Feb 14 08:58:36 2024

@author: afdol
"""

def wire_2 (filename, x1, y1, x2, y2):
    wide = 0.2
    car = ('Wire ' + str(wide) + ' (' + str(x1) + ' ' + str(y1) + ') (' + str(x2) + ' ' + str(y2) + ')' )
    file = open(filename, 'a')
    file.write(car + '\n')
    file.close()

def rect_2 (filename, x1, y1, x2, y2):
    car = ('Rect' + ' (' + str(x1) + ' ' + str(y1) + ') (' + str(x2) + ' ' + str(y2) + ')' )
    file = open(filename, 'a')
    file.write(car + '\n')
    file.close()

def erase (filename):
    file = open(filename, 'w')
    file.write('')
    file.close()

def diel_rect_vert (fn, x1, y1):
    incr = 0.5
    i = -0.2
    while (i <= 3.2):
        wire_2(fn, x1+i, y1 - 0.3, x1+i, y1 + 3.3 )
        i = i + incr
        wire_2(fn, x1+i, y1 + 3.3, x1+i, y1 - 0.3 )
        i = i + incr

def diel_rect_hor (fn, x1, y1):
    incr = 0.5
    i = -0.2
    while (i <= 3.2):
        wire_2(fn, x1 - 0.3, y1 + i, x1 + 3.3, y1 + i)
        i = i + incr
        wire_2(fn, x1 + 3.3, y1 + i, x1 - 0.3, y1 + i)
        i = i + incr

def bottomelec_nxn (fn, x1, y1,  nx, ny):
    wire_2(fn, x1 + 29 + (nx *5), y1 + 0, x1 + 29 + (nx *5), y1 + 4 )
    wire_2(fn, x1 + 27 + (nx *5), y1 + 2, x1 + 31 + (nx *5), y1 + 2 )
    wire_2(fn, x1 + 29 + (nx *5), y1 - 6 + (ny*2.5), x1 + 29 + (nx *5), y1 + 6 + (ny*2.5))
    wire_2(fn, x1 + 29 + (nx *5), y1 + 2 + (ny*5), x1 + 29 + (nx *5), y1 + 6 + (ny*5))
    wire_2(fn, x1 + 27 + (nx *5), y1 + 4 + (ny*5), x1 + 31 + (nx *5), y1 + 4 + (ny*5))
    
    wire_2(fn, x1 + 0, y1 + 4, x1 + 25 + (nx*5), y1 + 4)
    for i in range (1, ny):
        wire_2(fn, x1 + 0, y1 + 4 + i, x1 + 27 - (i*2), y1 + 4 + i)
        wire_2(fn, x1 + 27 - (i*2), y1 + 4 + i, x1 + 27 - (i*2), y1 + 4 + i +(i*4))
        wire_2(fn, x1 + 27 - (i*2), y1 + 4 + i +(i*4), x1 + 25 + (nx*5), y1 + 4 + i +(i*4))

    for i in range (0, nx):
        for j in range (0, ny):
            rect_2(fn, x1+27+(i*5), y1+4+(j*5), x1+30+(i*5), y1+7+(j*5))

def topelec_nxn (fn, x1, y1,  nx, ny):
    wire_2(fn, x1 + 29 + (nx *5), y1 + 0, x1 + 29 + (nx *5), y1 + 4 )
    wire_2(fn, x1 + 27 + (nx *5), y1 + 2, x1 + 31 + (nx *5), y1 + 2 )
    
    wire_2(fn, x1 + 29 + (nx *5), y1 - 6 + (ny*2.5), x1 + 29 + (nx *5), y1 + 6 + (ny*2.5))
    
    wire_2(fn, x1 + 29 + (nx *5), y1 + 2 + (ny*5), x1 + 29 + (nx *5), y1 + 6 + (ny*5))
    wire_2(fn, x1 + 27 + (nx *5), y1 + 4 + (ny*5), x1 + 31 + (nx *5), y1 + 4 + (ny*5))
    
    for i in range (0, nx):
        for j in range (0, ny):
            wire_2(fn, x1 + 0, y1 + 4 - i, x1 + 30 + (i*5), y1 + 4 - i)
            wire_2(fn, x1 + 30 + (i*5), y1 + 4 - i, x1 + 30 + (i*5), y1 + 7 + (j*5))
        
        #wire_2(fn, x1 + 27 - (i*2), y1 + 4 + i, x1 + 27 - (i*2), y1 + 4 + i +(i*4))
        #wire_2(fn, x1 + 27 - (i*2), y1 + 4 + i +(i*4), x1 + 25 + (nx*5), y1 + 4 + i +(i*4))

    for i in range (0, nx):
        for j in range (0, ny):
            rect_2(fn, x1+27+(i*5), y1+4+(j*5), x1+30+(i*5), y1+7+(j*5))
            
def dielbottom (fn, x1, y1, nx, ny): 
    for i in range (0, nx):
        for j in range (0, ny):
            diel_rect_vert(fn, x1 + (i*5), y1 + (j*5))
            
def dieltop (fn, x1, y1, nx, ny): 
    for i in range (0, nx):
        for j in range (0, ny):
            diel_rect_hor(fn, x1 + (i*5), y1 + (j*5))





def main():
    def submit():
        nx = int(entry_nx.get())
        ny = int(entry_ny.get())
        # Injecter cette valeur dans topelec_nxn et bottomelec_nxn
        topelec_nxn('{}x{} matrixtop.scr'.format(nx, ny), 0, 0, nx, ny)
        bottomelec_nxn('{}x{} matrixbottom.scr'.format(nx, ny), 63, 0, nx, ny)

    # Créer une fenêtre Tkinter
    root = tk.Tk()
    root.title("Entrée des capteurs")
    root.geometry('500x200')  # Rendre la fenêtre plus grande
    root.configure(bg='lightblue')  # Ajouter de la couleur

    # Créer des champs de saisie pour nx et ny
    tk.Label(root, text="Nombre de capteurs en ligne:", bg='lightblue').grid(row=0)
    tk.Label(root, text="Nombre de capteurs en colonne:", bg='lightblue').grid(row=1)
    entry_nx = tk.Entry(root)
    entry_ny = tk.Entry(root)
    entry_nx.grid(row=0, column=1)
    entry_ny.grid(row=1, column=1)

    # Créer un bouton de soumission qui récupère les valeurs de nx et ny et appelle les fonctions appropriées
    submit_button = tk.Button(root, text="Entrée", command=submit, bg='lightgreen')
    submit_button.grid(row=2, column=1)

    # Créer un bouton Quitter qui ferme la fenêtre
    quit_button = tk.Button(root, text="Quitter", command=root.destroy, bg='salmon')
    quit_button.grid(row=3, column=1)

    # Exécuter la boucle principale de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()