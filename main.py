import os
from modules.book import Books
from modules.file import KindleFile
from modules.notion import Notion
    
def main():

    kindleFile = KindleFile("My Clippings.txt")
    
    books = Books()
    books.create_books_from_highlights(kindleFile.parse_file())
    
    notion = Notion(os.environ["NOTION_TOKEN"], os.environ["NOTION_DB"])
    notion.process_books(books)

if __name__ == "__main__":
    main()



