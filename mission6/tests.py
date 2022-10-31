import unittest
from main import *
class MockAssistant(Assistant):
    def speak(self, text):
        #Remove colors
        colorsName = [ x for x  in dir(bcolors) if not x.startswith("_") ]
        for color in colorsName:
            text = text.replace(getattr(bcolors, color), "")

        self.output = text
assistant = MockAssistant("Demo assistant")
assistant.set_file("all-words.dat")


class AssistantTest(unittest.TestCase):
    def test_file_info(self):
        file_info(assistant, [])
        self.assertEqual(assistant.output, "Lines 113005\n Chars 1330218")

if __name__ == "__main__":
    unittest.main(verbosity=2) 