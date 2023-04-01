import feedparser, os, time, datetime, logging
from src.config.logger import logger
from src.Utils.utils import Operations as ops
from dotenv import load_dotenv
import src.scripts.database as Db
import pandas as pd

HEAD = [['URL', 'HEADLINE', 'AUTHOR', 'DATE']]

class Verge():

    def fetchData():
        feed = feedparser.parse('https://www.theverge.com/rss/index.xml/')
        fileName = './Data/'+datetime.datetime.strptime(feed.entries[0].published[:-6], '%Y-%m-%dT%H:%M:%S').strftime("%d%m%y")+'.csv'
        latest_id = feed.entries[0].id
        
        if not os.path.isfile(os.path.join(os.getcwd(),fileName)): 
            pd.DataFrame(columns=HEAD).rename_axis('ID', axis=1).to_csv(fileName)

        if(pd.notna(pd.read_csv(fileName)['URL'].max())):
            if (pd.read_csv(fileName)['URL'].tolist()[-1] != latest_id):
                latest_id = pd.read_csv(fileName)['URL'].tolist()[-1]

        while True:

            feed = feedparser.parse('https://www.theverge.com/rss/index.xml/')
            dcount = 0
            data = []
            
            if(pd.notna(pd.read_csv(fileName)['URL'].max())):
                if (pd.read_csv(fileName)['URL'].tolist()[-1] != latest_id):
                    if (feed.entries[0].id == latest_id):
                        logger.info("Looking for new Feeds...!")
                        time.sleep(300)
                        continue

            if (feed.entries[0].id == latest_id and pd.notna(pd.read_csv(fileName)['URL'].max())):
                    logger.info("1.Looking for new Feeds...!")
                    time.sleep(300)
                    continue
            
            for i in feed.entries:
                author = i['author']
                headline = i['title']
                url = i['link']
                date1 = datetime.datetime.strptime(i['published'][:-6], '%Y-%m-%dT%H:%M:%S').strftime("%d/%m/%y")
                date = datetime.datetime.strptime(date1, "%d/%m/%y").date()

                if (pd.notna(pd.read_csv(fileName)['URL'].max())):
                    if (url == latest_id):
                        latest_id = feed.entries[0].id
                        break

                # Db.insertData(url, headline, author, date)
                # Db.connect.commit()
                # Db.mydb.commit()

                data.append([url, headline, author, date])
                print([url, headline, author, date])
                dcount+=1

            data.reverse()
            ops.get_csv(HEAD,data,fileName=date.strftime("%d%m%y"))
            logger.info(f'Fetched {dcount} articles')


if __name__ == '__main__':

    # loading env vars
    load_dotenv()

    v1 = Verge
    
    v1.fetchData()