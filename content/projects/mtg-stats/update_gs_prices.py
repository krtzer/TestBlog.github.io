from use_db import *
from use_sheets import *
from mtg_analysis import *
import pandas as pd
import math
BASEURL = 'https://www.mtgstocks.com/prints/'

def get_all_cards(sheet_df):
    cols = 'Name'
    return sheet_df[cols]

def get_unowned_cards(sheet_df):
    cols = 'Owner'
    sheet_df[cols] = sheet_df[sheet_df[cols] != 'Kurt'][cols]
    return sheet_df.dropna()

def update_gs_prices(cube_df):
    #Todo re-write this piece of code. it has terrible logic
    problem_list = []
    for index, row in cube_df.iterrows():
        # print (index, row)
        mtg_id , mkrt_price = postgres_mtg.query_mkt_val_for_card_and_set([row['Name'] , row['Set']])
        url = BASEURL+str(mtg_id)
        
        if mkrt_price is not None:
            conv_price = float(mkrt_price)
        
        if mtg_id != None and mkrt_price != None and math.isnan(conv_price) != True:
            updated_df.loc[index,['Latest Avg']] = [conv_price]
        else:
            problem_list.append(row)

    return updated_df

def process_cube(cube_df):
    unowned_df = get_unowned_cards(cube_df)
    cards = get_all_cards(unowned_df)
    problem_cards = []
    for card in cards:
        prices_df = postgres_mtg.get_avg_data(card)
        print (card)
        if prices_df != (None, None):
            results = data_formatter(card, prices_df)
            results_df = pd.DataFrame(results,columns=['CardName', 'Timespan', 'Edition', 'Current Price', 'Minimum in Epoch', 'Date of Epoch Min', \
            'Percent change Current Price from Epoch Min', 'Standard Dev'])
            results_df.to_csv('processed_cards.csv', header=False, index=False, mode='a')
            print (results_df)
        else:
            f = open("missingcards.txt", "a")
            f.write(card)
            f.close()

if __name__ == "__main__":
    postgres_mtg = db_interface("conn_info_windows.ini")
    vc_interface = gs_interface("Vintage-Cube-Kurt-Edition")
    cube_df = vc_interface.sheets_df
    updated_df = cube_df.copy()
    temp = update_gs_prices(updated_df)

    vc_interface.update_sheet(temp)

    postgres_mtg.close()