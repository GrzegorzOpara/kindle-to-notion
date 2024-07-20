from highlight import Highlight

class Book(object):
    """
    This class represents a book with its title, author, and associated highlights.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        highlights (list[Highlight]): A list of `Highlight` objects associated with the book.

    Methods:
        add_highlight(highlights: Highlight): Adds a `Highlight` object to the book's highlight list.
        sort_highlight_by_location(): Sorts the highlight list by their location within the book (not implemented yet).
    """
    def __init__(self, title, author, highlights=[]) -> None:
        self.title = title
        self.author = author
        self.highlights = highlights

    def add_highlight(self, highlights):
        self.highlights.append(highlights)
        pass

    def sort_highlight_by_location() -> None:
        pass

class Books(object):
    """
    Creates and returns a list of Book objects from a list of Highlight objects.

    Attributes:
        highlights: A list of Highlight objects.

    Returns:
        A list of Book objects.
    """
    
    def __init__(self) -> None:
        self.books = []

    def create_books_from_highlights(self, highlights) -> None:
        """
            param: highlights
            return: list of Books
        """      
        for highlight in highlights:
            found = False
            if not isinstance(highlight, Highlight):
                raise TypeError("Invalid highlight object found in highlights list.")
            
            for book in self.books:
                if highlight.title.strip() == book.title:
                    found = True
                    book.add_highlight(highlight)
                    break

            if not found:
                self.books.append(Book(highlight.title.strip(), highlight.author.strip(), [highlight]))
                            
        pass

    def get_books(self) -> list:
        return self.books

