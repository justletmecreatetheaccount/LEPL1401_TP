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
        width = self.config.flagSize
        ratio = country["ratio"]
        height = width * country["ratio"]

        #Certains drapeaux (Europe) ne peuvent être dessinés via des simples bandes, j'appelle donc la fonction propre au drapeau qu'on essaie de dessiner
        if country["callback"] != None: 
            country["callback"](self.config,self)
            self.isDrawing = False
            return
        
        turtle.pendown()
        
        #La fonction horizontale sert a faire des drapeaux dans différentes orientations (Belgique = horizontal, Allemagne = vertical)
        horizontal = country["horizontal"]

        if not horizontal:
            width = width * ratio

        angle = 0 if horizontal else 90

        turtle.right(angle)

        for (color, color_ratio) in country["colors"]:
            color_width =  width * color_ratio * (1 if horizontal else -1) # If width = 200 but color only 1/2, color_width will be 100
            color_height = width * (ratio if horizontal else 1/ratio) # If height is width/2, then height will be 100
            self.draw_rectangle(color_width, -color_height, color) # color_height is times -1 to draw below the cursor.
            turtle.forward(color_width)
        turtle.right(-angle)
        turtle.forward(-width)
        home_x,home_y = turtle.pos()
        if len(country["stars"]) > 0 or True:
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