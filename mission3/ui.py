import turtle
import tkinter as tk
import tkinter.ttk as ttk
from registry import FlagsRegistry
class UIConfig:
    def __init__(self, window, registry: FlagsRegistry):
        self.master = window.canvas.master
        self.registry = registry
        self.window = window
        self.flagSize = 200
        self.clickCallback = None
        self.init_ui()
        turtle.onscreenclick(self.onclick, add=True)
    def init_ui(self):
        self.draw_button_lines()
        self.add_turtle_button()
        self.add_country_choice()
        self.add_size_choice()

    def draw_button_lines(self):
        """
        Cette fonction sert juste a créer une ligne pour séparer la zone de contrôle et la zone de dessin
        """
        turtle.penup()
        turtle.goto(-25, 25)
        turtle.pendown()
        turtle.forward(1825)
        turtle.penup()

    def add_turtle_button(self):
        """
        On utilise la libairie tkinter pour les boutons, select, ...
        Command correspond a la fonction qui sera executée au click 
        Et canvas.master provient de turtle et permet d'afficher le bouton sur l'écran turtle
        """
        button = tk.Button(self.master, text="Toogle turtle", command=self.window.toogle_turtle)
        button.pack()
        button.place(x=15,y=8)


    def add_label(self,text, x, y):
        """
        Fonction utilitaire pour ajouter un texte a l'écran
        """
        var = tk.StringVar()
        label = tk.Label(self.master, textvariable=var)
        var.set(text)
        label.pack()
        label.place(x=x, y=y)
    
    def get_country(self):
        return self.registry.get_flag(self.selectBox.get())


    def add_country_choice(self):
        countries_names = list(self.registry.flags.keys())
        self.selectBox = ttk.Combobox(self.master, values=countries_names)
        self.add_label("Select country", 100, 10)
        self.selectBox.current(0)
        self.selectBox.pack()
        self.selectBox.place(x=200, y=10)

    def set_size(self,event):
        text = self.numberEntry.get()
        try:
            self.flagSize = int(text)
        #Si l'utilisateur ne rentre pas un chiffre valide, on écrit Not a number
        except ValueError:
            self.numberEntry.delete(0, tk.END)
            self.numberEntry.insert(0, "Not a number !") 

    def add_size_choice(self):
        self.add_label("Flag size", 350, 10)
        self.numberEntry = tk.Entry(self.master)
        self.numberEntry.insert(10,"200")
        self.numberEntry.bind("<Return>", self.set_size)

        self.numberEntry.pack()
        self.numberEntry.place(x=400,y=10)

    def onclick(self, x,y):
        if y < 25:
            return # Block y if it's below 25 so the user can't draw anything on the control bar.
        self.clickCallback(x, y)
