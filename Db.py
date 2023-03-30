import sqlite3
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

connect = sqlite3.connect('articles.db')
cursor = connect.cursor()

mydb = mysql.connector.connect(
  host="165.22.216.82",
  user="resahil",
  password="Object@23",
  database="theVerge",
  port='3306'
)
mycursor = mydb.cursor()

engine = create_engine('mysql+pymysql://root:Object@23@165.22.216.82:3306/theVerge')

# creating a table
def createTable():
    # cursor.execute("""create table verge(id INTEGER PRIMARY KEY AUTOINCREMENT, url varchar(1000), headline varchar(1000), author varchar(100), date date)""")
    mycursor.execute("""create table verge(id INTEGER PRIMARY KEY AUTO_INCREMENT, url varchar(1000), headline varchar(1000), author varchar(100), date date)""")


# Insert data
def insertData(url, headline, author, date):
    # cursor.execute(f'''INSERT INTO verge (url,headline,author,date) VALUES(?,?,?,?)''', (url, headline, author, date))
    mycursor.execute(f'''INSERT INTO verge (url,headline,author,date) VALUES(%s,%s,%s,%s)''', (url, headline, author, date))

# drop a table
def dropTable(tname):
    cursor.execute(f'drop table {tname}')


# delete data
def deleteData(tname):
    cursor.execute(f'''DELETE FROM {tname}''')
    mycursor.execute(f'''DELETE FROM {tname}''')

# reset id's
def resetIds(no):
    cursor.execute("UPDATE SQLITE_SEQUENCE SET seq= ? WHERE NAME='verge'", (str(no)))
    mycursor.execute("ALTER TABLE verge AUTO_INCREMENT = %s", (no,))
        
def csvToDb(filename, db):
    articles = pd.read_csv(filename, usecols=['URL','HEADLINE','AUTHOR','DATE'])
    # articles.to_sql(db, connect, if_exists='append',index=False)
    articles.to_sql(name=db, con=engine, if_exists='append',index=False)

if __name__ == '__main__':
    # deleteData('verge')
    # resetIds(0)

    createTable()
    # insertData('hhtp://google.com', 'This is a demo healdine', 'Mr. Kumar', '23-05-2002')
    # connect.commit()
    mydb.commit()
    mydb.close()
    cursor.close()