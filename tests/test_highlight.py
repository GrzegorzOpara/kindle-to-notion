import unittest
from datetime import datetime
from modules.highlight import Highlight

class TestHighlight(unittest.TestCase):  

    def setUp(self):
        self.highlight = Highlight("Title", "Author", "12", 1, 10, "2024/01/01", "Hello World!")

    def test_create_highlight_with_incorrect_type(self):
        self.assertRaises(TypeError, Highlight, "Title", "Author", 12, 0, 10, datetime.strptime("2024/01/01", '%Y/%m/%d'), "Hello World!") 
        self.assertRaises(TypeError, Highlight, 12, "Author", 12, 0, 10, "2024/01/01", "Hello World!") 
        self.assertRaises(TypeError, Highlight, "Title", 0, 12, 0, 10, "2024/01/01", "Hello World!") 
        self.assertRaises(TypeError, Highlight, "Title", "Author", 12, 0, 10, "2024/01/01", 5) 

    def test_highlight_to_str(self):
        self.assertEqual(str(self.highlight), f"Title (Author)\npage: 12 (1 - 10), added: 2024/01/01\ntext: Hello World!\nnote: \n")

if __name__ == '__main__':
    unittest.main()