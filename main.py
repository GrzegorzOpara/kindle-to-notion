import os
from classes.book import Books
from classes.file import KindleFile
from classes.notion import Notion
    
def main():

    kindleFile = KindleFile("My Clippings.txt")
    
    books = Books()
    books.createBooksFromHighlights(kindleFile.parseFile())
    
    notion = Notion(os.environ["NOTION_TOKEN"], os.environ["NOTION_DB"])
    notion.processBooks(books)

if __name__ == "__main__":
    main()



