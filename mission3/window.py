import turtle
class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.isTurtle = False
        turtle.title(title)
        screen = turtle.Screen()
        screen.bgcolor("#f5f5f5") #On met un fond d'écran gris pour éviter que les drapeaux avec du blanc ne soient que peu visibles
        screen.setup(width=width, height=height)
        screen.setworldcoordinates(0, height, width, 0)
        turtle.speed("fastest")  
        turtle.hideturtle()
        self.canvas = screen.getcanvas()

    def toogle_turtle(self):
        if self.isTurtle:
            turtle.hideturtle()
            turtle.speed("fastest")
        else:
            turtle.shape("turtle")
            turtle.showturtle()
            turtle.speed("slow")
        self.isTurtle = not self.isTurtle
