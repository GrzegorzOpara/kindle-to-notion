<p align="center">
  <i>Do you like my work? Buy me a coffee!</i><BR>
  <a href="https://www.buymeacoffee.com/grzegorz.opara" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
  <BR><BR>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Amazon_Kindle_logo.svg/388px-Amazon_Kindle_logo.svg.png">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Plus_symbol.svg/200px-Plus_symbol.svg.png" width="100" height="100">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Notion-logo.svg/240px-Notion-logo.svg.png" width="100" height="100">
</p>



# Kindle to Notion

[![kindle-to-notion](https://github.com/GrzegorzOpara/kindle-to-notion/actions/workflows/kindle-to-notion-workflow.yml/badge.svg)](https://github.com/GrzegorzOpara/kindle-to-notion/actions/workflows/kindle-to-notion-workflow.yml)

This Python back-end application allows you to automatically import your Kindle highlights into your Notion workspace.

## Features

* **Parses Kindle highlight files:** Reads your Kindle highlight file and extracts the title, author, page number, highlight text, and notes.
* **Organizes highlights by book:** Groups highlights from the same book together.
* **Creates Notion pages for each book:** Creates a new Notion page for each book in your specified Notion database.
* **Adds highlights as blocks:** Adds each highlight as a Notion block with the appropriate formatting (callout for page number and highlight text, quote for the highlight itself).
* **Supports notes:** Includes notes associated with highlights in the Notion blocks.
* **Security** Support basic auth (using API key) and rate limiting
* **Handles large files:** Processes highlights in batches to avoid exceeding Notion API rate limits.

## Installation
> If you prefer to use docker go to: [Docker section](#Docker)

1. **Install Python:** If you don't have Python installed, download and install it from [https://www.python.org/](https://www.python.org/).
2. **Install required packages:**
    ``bash
    pip install -r requirements.txt
    ``
## Usage
1. Create a new database in your Notion workspace to store your book highlights. You can skip this step you you want to use an exisitng database.
2. Create Notion Intergation https://www.notion.so/profile/integrations and get your ``Notion API key`` (aka. *Internal Integration Secret*)
3. Set up connection in your Notion workspace:
    https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages
4. Get your ``Notion database ID``: Copy the ID of the database (https://developers.notion.com/reference/retrieve-a-database).
5. Create API key and store it in .env file, for instance
``API_KEY=3089657c-30fc-4fa6-86e1-f9fd38c03264``
6. Encode API Key to use it to call the process_file endpoint, you can use this site https://www.base64encode.org/

   **when encodig please put : (a colon) as a first chracter followed by the API KEY**

   for instance: ``:3089657c-30fc-4fa6-86e1-f9fd38c03264``

   that should result in encoded: ``OjMwODk2NTdjLTMwZmMtNGZhNi04NmUxLWY5ZmQzOGMwMzI2NA==``

   **Do not share the API key!**

7. Run the app:
    ```bash
    gunicorn --bind 127.0.0.1:8080 app:app
    ```

8. Access the API endpoint:
    * Endpoint: ``/process_file``
    * Method: ``POST``
    * Form data:
      * ``notion_api_key``: Your Notion API key.
      * ``notion_db_id``: The ID of your Notion database.
      * ``file``: The Kindle highlight file you want to import.
    * Example:
        
        ***These are fake notion_db, notion api key and encoded api key, don't try to use them :)***
        ```bash
        curl -X POST \
        -H "Authorization: Basic OjMwODk2NTdjLTMwZmMtNGZhNi04NmUxLWY5ZmQzOGMwMzI2NA=="
        -F "notion_api_key=secret_3732hr2f90y34h3i4ro39ru" \
        -F "notion_db_id=3r9ehfw9347rf3hw9rfy34" \
        -F "file=@/home/user/My Clippings.txt" \
        http://127.0.0.1:8080/process_file
9. View your highlights in Notion: Once the file is processed, you'll see the book pages and highlights in your Notion database.

### Docker
If you prefer to use docker
1. Build docker image ```bash docker build --build-arg API_KEY==$API_KEY -t kindle-to-notion . ```
2. Run docker imiage ```bash docker run --env-file=.env -p 8080:8080 kindle-to-notion:latest ```

## Notes
* The app currently supports .txt Kindle highlight files.
* You can adjust the batch size and delay between API requests in the notion.py file (*default = 3 seconds*).
* The app uses the Notion API v2022-06-28.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.