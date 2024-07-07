import requests
import json
import time

class Notion(object):

    headers = None
    notion_db = ""

    def __init__(self, notion_token, notion_db) -> None:
        self.headers = {
            "Authorization": "Bearer " + notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.notion_db = notion_db

    def createEmptyBookPage(self, title, author) -> str:
        page_id = ""
        create_url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": f"{self.notion_db}"
            },
            "properties": {
                "title": [
                    {
                        "text": {
                            "content": f"{title} - {author}"
                        }
                    }
                ]
            }
        }

        response = requests.post(create_url, headers=self.headers, json=payload)
        page_id = json.loads(response.text)['id']
        
        return page_id

    def createBlocksFromHighlghts(self, highlights):
        blocksList = []
        
        for highligth in highlights:
            if highligth.note:
                highligth.note += " - "
            
            dict = {
                "object": "block",
                "callout":  {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"{highligth.note}page {highligth.page} ({highligth.location_start} - {highligth.location_end})"
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
                                "content": highligth.highlight
                            }
                        }
                    ]
                }
            }

            blocksList.append(dict)
            
        return blocksList  

    def addHighlightsBlocksToTheBookPage(self, page_id, highlights, delay=3) -> None:
        start_index = 0
        while start_index < len(highlights):
            end_index = min(start_index + 99, len(highlights))
            
            # append notion page
            append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            payload = {
                "children": highlights[start_index:end_index]
            }
            requests.patch(append_url, headers=self.headers, json=payload)
            start_index += 99
            time.sleep(10)

    def processBooks(self, books) -> None:
        for book in books.getBooks():
            page_id = self.createEmptyBookPage(book.title, book.author)
            self.addHighlightsBlocksToTheBookPage(page_id, self.createBlocksFromHighlghts(book.highlights))
            



    
