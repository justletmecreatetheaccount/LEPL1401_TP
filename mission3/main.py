from window import Window
from registry import FlagsRegistry
from artist import Artist
from ui import UIConfig
from custom.flags.europe import europe_flag


registry = FlagsRegistry()
registry.add_flag("Belgique", colors=[("black", 1/3), ("yellow", 1/3), ("red", 1/3)], ratio=2/3)
registry.add_flag("Cameroun", colors=[("green", 1/3), ("red", 1/3), ("yellow", 1/3)], ratio=2/3, stars=[{
    "color": "yellow",
    "size": 1/8,
    "position": (1/2, 1/2),
    "sides": 5
}])
registry.add_flag("France", colors=[("blue", 1/3), ("white", 1/3), ("red", 1/3)], ratio=2/3)
registry.add_flag("Monaco", colors=[("red", 1/2), ("white", 1/2)], ratio=2/3, horizontal=False)
registry.add_flag("Ukraine", colors=[("blue", 1/2), ("yellow", 1/2)], ratio=2/3, horizontal=False)
registry.add_flag("Pologne", colors=[("white", 1/2), ("red", 1/2)], ratio=2/3, horizontal=False)
registry.add_flag("Lituanie", colors=[("yellow", 1/3),  ("green", 1/3), ("red", 1/3)], ratio=2/3, horizontal=False)
registry.add_flag("Italie", colors=[("green", 1/3), ("white", 1/3), ("red", 1/3)], ratio=2/3)
registry.add_flag("Estonie", colors=[("blue", 1/3), ("black", 1/3), ("white", 1/3)], ratio=2/3, horizontal=False)
registry.add_flag("Allemagne", colors= [("black",1/3),("red",1/3),("yellow",1/3)], ratio=3/5, horizontal=False)
registry.add_flag("Arménie", colors= [("red",1/3),("blue",1/3),("orange",1/3)], ratio=3/5, horizontal=False)
registry.add_flag("Autriche", colors= [("red",1/3),("white",1/3),("red",1/3)], ratio=3/5, horizontal=False)
registry.add_flag("Bolivie", colors= [("red",1/3),("yellow",1/3),("green",1/3)], ratio=3/5, horizontal=False)
registry.add_flag("Bulgarie", colors= [("white",1/3),("green",1/3),("red",1/3)], ratio=3/5, horizontal=False)
registry.add_flag("Costa Rica", colors= [("blue",1/6),("white",1/6),("red",2/6),("white",1/6), ("blue",1/6)], ratio=3/5, horizontal=False)
registry.add_flag("Russia", colors=[("white", 1/3), ("blue", 1/3), ("red", 1/3)], ratio=2/3, horizontal=False)

registry.add_flag("Europe", callback=europe_flag)


window = Window(1800, 900, "Flags TP")
config = UIConfig(window=window, registry=registry)
artist = Artist(window, config)
artist.wait()