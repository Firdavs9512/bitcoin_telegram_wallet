import sqlite3
from config import database

class User:
    def __init__(self):
        self.connect = sqlite3.connect(database)
        m = Migrate()
        m.create_users_table

    def get_user(self,name):
        c = self.connect.cursor()
        c.execute("SELECT * FROM users WHERE user_id=?", [name])
        result = c.fetchone()
        return result
    
    def create_user(self, name, private, address, c_id, network='testnet'):
        c =  self.connect.cursor()
        c.execute("insert into users (user_id, network, c_id, private, address) values (?, ?, ?, ?, ?)",[name,network,c_id,private,address])
        self.connect.commit()
        return c.lastrowid
    
class Migrate:
    def __init__(self):
        self.conn = sqlite3.connect(database)

    def create_users_table(self):
        c = self.conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, network TEXT, c_id INTEGER, private TEXT, address TEXT)"""
        )
        self.conn.commit()
        self.conn.close()

