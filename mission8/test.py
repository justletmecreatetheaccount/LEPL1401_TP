import unittest
from mission8 import Chanson, Duree, Album

class DureeTest(unittest.TestCase):
    def test_to_seconds(self):
        u = Duree(2,2,2)
        seconds = 2*60*60 + 2*60 + 2
        self.assertEqual(seconds, u.to_secondes())
    def test_detla(self):
        u = Duree(2,0,0)
        a = Duree(0,2,0)
        self.assertEqual(u.delta(a), 1*60*60+58*60)
    def test_ajout(self):
        u = Duree(2,35,0)
        a = Duree(1, 30, 58)
        u.ajouter(a)
        self.assertEqual(u.to_secondes(),Duree(4,5,58).to_secondes())
    def test_apres(self):
        u = Duree(2,0,0)
        a = Duree(5,0,0)
        self.assertTrue(a.apres(u))
        self.assertFalse(u.apres(a))
    def test_raise(self):
        with self.assertRaises(ValueError):
            Duree(100,100,100)
    def test_str(self):
        u = Duree(1,2,3)
        self.assertEqual(u.__str__(), "01:02:03")

class ChansonTest(unittest.TestCase):
    def test_basic(self):
        chanson = Chanson("Super song","Super artist", Duree(1,0,0))
        self.assertEqual(chanson.auteur, "Super artist")
        self.assertEqual(chanson.titre, "Super song")
        self.assertEqual(chanson.duree.to_secondes(), Duree(1,0,0).to_secondes())

class AbumTest(unittest.TestCase):
    def test_basic(self):
        album = Album(5)
        self.assertEqual(album.chansons, [])
        self.assertEqual(album.numero, 5)
        chanson = Chanson("Super song","Super artist", Duree(1,0,0))
        album.add(chanson)
        self.assertEqual(album.chansons, [chanson])
    def test_length_add(self):
        album = Album(0)
        duree = Duree(0,1,0)
        for _ in range(75):
            album.add(Chanson("", "", duree))
        self.assertEqual(len(album.chansons), 75)
        self.assertFalse(album.add(Chanson("","", duree)), 75)

if __name__ == "__main__":
    unittest.main(verbosity=2)
