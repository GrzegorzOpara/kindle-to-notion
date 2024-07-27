import os
from modules.book import Books
from modules.file import KindleFile
from modules.notion import Notion
from flask import Flask, request, jsonify, make_response
# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)

@app.route("/health")
def health_check():
    return jsonify({'message': 'service is healthy'}), 200

@app.route("/process_file", methods = ['POST'])
def kindle_to_notion():
    notion_api_key = request.form.get('notion_api_key')
    notion_db_id = request.form.get('notion_db_id')

    if 'file' not in request.files:
        return jsonify({'error': 'no file uploaded'}), 400
    
    if not notion_api_key:
        return jsonify({'error': 'no Notion API key provided'}), 400

    if not notion_db_id:
        return jsonify({'error': 'no Notion database id provided'}), 400
       
    kindleFile = KindleFile()
   
    books = Books()
    books.create_books_from_highlights(kindleFile.parse_file(request.files['file']))
    
    notion = Notion(request.form['notion_api_key'], request.form['notion_db_id'])
    notion.process_books(books)

    return jsonify({'message': 'file processed successfully'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)