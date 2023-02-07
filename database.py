import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as file:
    connection.executescript(file.read())

cur = connection.cursor()

cur.execute("insert into items (title, description) values (?, ?)", ("First task", "Description for the first task"))
cur.execute("insert into items (title, description) values (?, ?)", ("Second task", "Description for the second task"))
cur.execute("insert into items (title, description) values (?, ?)", ("Third task", "Description for the third task"))

connection.commit()
connection.close()

