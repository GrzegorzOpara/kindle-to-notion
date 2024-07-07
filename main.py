import os
from modules.book import Books
from modules.file import KindleFile
from modules.notion import Notion
    
def main():

    kindleFile = KindleFile("My Clippings.txt")
    
    books = Books()
    books.createBooksFromHighlights(kindleFile.parseFile())
    
    notion = Notion(os.environ["NOTION_TOKEN"], os.environ["NOTION_DB"])
    notion.processBooks(books)

if __name__ == "__main__":
    main()



