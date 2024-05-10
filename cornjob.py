import schedule
import time
from functions.proxy_get import ProxyGet
from functions.proxy_check import ProxyCheck
from functions.db import ProxyDatabase
from concurrent.futures import ThreadPoolExecutor

db = ProxyDatabase()
db.create_table()

def check_proxy(proxy: str) -> None:
    try:
        check_obj = ProxyCheck()
        result = check_obj.check_http("google.com", proxy, 30)
        if result:
            ip, port = proxy.split(":")
            proxy_info = check_obj.get_proxy_info(proxy)
            db.add_proxy(
                ip=ip,
                port=port,
                protocol="http",
                ssl=result["ssl"],
                country=f"{proxy_info['flag']['emoji']}  {proxy_info['country_code']}",
                status=result["status"],
                speed="{:.2f}".format(result["speed"]),
            )
    except Exception as e: pass

def fetch_proxies() -> None:
    old_proxies = db.fetch_all_proxies()
    db.delete_proxy()
    global proxies_db
    proxy_obj = ProxyGet("http")
    new_proxies = proxy_obj.get_proxyscrape(10000, "all")
    proxies = [item["ip"] + ":" + str(item["port"]) for item in old_proxies] + new_proxies
    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(check_proxy, proxies)

def cronjob_checker() -> None:
    schedule.every(5).minutes.do(fetch_proxies)
    while True:
        schedule.run_pending()
        time.sleep(1)

cronjob_checker()
