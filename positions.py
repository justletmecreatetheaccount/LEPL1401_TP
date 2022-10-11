import turtle

def stairs():
    for x in range(3):
        turtle.forward(20)
        turtle.right(90)
        turtle.forward(20)
        turtle.left(90)
stairs()
turtle.done()
