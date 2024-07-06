import re
import os
import json
import requests
import time


class Highlight(object):

    def __init__(self, title, author, page, location_start, location_end, date_added, text):
        self.title = title
        self.author = author
        self.page = page
        self.location_start = location_start
        self.location_end = location_end
        self.added_date = date_added
        self.highlight = text
        self.note = ""
    
    def __str__(self):
        return f"{self.title} ({self.author})\npage: {self.page} ({self.location_start} - {self.location_end}), added: {self.added_date}\ntext: {self.highlight}note: {self.note}\n" 
    
    def genListOfNotionBlocks(self):
        blocksList = []
        if self.note:
            self.note += " - "
        dict = {
            "object": "block",
            "callout":  {
                "rich_text": [
                    {
                        "text": {
                            "content": f"{self.note}page {self.page} ({self.location_start} - {self.location_end})"
                        }
                    }
                ], 
                "icon":{
                    "type":"external",
                    "external":{
                        "url":"https://www.notion.so/icons/compose_green.svg"
                    }
                },
                "color": "gray_background"               
            }
        }
        blocksList.append(dict)

        dict = {
            "object": "block",
            "quote": {
                "rich_text": [
                    {
                        "text": {
                            "content": self.highlight
                        }
                    }
                ]
            }
        }

        blocksList.append(dict)
            
        return blocksList      
    
class Book(object):
    def __init__(self, title, author, highlights=[]):
        self.title = title
        self.author = author
        self.highlights = highlights

    def addHighlight(self, highlights):
        self.highlights += highlights
        pass

    def genNotionEmptyPage(self, notion_db_id):
        dict = {
            "parent": {
                "type": "database_id",
                "database_id": f"{notion_db_id}"
            },
            "properties": {
                "title": [
                    {
                        "text": {
                            "content": f"{self.title} - {self.author}"
                        }
                    }
                ]
            }
        }

        return dict

def parseFile(filename):
    """
        param: file
        return: lists of highlights with notes, sorted by book, start_loacation
    """
    with open(filename, encoding="utf-8-sig") as file:
        content = file.readlines()
        highlights = []
        note = None
        is_highlight = is_bookmark = False
        text = ""
        for line in content:            
            if line.strip():
                # Title and Author
                if re.search(r"^(.*?)\s*\(([^)]+)\)$", line):
                    match = re.search(r"^(.*?)\s*\(([^)]+)\)$", line)
                    title = match.group(1)
                    author = match.group(2)

                # Highlight
                elif re.search(r"^- Your Highlight on page (\d+) \| location (\d+)-(\d+) \| Added on (.+)$", line):
                    is_highlight = True # highlight
                    match = re.search(r"^- Your Highlight on page (\d+) \| location (\d+)-(\d+) \| Added on (.+)$", line)
                    page, location_start, location_end, date_added = match.groups()

                # Note
                elif re.search(r"^- Your Note on page (\d+) \| location (\d+) \| Added on (.+)$", line):
                    match = re.search(r"^- Your Note on page (\d+) \| location (\d+) \| Added on (.+)$", line)
                    location = match.group(2)

                # Bookmark
                elif re.search(r"^- Your Bookmark on page (\d+) \| location (\d+) \| Added on (.+)$", line):
                    is_bookmark = True

                # Entry end
                elif line == "==========\n":
                    if is_highlight:
                        highlight = Highlight(title, author, page, location_start, location_end, date_added, text.strip())
                        if note and note[0] == title and note[1] == author and note[2] >= location_start and note[2] <= location_end:
                            highlight.note = note[3]
                            note = None
                        highlights.append(highlight)
                        is_highlight = False
                    elif is_bookmark:
                        is_bookmark = False
                    else: 
                        note = (title, author, location, text.strip())
                    text = ""
                else:
                    text += line

        # sort highlights by title, location_start
        highlights_sorted = sorted(highlights, key = lambda x: (x.title, x.location_start))

    return highlights_sorted

def createBooks(highlights):
    """
        param: highlights
        return: list of Books
    """
    books = []
    
    for highlight in highlights:
        found = False
        
        for book in books:
            if highlight.title.strip() == book.title:
                found = True
                book.addHighlight(highlight.genListOfNotionBlocks())
                break

        if not found:
            books.append(Book(highlight.title.strip(), highlight.author.strip(), highlight.genListOfNotionBlocks()))
                           
    return books

def main():
    
    create_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer " + os.environ["NOTION_TOKEN"],
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    highlights = parseFile("My Clippings.txt")
    books = createBooks(highlights)

    for book in books:
        
        # Create an empty page for book
        payload = book.genNotionEmptyPage(os.environ["NOTION_DB"])      
        response = requests.post(create_url, headers=headers, json=payload)
        page_id = json.loads(response.text)['id']
       
        highlights = book.highlights
        start_index = 0
        while start_index < len(highlights):
            end_index = min(start_index + 99, len(highlights))
            
            # append notion page
            append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            payload = {
                "children": highlights[start_index:end_index]
            }
            requests.patch(append_url, headers=headers, json=payload)
            start_index += 99
            time.sleep(10)

if __name__ == "__main__":
    main()



