import requests
import json
import urllib
import random
from use_db import db_interface
import time
import pandas as pd
from itertools import zip_longest

BASEURL = 'https://api.mtgstocks.com/'

# need to find api to get list of cards 
# 59893 is max currently
# What happens when we fail or lose a connection?

def test_stocks_api(id):
    r = requests.get(BASEURL+str(id))   
    return 0

def grouper(iterable, n, fillvalue = None):
	args = [iter(iterable)]*n
	return zip_longest(*args, fillvalue=fillvalue)

def update_all_cards():
    return True

def get_all_cards_magic(existing_ids, dead_ids, chunk_size):
    randomlist = random.sample(range(1,65001), 65000)  
    # TODO when you have the list of dead IDs, remove them from this list
    blacklist = existing_ids + dead_ids

    shortlist = [x for x in randomlist if x not in blacklist]
    retrylist = []
    retrylimit = 5

    prints_columns = postgres_mtg.get_columns('prints')
    prices_avg_columns = postgres_mtg.get_columns('prices_averages')
    prices_mkt_columns = postgres_mtg.get_columns('prices_market')
    # random_Api_calls = [BASEURL+str(i) for i  in shortlist] 
    random_Api_calls = [str(i) for i  in shortlist] 

    chunked_Api_Calls = grouper(random_Api_calls, chunk_size)

    for chunk in chunked_Api_Calls: 
        start_time = time.time()
        prints_chunk = []
        prices_mkt_chunk = []
        prices_avg_chunk = []
        for api_call in chunk:
            if api_call is not None:
                retry = 0
                success = False
                while (retry < retrylimit and not success):
                    try:
                        r_prints = requests.get(BASEURL + "prints/" + str(api_call))
                        r_prices = requests.get(BASEURL + "prints/" + str(api_call) + "/prices/")
                        success = True
                    except Exception as error:
                        print (error)
                        retry+=1
                        time.sleep(2)

                if (r_prints.status_code == 200 and r_prices.status_code == 200):
                    # Main card info Page

                    blob = r_prints.json()
                    
                    name = blob['name']
                    set_abr = blob['card_set']['abbreviation']
                    rarity = blob['rarity']
                    reserved_list = blob['card']['reserved']
                    latest_market_price = blob['latest_price']['market']
                    date = blob['latest_price']['date']
                    mtg_stocks_id = blob['id']
                    
                    r_prices_avg = r_prices.json()['avg']
                    r_prices_mkt = r_prices.json()['market']

                    prints_chunk.append([name, set_abr, rarity, reserved_list, latest_market_price, date, mtg_stocks_id])
                    mtk_to_append = [[mtg_stocks_id] + x for x in r_prices_mkt]
                    avg_to_append = [[mtg_stocks_id] + x for x in r_prices_avg]
                    prices_mkt_chunk += mtk_to_append
                    prices_avg_chunk += avg_to_append

                    # print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(None)) + " Added: "+" | " + name +" | " + str(set_abr) +" | " + str(latest_market_price))

                elif (r_prints.status_code == 502) or (r_prints.status_code == 404):
                    # black list this id because it doesn't exist anymore
                    print (str(r_prints.status_code) + " on Id " + str(api_call))
                    postgres_mtg.insert_dead_id(int(api_call))
                    
                else:
                    retrylist.append(api_call)
                    print (str(r_prints.status_code) + " on Id " + str(api_call))
                    # log id, log status, probably retry

            end_time = time.time()

        # build data frame, push chunk to db
        # Prices is auto indexing, so we skip the first column
        db_df = pd.DataFrame(data=prints_chunk, columns=prints_columns[1:])
        mkt_df = pd.DataFrame(data=prices_mkt_chunk, columns=prices_mkt_columns[1:])
        avg_df = pd.DataFrame(data=prices_avg_chunk, columns=prices_avg_columns[1:])
        postgres_mtg.insert_data_new_prints(db_df, chunk_size)
        postgres_mtg.insert_into_prices_mkt(mkt_df, chunk_size)
        postgres_mtg.insert_into_prices_avg(avg_df, chunk_size)
        
        print (end_time - start_time)
        print (retrylist)

def update_all_cards_with_latest_prices(existing_ids, chunk_size):
    
    # TODO when you have the list of dead IDs, remove them from this list
    retrylist = []
    retrylimit = 5

    prices_avg_columns = postgres_mtg.get_columns('prices_averages')
    prices_mkt_columns = postgres_mtg.get_columns('prices_market')
    # random_Api_calls = [BASEURL+str(i) for i  in shortlist] 
    random_Api_calls = [str(i) for i  in existing_ids] 

    chunked_Api_Calls = grouper(random_Api_calls, chunk_size)

    for chunk in chunked_Api_Calls: 
        start_time = time.time()
        prints_chunk = []
        prices_mkt_chunk = []
        prices_avg_chunk = []
        for api_call in chunk:
            if api_call is not None:
                retry = 0
                success = False
                while (retry < retrylimit and not success):
                    try:
                        r_prints = requests.get(BASEURL + "prints/" + str(api_call))
                        success = True
                    except Exception as error:
                        print (error)
                        retry+=1
                        time.sleep(2)

                if (r_prints.status_code == 200):
                    # Main card info Page

                    blob = r_prints.json()
                    latest_avg_price = blob['latest_price']['avg']
                    latest_market_price = blob['latest_price']['market']
                    date = blob['latest_price']['date']
                    mtg_stocks_id = blob['id']
                    
                    prices_mkt_chunk.append([mtg_stocks_id, date, latest_market_price])
                    prices_avg_chunk.append([mtg_stocks_id, date, latest_avg_price])

                    # print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(None)) + " Added: "+" | " + name +" | " + str(set_abr) +" | " + str(latest_market_price))

                elif (r_prints.status_code == 502) or (r_prints.status_code == 404):
                    # black list this id because it doesn't exist anymore
                    print (str(r_prints.status_code) + " on Id " + str(api_call))
                    postgres_mtg.insert_dead_id(int(api_call))
                    
                else:
                    retrylist.append(api_call)
                    print (str(r_prints.status_code) + " on Id " + str(api_call))
                    # log id, log status, probably retry

            end_time = time.time()

        # build data frame, push chunk to db
        # Prices is auto indexing, so we skip the first column
        mkt_df = pd.DataFrame(data=prices_mkt_chunk, columns=prices_mkt_columns[1:])
        avg_df = pd.DataFrame(data=prices_avg_chunk, columns=prices_avg_columns[1:])
        postgres_mtg.insert_into_prices_mkt(mkt_df, chunk_size)
        postgres_mtg.update_latest_mkt_price(mkt_df, chunk_size)
        postgres_mtg.insert_into_prices_avg(avg_df, chunk_size)
        
        print (end_time - start_time)
        # print (retrylist)

    print ('List of missing IDs to retry: ' +str(retrylist))
    return True

if __name__ == "__main__":
    test_stocks_api(9177)
    postgres_mtg = db_interface("conn_info_windows.ini")
    update_all_cards_with_latest_prices(postgres_mtg.existing_ids, 1000)
    # get_all_cards_magic(postgres_mtg.existing_ids, postgres_mtg.dead_ids, 10)

    postgres_mtg.close()

    