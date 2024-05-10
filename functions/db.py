import sqlite3
from typing import Dict, Optional, List, Any
import logging

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyDatabase:
    def __init__(self, db_name: Optional[str] = 'proxies.db') -> None:
        """
        Configure proxies database.

        Args:
            db_name: (Optional) Database filename.

        """
        self.db_name = db_name

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            logging.error(f"Error closing the database connection: {e}")
            raise e

    def create_table(self) -> bool:
        """
        Create proxies table.

        Return:
            bool
        
        """
        try:
            with self:
                self.cur.execute('''CREATE TABLE IF NOT EXISTS proxies (
                                    id INTEGER PRIMARY KEY,
                                    ip TEXT,
                                    port INTEGER,
                                    protocol TEXT,
                                    ssl INTEGER,
                                    country TEXT,
                                    status INTEGER,
                                    speed INTEGER)''')
            return True
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
            return False

    def add_proxy(self, ip: str, port: int, protocol: str, ssl: bool, country: str, status: bool, speed: int) -> bool:
        """
        Add a proxy to proxies db.

        Args:
            ip: Proxy ip address.
            port: Proxy port.
            protocol: proxy protocol (http, https).
            ssl: proxy ssl.
            country: Proxy country.
            status: Proxy status.
            speed: Proxy speed.

        Returns:
            Bool
        """
        try:
            with self:
                self.cur.execute('''INSERT INTO proxies (ip, port, protocol, ssl, country, status, speed)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (ip, port, protocol, int(ssl), country, int(status), speed))
                return True
        except sqlite3.Error as e:
            logging.error(f"Error adding proxy: {e}")
            return False

    def delete_proxy(self) -> bool:
        """
        Delete proxies from db.

        Returns:
            Bool
        """
        try:
            with self:
                self.cur.execute('''DELETE FROM proxies''')
                return True
        except sqlite3.Error as e:
            logging.error(f"Error deleting proxies: {e}")
            return False

    def fetch_all_proxies(self) -> List[Dict[str, Any]]:
        """
        Fetch all proxies from db.

        Returns:
            A list containing dictionaries representing each proxy.
        """
        try:
            with self:
                self.cur.execute('''SELECT * FROM proxies''')
                columns = [col[0] for col in self.cur.description]
                proxies = [dict(zip(columns, row)) for row in self.cur.fetchall()]
                return proxies
        except sqlite3.Error as e:
            logging.error(f"Error fetching proxies: {e}")
            return []
        
    def len_proxies(self) -> int:
        try:
            with self:
                self.cur.execute('''SELECT COUNT(*) FROM proxies''')
                count = self.cur.fetchone()
                return count[0]
        except sqlite3.Error as e:
            logging.error(f"Error counting proxies: {e}")
            return 0
        