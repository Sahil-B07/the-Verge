import sys
sys.path.append('src')

import scripts.database as Db
import config.logger as logger
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c2d', nargs='+',type=str, help='store Csv To Database')
parser.add_argument('-rtd',type=str ,nargs='+' ,help='Remove Table\'s Data')

arg = parser.parse_args()

class Operations():
    
    def c2d(arg):
        Db.csvToDb(arg.c2d[0],arg.c2d[1])
        logger.info(f'{arg.c2d[0]} saved in {arg.c2d[1]} table:theVerge-DB')
    def rtd(arg):
        Db.deleteData(arg.rtd[0])
        Db.resetIds(0)

    def get_csv(head,details,fname):
        df = pd.DataFrame(details,columns=head).rename_axis('ID', axis=1)

        old_df = pd.read_csv(fname, index_col=0)
        max_index = old_df.index.max()
        try:
            df.index = range(max_index + 1, max_index + 1 + len(df))
        except:
            df.index = range(1,1 + len(df))
        df.to_csv(fname , mode='a', header=False)