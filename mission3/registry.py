class FlagsRegistry:
    def __init__(self):
        self.flags = {}
    def add_flag(self, countryName, colors=[], stars=[],ratio=1/2, horizontal=True,callback=None):
        self.flags[countryName] = {
            "colors": colors,
            "ratio": ratio,
            "horizontal": horizontal,
            "callback": callback,
            "stars": stars
        }
    def get_flag(self, country):
        return self.flags[country]
   