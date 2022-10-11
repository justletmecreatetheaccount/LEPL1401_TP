from ui import UIConfig
import turtle
class Artist:
    def __init__(self, window, config: UIConfig):
        self.isDrawing = False
        self.window = window
        self.config = config
        self.turtle = turtle
        config.clickCallback = self.flag
    def draw_rectangle(self,width, height, color):
        """
        Basé sur la fonction square donnée par le professeur
        """
        turtle.color(color)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(width)
            turtle.right(90)
            turtle.forward(height)
            turtle.right(90)
        turtle.end_fill()
        turtle.penup()
    def draw_star(self,n, color, size):
        """
        Permet de dessiner une étoile a n cotés, et size correspond au "diamètre" de celle ci.
        """
        turtle.color(color)
        turtle.fillcolor(color)
        turtle.begin_fill()
        turtle.pendown()
        offset_angle = 180-(180/n*2) 
        turtle.left(offset_angle)
        for x in range(n):
            turtle.forward(size)
            turtle.right(180-(180/n))
        turtle.right(offset_angle)
        turtle.end_fill()
    def flag(self,x,y, country=None):
        """
        Probablement la fonction la plus complexe de ce programme. Elle permet de dessiner n'importe quel drapeau constitué de X bandes de couleur différentes.
        """
        
        if self.isDrawing: # Ce check évite de dessiner deux drapeaux en même temps
            return
        self.isDrawing = True

        
        # Aller a la bonne position
        turtle.penup()
        turtle.goto(x,y)

        country = country if country else self.config.get_country()
        ratio = country["ratio"]
        
        width = self.config.flagSize
        height = width * country["ratio"]

        #Certains drapeaux (Europe) ne peuvent être dessinés via des simples bandes, j'appelle donc la fonction propre au drapeau qu'on essaie de dessiner
        if country["callback"] != None: 
            country["callback"](self.config,self)
            self.isDrawing = False
            return
        
        turtle.pendown()
        
        #La fonction horizontale sert a faire des drapeaux dans différentes orientations (Belgique = horizontal, Allemagne = vertical)
        horizontal = country["horizontal"]


        print("Total size: ",width, height)

        for (color, color_ratio) in country["colors"]:
            color_width =  width * color_ratio if horizontal else width
            color_height = height if horizontal else height * color_ratio
            print(color, color_width, color_height)
            self.draw_rectangle(color_width, -color_height, color) # color_height is times -1 to draw below the cursor.

            #Placement pour le prochain bloc de couleur si vertical
            if not horizontal: 
                turtle.right(90)
                turtle.forward(-color_height)
                turtle.left(90)
            else: 
                turtle.forward(color_width)

        #Retour au coin supérieur gauche du drapeau
        if horizontal:
            turtle.forward(-width)
        else:
            turtle.right(90)
            turtle.forward(height)
            turtle.left(90)
        home_x,home_y = turtle.pos()
        for star in country["stars"]:
            starSize = width * star["size"]
            turtle.penup()
            turtle.goto(home_x, home_y)
            turtle.forward(width*star["position"][0])
            turtle.right(90)
            turtle.forward(-height*star["position"][1]+starSize/2)
            turtle.left(90)
            self.draw_star(star["sides"], star["color"], width*star["size"])
            
        self.isDrawing = False
    def wait(self):
        turtle.done()