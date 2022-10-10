from window import Window
from registry import FlagsRegistry
from artist import Artist
from ui import UIConfig
from custom.flags.europe import europe_flag


registry = FlagsRegistry()
registry.add_flag("Belgique", colors=[("black", 1/3), ("yellow", 1/3), ("red", 1/3)], ratio=2/3)
registry.add_flag("France", colors=[("blue", 1/3), ("white", 1/3), ("red", 1/3)], ratio=2/3)
registry.add_flag("Allemagne", colors= [("black",1/3),("red",1/3),("yellow",1/3)], ratio=3/5, horizontal=False)
registry.add_flag("Europe", callback=europe_flag)

window = Window(1800, 900, "Flags TP")
config = UIConfig(window=window, registry=registry)
artist = Artist(window, config)
artist.wait()