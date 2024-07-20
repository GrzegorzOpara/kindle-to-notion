import requests
import json
import time

class NotionAPIError(Exception):
  """
  Exception class for Notion API errors.
  """
  def __init__(self, message):
    super().__init__(message)

class Notion(object):
    """
    This class interacts with the Notion API to create and manage book pages with highlight information.

    Attributes:
        headers (dict): A dictionary containing authorization headers for Notion API requests.
        notion_db (str): The ID of the Notion database used to store book pages.

    Methods:
        create_empty_book_page(self, title: str, author: str) -> str:
            Creates a new empty book page in the Notion database with the given title (including author name).

            Args:
                title (str): The title of the book.
                author (str): The author of the book.

            Returns:
                str: The ID of the newly created Notion page.

        create_blocks_from_highlghts(self, highlights: list[Highlight]) -> list:
            Converts a list of `Highlight` objects into a list of Notion block dictionaries suitable for creating highlights blocks.

            Args:
                highlights (list[Highlight]): A list of `Highlight` objects containing highlight information.

            Returns:
                list: A list of Notion block dictionaries representing the highlights and notes.

        add_highlights_blocks_to_the_book_page(self, page_id: str, highlights: list[Highlight], delay: int = 3) -> None:
            Appends Notion blocks representing highlights and notes to a specified book page in batches with an optional delay between batches.

            Args:
                page_id (str): The ID of the Notion page representing the book.
                highlights (list[Highlight]): A list of `Highlight` objects containing highlight information.
                delay (int, optional): The number of seconds to wait between batches of Notion API requests. Defaults to 3.

            Returns:
                None
        
        process_books(self, books: Books) -> None:
            Iterates through a `Books` object, creates Notion book pages for each book, and adds highlight blocks to the corresponding pages.

            Args:
                books (Books): A `Books` object containing book data and associated highlights.

            Returns:
                None
    """
    headers = None
    notion_db = ""

    def __init__(self, notion_token, notion_db) -> None:
        self.headers = {
            "Authorization": "Bearer " + notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.notion_db = notion_db

    def make_api_request(self):
        try:
            response = requests.request(method, url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise exception for non-200 status codes
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            raise NotionAPIError(f"Error making API request: {e}")
        except json.JSONDecodeError as e:
            raise NotionAPIError(f"Error decoding JSON response: {e}")
    
    def create_empty_book_page(self, title, author) -> str:
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

    def create_blocks_from_highlghts(self, highlights):
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

    def add_highlights_blocks_to_the_book_page(self, page_id, highlights, delay=3) -> None:
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

    def process_books(self, books) -> None:
        for book in books.get_books():
            page_id = self.create_empty_book_page(book.title, book.author)
            self.add_highlights_blocks_to_the_book_page(page_id, self.create_blocks_from_highlghts(book.highlights))
            



    
