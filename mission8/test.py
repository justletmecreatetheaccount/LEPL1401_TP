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


if __name__ == "__main__":
    unittest.main(verbosity=2)