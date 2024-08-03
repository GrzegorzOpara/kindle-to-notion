import os
from modules.book import Books
from modules.file import KindleFile
from modules.notion import Notion
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('API_KEY')

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "1 per second"],
    storage_uri="memory://",
    strategy="fixed-window"
)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_key(username, password):
    return password == api_key

@app.route("/health")
def health_check():
    return jsonify({'message': 'service is healthy'}), 200

@app.route("/process_file", methods = ['POST'])
@auth.login_required
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