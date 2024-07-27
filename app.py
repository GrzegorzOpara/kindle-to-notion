import os
from modules.book import Books
from modules.file import KindleFile
from modules.notion import Notion
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/health")
def hello_world():
    return "<p>Service is healthy!</p>"

@app.route("/process_file", methods = ['POST'])
def kindle_to_notion():

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    kindleFile = KindleFile()
   
    books = Books()
    books.create_books_from_highlights(kindleFile.parse_file(request.files['file']))
    
    notion = Notion(os.environ["NOTION_TOKEN"], os.environ["NOTION_DB"])
    notion.process_books(books)

    return "<p>File processed.</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, load_dotenv=True)