import feedparser, os, time, datetime
from src.config.logger import config_logger
from src.Utils.utils import Operations as ops
from dotenv import load_dotenv
import src.scripts.database as Db
import pandas as pd

HEAD = [['URL', 'HEADLINE', 'AUTHOR', 'DATE']]

class Verge():

    def fetchData():
        feed = feedparser.parse('https://www.theverge.com/rss/index.xml/')
        fileName = '/home/sahilr/the-Verge/Data/'+datetime.datetime.strptime(feed.entries[0].published[:-6], '%Y-%m-%dT%H:%M:%S').strftime("%d%m%y")+'.csv'
        latest_id = feed.entries[0].id
        
        if not os.path.isfile(os.path.join(os.getcwd(),fileName)): 
            pd.DataFrame(columns=HEAD).rename_axis('ID', axis=1).to_csv(fileName)


        # if file is not empty and the last URL in file not equal to latest_id
        # then make the last url of file the latest_id
        if(pd.notna(pd.read_csv(fileName)['URL'].max())):
            if (pd.read_csv(fileName)['URL'].tolist()[-1] != latest_id):
                latest_id = pd.read_csv(fileName)['URL'].tolist()[-1]

        while True:

            feed = feedparser.parse('https://www.theverge.com/rss/index.xml/')
            dcount = 0
            data = []

            if (feed.entries[0].id == latest_id and pd.notna(pd.read_csv(fileName)['URL'].max())):
                    logger.info("Looking for new Feeds...!")
                    time.sleep(300)
                    continue
            
            for i in feed.entries:
                author = i['author']
                headline = i['title']
                url = i['link']+' '
                date1 = datetime.datetime.strptime(i['published'][:-6], '%Y-%m-%dT%H:%M:%S').strftime("%d/%m/%y")
                date = datetime.datetime.strptime(date1, "%d/%m/%y").date()

                if (pd.notna(pd.read_csv(fileName)['URL'].max())):
                    if (url == latest_id):
                        latest_id = feed.entries[0].id
                        break

                Db.insertData(url, headline, author, date)
                Db.connect.commit()
                Db.mydb.commit()
        

                articleDate = '/home/sahilr/the-Verge/Data/'+date.strftime("%d%m%y")+'.csv'
                if articleDate != fileName:
                    latest_id = feed.entries[0].id
                    break
                data.append([url, headline, author, date])
                dcount+=1

            data.reverse()
            ops.get_csv(HEAD,data,fileName)

            logger.info(f'Fetched {dcount} articles')


if __name__ == '__main__':

    # loading env vars
    load_dotenv()
    logger = config_logger()

    v1 = Verge
    
    v1.fetchData()

#  filedate = 2023-04-01
# articledate = 