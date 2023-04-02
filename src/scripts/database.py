from sqlalchemy import create_engine
import mysql.connector
import sqlite3

from dotenv import load_dotenv
import configparser, os
import pandas as pd

load_dotenv()

config = configparser.ConfigParser()
config.read('/home/sahilr/the-Verge/src/config/database.ini')

host = config['mysql']['host']
database_name = config['mysql']['database_name']
user = config['mysql']['user']
password = os.getenv('DB_PASSWORD')
port = config['mysql']['port']
alchemyPass = os.getenv('AL_DB_PASSWORD')

connect = sqlite3.connect('/home/sahilr/the-Verge/Data/articles.db')
mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database_name,
  port=port
)


cursor = connect.cursor()
mycursor = mydb.cursor()

engine = create_engine(f'mysql+pymysql://{user}:{alchemyPass}@{host}/{database_name}')

# creating a table
def createTable():
    cursor.execute("""create table verge(id INTEGER PRIMARY KEY AUTOINCREMENT, url varchar(1000), headline varchar(1000), author varchar(100), date date)""")
    mycursor.execute("""create table verge(id INTEGER PRIMARY KEY AUTO_INCREMENT, url varchar(1000), headline varchar(1000), author varchar(100), date date)""")


# Insert data
def insertData(url, headline, author, date):
    cursor.execute(f'''INSERT INTO verge (url,headline,author,date) VALUES(?,?,?,?)''', (url, headline, author, date))
    mycursor.execute(f'''INSERT INTO verge (url,headline,author,date) VALUES(%s,%s,%s,%s)''', (url, headline, author, date))

# drop a table
def dropTable(tname):
    cursor.execute(f'drop table {tname}')


# delete data
def deleteData(tname):
    cursor.execute(f'''DELETE FROM {tname} where id > 60''')
    mycursor.execute(f'''DELETE FROM {tname} where id > 60''')

# reset id's
def resetIds(no):
    cursor.execute("UPDATE SQLITE_SEQUENCE SET seq= ? WHERE NAME='verge'", (str(no),))
    mycursor.execute("ALTER TABLE verge AUTO_INCREMENT = %s", (no,))
        
def csvToDb(filename, db):
    articles = pd.read_csv(filename, usecols=['URL','HEADLINE','AUTHOR','DATE'])
    articles.to_sql(db, connect, if_exists='append',index=False)
    articles.to_sql(name=db, con=engine, if_exists='append',index=False)

if __name__ == '__main__':
    deleteData('verge')
    resetIds(60)


    connect.commit()
    mydb.commit()
    mydb.close()
    cursor.close()