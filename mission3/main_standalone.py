"""
Mission 3
Groupe: Théo Daron et Vlad Doniga
Local BARB15
11 octobre 2022
Objectif: Programme qui dessine des drapeaux.

Mot clé inhabituel du programme: global

variable = 0
def super_function():
    global variable
    variable = 1

global permet de dire qu'on peut modifier une variable déclarée en dehors d'une fonction.
Sans ce mot clé, je ne pourrais pas modifier variable a l'intérieur de ma fonction.

On utilise également beaucoup d'expressions ternaires du genre

a = "vrai" if condition else "faux"

Cela mettra "vrai" dans a si la condition est respectée, sinon "faux"

Une version plus propre du code (Avec de la POO) et divisée en plusieurs fichiers est disponible a cette adresse:
https://github.com/Kaporos/LEPL1401_TP/tree/main/mission3

Cette version est également plus complete (+ de drapeaux disponibles, ... ) car plus facile a étendre grâce a la POO !

"""

import tkinter as tk
import tkinter.ttk as ttk
import turtle
from math import sin, cos, pi
tortue = turtle.Turtle()

"""
Program State (variables qui seront modifiées grâce a un global)
"""
isTurtle = False # Booléen correspondant a l'état d'affichage du curseur turtle (visible/invisible)
selectBox = None # Dedans sera stocké le select qui permet de choisir le pays
numberEntry = None # Correspond a l'input de la taille du flag
isDrawing = False # Variable permettant d'éviter de dessiner deux drapeaux a la fois
flag_size = 200 # Valeur par défaut, sera paramétrable dans l'interface


"""
Program State Modifiers
"""


def toogle_turtle():
    """
    Cette fonction rend le curseur de turtle visible/invisible et change sa vitesse de déplacement.
    Très utile pour débug.
    """
    global isTurtle
    if isTurtle:
        tortue.hideturtle()
        tortue.speed("fastest")
    else:
        tortue.shape("turtle")
        tortue.showturtle()
        tortue.speed("slow")
    isTurtle = not isTurtle

def set_country_choice(event):
    global country
    country = selectBox.get() #Permet de récupérer la valeur du select de l'UI

def set_size(event):
    global flag_size
    text = numberEntry.get()
    try:
        flag_size = int(text)
    #Si l'utilisateur ne rentre pas un chiffre valide, on écrit Not a number
    except ValueError:
        numberEntry.delete(0, tk.END)
        numberEntry.insert(0, "Not a number !") 

"""
Fonctions utiles (rectangle, flag,...)
"""
    
def rectangle(width, height, color):
    """
    Basé sur la fonction square donnée par le professeur
    """
    tortue.color(color)
    tortue.pendown()
    tortue.begin_fill()
    for i in range(2):
        tortue.forward(width)
        tortue.right(90)
        tortue.forward(height)
        tortue.right(90)
    tortue.end_fill()
    tortue.penup()

def etoile(n, color, size):
    """
    Permet de dessiner une étoile a n cotés, et size correspond au "diamètre" de celle ci.
    """
    tortue.color(color)
    tortue.fillcolor(color)
    tortue.begin_fill()
    tortue.pendown()
    for x in range(n):
        tortue.forward(size)
        tortue.right(180-(180/n))
    tortue.end_fill()

def flag(width,x,y, country):
    """
    Probablement la fonction la plus complexe de ce programme. Elle permet de dessiner n'importe quel drapeau constitué de X bandes de couleur différentes.
    """
    
    global isDrawing
    if isDrawing: # Ce check évite de dessiner deux drapeaux en même temps
        return
    isDrawing = True

    
    # Aller a la bonne position
    tortue.penup()
    tortue.goto(x,y)


    #Certains drapeaux (Europe) ne peuvent être dessinés via des simples bandes, j'appelle donc la fonction propre au drapeau qu'on essaie de dessiner
    if "callback" in country.keys(): 
        country["callback"]()
        isDrawing = False
        return
    
    ratio = country["ratio"]
    tortue.pendown()
    
    #La fonction horizontale sert a faire des drapeaux dans différentes orientations (Belgique = horizontal, Allemagne = vertical)
    horizontal = country["horizontal"]

    if not horizontal:
        width = width * ratio

    angle = 0 if horizontal else 90

    tortue.right(angle)

    for (color, color_ratio) in country["colors"]:
        color_width =  width * color_ratio * (1 if horizontal else -1) # If width = 200 but color only 1/2, color_width will be 100
        color_height = width * (ratio if horizontal else 1/ratio) # If height is width/2, then height will be 100
        rectangle(color_width, -color_height, color) # color_height is times -1 to draw below the cursor.
        tortue.forward(color_width)
    tortue.right(-angle)
    isDrawing = False

"""

DRAPEAUX CUSTOMS (Europe, ...)

"""

def europe_flag():

    #STYLE CONSTANTS (Cela concerne juste l'apparence du drapeau européen)
    ratio_star_size = 1/30
    stars_number = 12
    star_angle_number = 5
    star_ray = flag_size/6

    width = flag_size
    height = flag_size / 2
    rectangle(width, -height,"blue")
    tortue.forward(width/2)
    tortue.left(90)
    tortue.forward(height/2)
    tortue.right(90)
    center = tortue.pos()
    for x in range(stars_number):
        angle = (360/stars_number)*(x+1)
        sinus = sin(angle*(pi/180))
        cosinus = cos(angle*(pi/180))
        tortue.penup()
        tortue.goto(center[0]+(cosinus*star_ray), center[1]-(sinus*star_ray))
        tortue.pendown()
        etoile(star_angle_number,"yellow", flag_size*ratio_star_size)


"""
UI
"""


def init_ui(canvas, tortue):
    draw_button_lines()
    add_turtle_button(canvas)
    add_country_choice(canvas)
    add_size_choice(canvas)

def draw_button_lines():
    """
    Cette fonction sert juste a créer une ligne pour séparer la zone de contrôle et la zone de dessin
    """
    tortue.penup()
    tortue.goto(-25, 25)
    tortue.pendown()
    tortue.forward(1825)
    tortue.penup()

def add_turtle_button(canvas):
    """
    On utilise la libairie tkinter pour les boutons, select, ...
    Command correspond a la fonction qui sera executée au click 
    Et canvas.master provient de turtle et permet d'afficher le bouton sur l'écran turtle
    """
    button = tk.Button(canvas.master, text="Toogle turtle", command=toogle_turtle)
    button.pack()
    button.place(x=15,y=8)


def add_label(canvas, text, x, y):
    """
    Fonction utilitaire pour ajouter un texte a l'écran
    """
    var = tk.StringVar()
    label = tk.Label(canvas.master, textvariable=var)
    var.set(text)
    label.pack()
    label.place(x=x, y=y)


def add_country_choice(canvas):
    global selectBox
    countries_names = list(countries.keys())
    selectBox = ttk.Combobox(canvas.master, values=countries_names)
    add_label(canvas,"Select country", 100, 10)
    selectBox.bind("<<ComboboxSelected>>", set_country_choice) #Cette fonction sert a mettre a jour la variable country lorsque l'utilisateur change depuis le select
    selectBox.current(0)
    selectBox.pack()
    selectBox.place(x=200, y=10)


def add_size_choice(canvas):
    global numberEntry
    add_label(canvas, "Flag size", 350, 10)
    numberEntry = tk.Entry(canvas.master)
    numberEntry.insert(10,"200")
    numberEntry.pack()
    numberEntry.bind("<Return>", set_size)
    numberEntry.place(x=400,y=10)

def onclick(x,y):
    if y < 25:
        return # Block y if it's below 25 so the user can't draw anything on the control bar.
    flag(flag_size, x, y, countries[country])

"""
Main function (Code executé)
"""


countries = {
    "Belgique": {
        "horizontal":True,
        "ratio": 2/3,
        "colors": [("black",1/3),("yellow",1/3),("red", 1/3)]
    },
    "Allemagne": {
        "horizontal":False,
        "ratio": 3/5,
        "colors": [("black",1/3),("red",1/3),("yellow",1/3)]
    },
    "France": {
        "horizontal": True,
        "ratio": 2/3,
        "colors": [("blue", 1/3), ("white", 1/3), ("red", 1/3)]
    },
    "Europe": {
        "callback": europe_flag
    }
}

country = list(countries.keys())[0] #Le pays sélectionné par défaut est le premier (La belgique hehe)


if __name__ == "__main__":
    turtle.title("Flag TP")
    screen = turtle.Screen()
    screen.bgcolor("#f5f5f5")
    screen.setup(width=1800, height=900)
    screen.setworldcoordinates(0, 900, 1800, 0)
    tortue.speed("fastest")  
    tortue.hideturtle()
    canvas = screen.getcanvas()
    init_ui(canvas, tortue) #Add UI
    turtle.onscreenclick(onclick, add=True)
    turtle.done()
