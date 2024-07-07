class Book(object):
    def __init__(self, title, author, highlights=[]) -> None:
        self.title = title
        self.author = author
        self.highlights = highlights

    def addHighlight(self, highlights):
        self.highlights.append(highlights)
        pass

    def sortHighlightByLocation() -> None:
        pass

class Books(object):
    def __init__(self) -> None:
        self.books = []

    def createBooksFromHighlights(self, highlights) -> None:
        """
            param: highlights
            return: list of Books
        """      
        for highlight in highlights:
            found = False
            
            for book in self.books:
                if highlight.title.strip() == book.title:
                    found = True
                    book.addHighlight(highlight)
                    break

            if not found:
                self.books.append(Book(highlight.title.strip(), highlight.author.strip(), [highlight]))
                            
        pass

    def getBooks(self) -> list:
        return self.books

