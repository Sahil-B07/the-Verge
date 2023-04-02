import sys
sys.path.append('/home/sahilr/the-Verge/src')

import scripts.database as Db
import config.logger as logger
import pandas as pd

class Operations():
    
    def get_csv(head,details,fname):
        df = pd.DataFrame(details,columns=head).rename_axis('ID', axis=1)

        old_df = pd.read_csv(fname, index_col=0)
        max_index = old_df.index.max()
        try:
            df.index = range(max_index + 1, max_index + 1 + len(df))
        except:
            df.index = range(1,1 + len(df))
        df.to_csv(fname , mode='a', header=False)