# Kindle to Notion

This Python project allows you to automatically import your Kindle highlights into your Notion workspace.

## Features

* **Parses Kindle highlight files:** Reads your Kindle highlight file and extracts the title, author, page number, highlight text, and notes.
* **Organizes highlights by book:** Groups highlights from the same book together.
* **Creates Notion pages for each book:** Creates a new Notion page for each book in your specified Notion database.
* **Adds highlights as blocks:** Adds each highlight as a Notion block with the appropriate formatting (callout for page number and highlight text, quote for the highlight itself).
* **Supports notes:** Includes notes associated with highlights in the Notion blocks.
* **Handles large files:** Processes highlights in batches to avoid exceeding Notion API rate limits.

## Installation

1. **Install Python:** If you don't have Python installed, download and install it from [https://www.python.org/](https://www.python.org/).
2. **Install required packages:**
    ``bash
    pip install -r requirements.txt
    ``
## Usage
1. Create a Notion database: Create a new database in your Notion workspace to store your book highlights. You can skip this step you you want to use an exisitng database.
2. Create Notion Intergation https://www.notion.so/profile/integrations and get your ``Notion API key`` (Internal Integration Secret)
3. Set up connection in your Notion workspace:
    https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages
4. Get your ``Notion database ID``: Copy the ID of the database you created in step 1 (https://developers.notion.com/reference/retrieve-a-database).
5. Run the app:
    ``bash
    gunicorn --bind 127.0.0.1:8080 app:app
    ``
6. Access the API endpoint:
    * Endpoint: ``/process_file``
    * Method: ``POST``
    * Form data:
      * ``notion_api_key``: Your Notion API key.
      * ``notion_db_id``: The ID of your Notion database.
      * ``file``: The Kindle highlight file you want to import.
7. View your highlights in Notion: Once the file is processed, you'll see the book pages and highlights in your Notion database.

### Example
***These are fake notion_db nor API key, don't try to use them :)***
```bash
curl -X POST \
-F "notion_api_key=secret_3732hr2f90y34h3i4ro39ru" \
-F "notion_db_id=3r9ehfw9347rf3hw9rfy34" \
-F "file=@/home/user/My Clippings.txt" \
http://127.0.0.1:8080/process_file
```

### Docker
If you prefer to use docker:
1. Build docker image
```
docker build -t kindle-to-notion .
```
2. Run docker imiage
```
docker run -p 8080:8080 kindle-to-notion:latest
```

## Notes
* The app currently supports .txt Kindle highlight files.
* You can adjust the batch size and delay between API requests in the notion.py file (*default = 3 seconds*).
* The app uses the Notion API v2022-06-28.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.