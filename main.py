import feedparser, os, argparse, time, datetime, logging
from dotenv import load_dotenv
import pandas as pd
import Db

API_KEY = os.getenv('API_KEY')
SOURCE = "the-verge"
HEAD = [['URL', 'HEADLINE', 'AUTHOR', 'DATE']]


def get_csv(head,details,fname):
    df = pd.DataFrame(details,columns=head).rename_axis('ID', axis=1)

    old_df = pd.read_csv(fname, index_col=0)
    max_index = old_df.index.max()
    try:
        df.index = range(max_index + 1, max_index + 1 + len(df))
    except:
        df.index = range(1,1 + len(df))
    df.to_csv(fname , mode='a', header=False)

def fetchData():
    feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
    fileName = './Data/'+datetime.datetime.strptime(feed.entries[0].published[:-6], '%Y-%m-%dT%H:%M:%S').strftime("%d%m%y")+'.csv'
    
    if not os.path.isfile(os.path.join(os.getcwd(),fileName)): 
        pd.DataFrame(columns=HEAD).rename_axis('ID', axis=1).to_csv(fileName)

    latest_id = feed.entries[0].id
    if(pd.notna(pd.read_csv(fileName)['URL'].max())):
        if (pd.read_csv(fileName)['URL'].tolist()[-1] != latest_id):
            latest_id = pd.read_csv(fileName)['URL'].tolist()[-1]

    while True:

        feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
        
        if(pd.notna(pd.read_csv(fileName)['URL'].max())):
            if (pd.read_csv(fileName)['URL'].tolist()[-1] != latest_id):
                if (feed.entries[0].id == latest_id):
                    logging.info("Looking for new Feeds...!")
                    time.sleep(300)
                    continue

        if (feed.entries[0].id == latest_id):
                logging.info("Looking for new Feeds...!")
                time.sleep(300)
                continue
        
        dcount = 0
        data = []
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

            Db.insertData(url, headline, author, date)
            Db.connect.commit()

            data.append([url, headline, author, date])
            print([url, headline, author, date])
            dcount+=1

        data.reverse()
        get_csv(HEAD,data,fileName)
        logging.info(f'Fetched {dcount} articles')


if __name__ == '__main__':

    # loading env vars
    load_dotenv()
    logging.basicConfig(filename='verge.log', encoding='utf-8', level=logging.DEBUG, format='%(levelname)s:%(message)s,%(asctime)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c2d', nargs='+',type=str, help='store Csv To Database')
    parser.add_argument('-rtd',type=str ,nargs='+' ,help='Remove Table\'s Data')
    
    arg = parser.parse_args()
    if arg.c2d:
        Db.csvToDb(arg.c2d[0],arg.c2d[1])
        logging.info(f'{arg.c2d[0]} saved in {arg.c2d[1]} database')
    if arg.rtd:
        Db.deleteData(arg.rtd[0])
        Db.resetIds(0)
    
    Db.connect.commit()
    
    # fetchData()