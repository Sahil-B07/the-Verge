import feedparser, os, time, datetime, logging
from dotenv import load_dotenv
import pandas as pd
import myDb

fileName = './Data/'+datetime.datetime.now().strftime("%d%m%y")+'.csv'
# loading env vars
load_dotenv()

API_KEY = os.getenv('API_KEY')
SOURCE = "the-verge"
HEAD = [['URL', 'HEADLINE', 'AUTHOR', 'DATE']]

def get_csv(head,details,fname):
    df = pd.DataFrame(details,columns=head).rename_axis('ID', axis=1)
    if not os.path.isfile(os.path.join(os.getcwd(),fname)):      
        df.to_csv(fileName,index=True,header=True)
    else:
        old_df = pd.read_csv(fileName, index_col=0)
        max_index = old_df.index.max()
        try:
            df.index = range(max_index + 1, max_index + 1 + len(df))
        except:
            df.index = range(1,1 + len(df))
        df.to_csv(fileName , mode='a', header=False)

def fetchData():
    feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
    latest_id = feed.entries[0].id

    while True:

        data = []
        feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
        
        if (feed.entries[0].id == latest_id):
            print("Looking for new Feeds...!")
            time.sleep(300)
            continue

        for i in feed.entries:
            author = i['author']
            headline = i['title']
            url = i['link']
            date = datetime.datetime.strptime(i['published'][:-6], '%Y-%m-%dT%H:%M:%S').strftime("%d/%m/%y")
            
            if (url == latest_id):
                latest_id = feed.entries[0].id
                break

            myDb.insertData(url, headline, author, date)
            myDb.connect.commit()

            data.append([url, headline, author, date])
            print([url, headline, author, date])

        get_csv(HEAD,data,fileName)


if __name__ == '__main__':
        
    # myDb.deleteData('verge')
    # myDb.resetIds(0)
    fetchData()