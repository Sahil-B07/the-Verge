import sqlite3
import pandas as pd

connect = sqlite3.connect('articles.db')
cursor = connect.cursor()
# creating a table
def createTable():
    cursor.execute("""create table verge(id INTEGER PRIMARY KEY AUTOINCREMENT, url varchar(1000), headline varchar(1000), author varchar(100), date date)""")


# Insert data
def insertData(url, headline, author, date):
    cursor.execute(f'''INSERT INTO verge (url,headline,author,date) VALUES(?,?,?,?)''', (url, headline, author, date))


# drop a table
def dropTable(tname):
    cursor.execute(f'drop table {tname}')


# delete data
def deleteData(tname):
    cursor.execute(f'''DELETE FROM {tname}''')

# reset id's
def resetIds(no):
    cursor.execute("UPDATE SQLITE_SEQUENCE SET seq= ? WHERE NAME='verge'", (str(no)))
        
def csvToDb(filename, db):
    articles = pd.read_csv(filename, usecols=['URL','HEADLINE','AUTHOR','DATE'])
    articles.to_sql(db, connect, if_exists='append',index=False)

if __name__ == '__main__':
    deleteData('verge')
    # resetIds(0)
    # csvToDb('Data/270323.csv')
    connect.commit()
    cursor.close()