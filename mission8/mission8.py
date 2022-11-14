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
    def ajouter(self,d):
        secondes = d.to_secondes()
        add_secondes = self.secondes + secondes 
        self.secondes = add_secondes % 60
        add_minutes = int((add_secondes - self.secondes)) / 60 + self.minutes    
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
        return f"{self.titre} - {self.auteur} - {self.duree}"

class Album :
    def __init__(self, numero):
        self.numero = numero
        self.chansons = []
        self._duree = Duree(0,0,0)
    def add(self, chanson):
        tmp_duree = Duree(self._duree.hours, self._duree.minutes, self._duree.secondes)
        tmp_duree.ajouter(chanson.duree)
        if len(self.chansons) >= 100 or tmp_duree.to_secondes() > 75 * 60:
            return False
        self.chansons.append(chanson)
        self._duree.ajouter(chanson.duree)

    def  __str__(self):
        result = f"Album {self.numero} ({len(self.chansons)} chansons, {self._duree})"
        for (i, x) in enumerate(self.chansons):
            result += f"\n0{i}: {x.titre} - {x.auteur} - {x.duree}" #TODO: Display i in two digits
        return result

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
                    print("##################")
                    albums.append(Album(len(albums)+1))
        return albums


if __name__ == "__main__":
    loader = FileLoader()
    albums = loader.get_albums("music-db.txt")
    for album in albums:
        print(album)
        print("\n\n")