import requests
import json
import urllib
import random
from use_db import db_interface
import time
import pandas as pd
from itertools import zip_longest

BASEURL = 'https://api.mtgstocks.com/prints/'

# need to find api to get list of cards 
# 59893 is max currently
# What happens when we fail or lose a connection?

def test_stocks_api(id):
    r = requests.get(BASEURL+str(id))   
    return 0

def grouper(iterable, n, fillvalue = None):
	args = [iter(iterable)]*n
	return zip_longest(*args, fillvalue=fillvalue)

def get_all_cards_magic(existing_ids, dead_ids, chunk_size):
    randomlist = random.sample(range(1,60001), 60000)  
    # TODO when you have the list of dead IDs, remove them from this list
    blacklist = existing_ids + dead_ids

    shortlist = [x for x in randomlist if x not in blacklist]
    retrylist = []

    prints_columns = postgres_mtg.get_columns('prints')

    # random_Api_calls = [BASEURL+str(i) for i  in shortlist] 
    random_Api_calls = [BASEURL+str(i) for i  in shortlist] 

    chunked_Api_Calls = grouper(random_Api_calls, chunk_size)

    for chunk in chunked_Api_Calls: 
        start_time = time.time()
        prints_chunk = []
        for api_call in chunk:
            if api_call is not None:
                r = requests.get(api_call)
                if (r.status_code == 200):
                    blob = r.json()
                    
                    name = blob['name']
                    set_abr = blob['card_set']['abbreviation']
                    rarity = blob['rarity']
                    reserved_list = blob['card']['reserved']
                    latest_market_price = blob['latest_price']['market']
                    date = blob['latest_price']['date']
                    mtg_stocks_id = blob['id']
                    json_resp = r.text
                    
                    prints_chunk.append([name, set_abr, rarity, reserved_list, latest_market_price, date, mtg_stocks_id, json_resp])

                    # postgres_mtg.insert_prints_data(name, set_abr, mtg_stocks_id, r.text)
                    
                    # print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(None)) + " Added: "+" | " + name +" | " + str(set_abr) +" | " + str(latest_market_price))

                elif (r.status_code == 502) or (r.status_code == 404):
                    # black list this id because it doesn't exist anymore
                    print (str(r.status_code) + " on Id " + str(api_call))
                    postgres_mtg.insert_dead_id(int(api_call.split(BASEURL)[1]))
                    
                else:
                    retrylist.append(api_call)
                    print (str(r.status_code) + " on Id " + str(api_call))
                    # log id, log status, probably retry

            end_time = time.time()

        # build data frame, push chunk to db
        # Prices is auto indexing, so we skip the first column
        db_df = pd.DataFrame(data=prints_chunk, columns=prints_columns[1:])
        postgres_mtg.insert_data_new_prints(db_df, chunk_size)
        print (end_time - start_time)
        print (retrylist)


if __name__ == "__main__":
    test_stocks_api(9177)
    postgres_mtg = db_interface("conn_info_windows.ini")
    get_all_cards_magic(postgres_mtg.existing_ids, postgres_mtg.dead_ids, 1000)
    postgres_mtg.close()

    