from flask import Flask, render_template, request, Response
from functions.db import ProxyDatabase
from math import ceil
import json

app = Flask(__name__)
db = ProxyDatabase()

PER_PAGE = 100

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    start_index = (page - 1) * PER_PAGE
    end_index = start_index + PER_PAGE
    proxies = db.fetch_all_proxies()[start_index:end_index]
    total_proxies = db.len_proxies()
    total_pages = ceil(total_proxies / PER_PAGE)
    has_next_page = page < total_pages
    return render_template("index.html", proxies=proxies, page=page, has_next_page=has_next_page)

@app.route('/download')
def download_proxies():
    format = request.args.get('format')
    proxies = db.fetch_all_proxies()
    if format == 'text':
        proxies_text = "\n".join([f'{proxy["ip"]}:{proxy["port"]}' for proxy in proxies])
        return Response(proxies_text, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=proxies.txt"})
    elif format == 'json':
        proxy_list = [{"ip": proxy["ip"], "port": proxy["port"], "protocol": proxy["protocol"], "ssl": proxy["ssl"],
                       "country": proxy["country"], "status": proxy["status"], "speed": proxy["speed"]} for proxy in proxies]
        return Response(json.dumps(proxy_list), mimetype='application/json', headers={"Content-Disposition": "attachment; filename=proxies.json"})
    return "Invalid format", 400

@app.route('/docs')
def docs():
    return render_template("docs.html")

if __name__ == "__main__":
    app.run(port=1020)
