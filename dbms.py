import sqlite3

#db creation
conn=sqlite3.connect('database.db')


#checking whether the table already exists
conn.execute('DROP TABLE IF EXISTS users')


#user table creation
conn.execute('CREATE TABLE users(UName TEXT\
             , ID INTEGER,Gender TEXT,Age INTEGER,Phone TEXT ,Email TEXT, Password TEXT) ')


#tweet table creation
conn.execute('DROP TABLE IF EXISTS tweet')

conn.execute('CREATE TABLE tweet(ID INTEGER,Tweet TEXT, Date DATE)')



conn.close()