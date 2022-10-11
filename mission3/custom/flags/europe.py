from ui import UIConfig
from artist import Artist
from math import sin, cos, pi
def europe_flag(config: UIConfig, artist: Artist):

    #STYLE CONSTANTS (Cela concerne juste l'apparence du drapeau européen)
    ratio_star_size = 1/25
    stars_number = 12
    star_angle_number = 5
    star_ray = config.flagSize/5
    ratio = 2/3
    width = config.flagSize
    height = config.flagSize * ratio
    artist.draw_rectangle(width, -height,"blue")
    starSize = config.flagSize*ratio_star_size
    artist.turtle.forward(width/2)
    artist.turtle.left(90)
    artist.turtle.forward(height/2 - starSize/2)
    artist.turtle.right(90)
    center = artist.turtle.pos()
    for x in range(stars_number):
        angle = (360/stars_number)*(x+1)
        sinus = sin(angle*(pi/180))
        cosinus = cos(angle*(pi/180))
        artist.turtle.penup()
        artist.turtle.goto(center[0]+(cosinus*star_ray), center[1]-(sinus*star_ray))
        artist.turtle.pendown()
        artist.draw_star(star_angle_number,"yellow", starSize)