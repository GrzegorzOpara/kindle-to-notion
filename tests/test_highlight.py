import unittest
from modules.highlight import Highlight

class TestHighlight(unittest.TestCase):  
    def test_create_highlight_with_incorrect_type(self):
        self.assertRaises(TypeError, Highlight, 1, "Author", "Title", "12", 12, "1", "2024/01/01", "Hello World!") 

if __name__ == '__main__':
    unittest.main()