# from typing import Union

class Highlight(object):
    """
    This class represents a highlighted text from the book. 

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        page (int): The page number where the highlight is found (can be a string representation of an integer).
        location_start (int): The starting location of the highlight within the source (can be a string representation of an integer).
        location_end (int): The ending location of the highlight within the source (can be a string representation of an integer).
        date_added (str): The date the highlight was added.
        text (str): The actual highlighted text.
        note (str, optional): An optional note associated with the highlight. Defaults to an empty string.

    Raises:
        TypeError: If any of the required attributes (`title`, `author`, `page`, or `text`) are not strings, 
                or if `page`, `location_start`, or `location_end` are not both integers or strings.
    """


    def __init__(self, title: str, author: str, page: str | int, location_start: str | int, location_end: str | int, date_added: str, text: str) -> None:        
        self.title = title
        self.author = author
        self.page = int(page)
        self.location_start = int(location_start)
        self.location_end = int(location_end)
        self.added_date = date_added
        self.highlight = text
        self.note = ""

        if not all(isinstance(arg, str) for arg in [title, author, page, text]):
            raise TypeError('title, author, page, text must be int type not %s %s %s %s' % (type(title), type(author), type(page), type(text)))
        
        if not all(isinstance(arg, str) for arg in [page, location_start, location_end]) or all(isinstance(arg, int) for arg in [page, location_start, location_end]):
            raise TypeError('page, location_start, location_end must be either int or string type not %s %s %s' % (type(page), type(location_start), type(location_end)))

    def __str__(self):
        return f"{self.title} ({self.author})\npage: {self.page} ({self.location_start} - {self.location_end}), added: {self.added_date}\ntext: {self.highlight}note: {self.note}\n" 

