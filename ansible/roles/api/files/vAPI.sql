import sqlite3
con = sqlite3.connect('vAPI.db') # Warning: This file is created in the current directory
con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username char(100) NOT NULL, password char(100) NOT NULL)")
con.execute("CREATE TABLE tokens (id INTEGER PRIMARY KEY, token char(100) NOT NULL, userid char(100) NOT NULL)")
for i in range(1,10):
    con.execute("INSERT INTO users (username,password) VALUES (?,?)", ('user'+str(i),'pass'+str(i)))
con.commit()
