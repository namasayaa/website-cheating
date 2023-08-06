import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Namasayaari25!",
)

my_cussor = mydb.cursor()

# my_cussor.execute("CREATE DATABASE DB_cheating")

my_cussor.execute("SHOW DATABASES")
for db in my_cussor:
    print(db)