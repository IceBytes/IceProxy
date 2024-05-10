from flask import Flask, render_template, request
from functions.db import ProxyDatabase
from math import ceil

app = Flask(__name__)
db = ProxyDatabase()

@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 100
    total_proxies = db.len_proxies()
    total_pages = ceil(total_proxies / per_page)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    proxies = db.fetch_all_proxies()[start_index:end_index]

    has_next_page = page < total_pages

    return render_template("index.html", proxies=proxies, page=page, has_next_page=has_next_page)

@app.route('/docs', methods=['GET'])
def docs():
    return render_template("docs.html")

if __name__ == "__main__":
    app.run(port=1020)
