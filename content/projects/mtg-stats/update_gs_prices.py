from use_db import *
from use_sheets import *
import pandas as pd
import math
BASEURL = 'https://www.mtgstocks.com/prints/'

if __name__ == "__main__":
    postgres_mtg = db_interface("conn_info_windows.ini")
    vc_interface = gs_interface("Vintage-Cube-Kurt-Edition")
    cube_df = vc_interface.sheets_df

    updated_df = cube_df.copy()
    problem_list = []
    for index, row in cube_df.iterrows():
        # print (index, row)
        mtg_id , mkrt_price = postgres_mtg.query_mkt_val_for_card_and_set([row['Name'] , row['Set']])
        url = BASEURL+str(mtg_id)
        
        if mkrt_price is not None:
            conv_price = float(mkrt_price)
        
        if mtg_id != None and mkrt_price != None and math.isnan(conv_price) != True:
            updated_df.loc[index,['MTGStocks Link', 'Mkt Avg']] = [url, conv_price]
        else:
            problem_list.append(row)

    vc_interface.commit_table(updated_df)
    postgres_mtg.close()