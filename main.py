from functions.db import ProxyDatabase
from flask import Flask, render_template

app = Flask(__name__)
db = ProxyDatabase()

@app.route('/', methods=['GET'])
def index():
    proxies = db.fetch_all_proxies()
    return render_template("index.html", proxies=proxies)

@app.route('/docs', methods=['GET'])
def docs():
    return render_template("docs.html")

if __name__ == "__main__":
    app.run(port=1020)
