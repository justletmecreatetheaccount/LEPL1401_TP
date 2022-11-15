import mutagen
import os
import argparse

class bcolors:
    """
    Colors special chars for terminal
    """
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def color(text, bcolor, end=bcolors.ENDC):
    """
    Will return a string with colored text
    """
    
    return f"{bcolor}{text}{end}"

class FakeID3:
    def __init__(self, text) -> None:
        self.text = [text]

class Duree :
    def __init__(self,h,m,s):
        if m > 60 or s > 60:
            raise ValueError("Minutes and seconds can't be upper than 60.")
        self.hours = h
        self.minutes = m
        self.secondes = s
    def to_secondes(self):
        return int(self.hours * 60 * 60 + self.minutes * 60 + self.secondes)
    def delta(self,d) :
        return self.to_secondes() - d.to_secondes()
    def apres(self,d):
        return self.delta(d) > 0
    def ajouter(self,d, isSecondes=False): #
        """
        isSecondes is to allow to add a certain amount of seconds. That's because we cannot initialise Duree with more than 60 secs
        """
        secondes = d.to_secondes() if not isSecondes else d
        add_secondes = self.secondes + secondes 
        self.secondes = add_secondes % 60
        add_minutes = int((add_secondes - self.secondes) / 60) + self.minutes    
        self.minutes = add_minutes % 60
        self.hours = int((add_minutes - self.minutes) / 60) + self.hours
    def __str__(self):
        return "{:02}:{:02}:{:02}".format(self.hours, self.minutes, self.secondes)
        
class Chanson :
    def __init__(self, t, a,d) -> None:
        self.titre = t
        self.auteur = a
        self.duree = d
    def __str__(self):
        return f"{color(self.titre, bcolors.BLUE)} - {color(self.auteur, bcolors.GREEN)} - {color(self.duree, bcolors.YELLOW)}"

class Album :
    def __init__(self, numero, name=""):
        self.numero = numero
        self.chansons = []
        self.name = name #Addition to what is required to be able to load music from filesystem
        self._duree = Duree(0,0,0)
    def add(self, chanson):
        tmp_duree = Duree(self._duree.hours, self._duree.minutes, self._duree.secondes)
        tmp_duree.ajouter(chanson.duree)
        if len(self.chansons) >= 100 or tmp_duree.to_secondes() > 75 * 60:
            return False
        self.chansons.append(chanson)
        self._duree.ajouter(chanson.duree)

    def  __str__(self):
        result = color(f"{'Album '+str(self.numero) if self.numero > 0 else self.name} ({len(self.chansons)} chansons, {self._duree})", bcolors.CYAN)

        for (i, x) in enumerate(self.chansons):
            result += color("\n{:02d}: {}".format(i, x), bcolors.BLUE) #TODO: Display i in two digits
        return result

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


class FileLoader():
    def __init__(self) -> None:
        pass
    def get_albums(self, filename):
        albums = [Album(1)]
        with open(filename) as f:
            content = f.readlines()
            for line in content:
                title, author, min, sec = line.split(" ")
                song = Chanson(title, author, Duree(0, int(min), int(sec)))
                while albums[-1].add(song) == False:
                    albums.append(Album(len(albums)+1))
        return albums
    def load_directory(self, directory, max_depth=2):
        albums = {}
        for directory, _, files in walklevel(directory, max_depth):
            for fileName in files:
                path = f"{directory}/{fileName}"
                file = mutagen.File(path)
                if not file:
                    continue
                art  = (file.get("TPE1", FakeID3("Unknown Artist"))).text[0]
                song = (file.get("TIT2", FakeID3(".".join(fileName.split(".")[:-1])))).text[0]
                alb  = (file.get("TALB", FakeID3(directory.split("/")[-1]))).text[0]
                albHash = hash(f"{alb}-{art}")
                if not albHash in albums.keys():
                    albums[albHash] = Album(0,name=alb)
                duration = int(file.info.length)
                d = Duree(0,0,0)
                d.ajouter(duration, isSecondes=True)
                albums[albHash].add(Chanson(song, art, d))
        return albums.values()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'Music Indexer',
                    description = "It's gonna index music from either your computer or a txt db file",
                    epilog = 'Never Gonna Give You Up.')
    parser.add_argument('--filename','-f', default="music-db.txt", required=False)           # positional argument

    args = parser.parse_args()
    path = args.filename
    loader = FileLoader()
    albums = []
    if os.path.isdir(path):
        albums = loader.load_directory(path)
    else:
        albums = loader.get_albums(path)
    for album in albums:
        print(album)
        print("\n\n")
