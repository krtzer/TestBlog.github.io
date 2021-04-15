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
    
def get_all_cards_magic(existing_ids, dead_ids, api_batch):
    randomlist = random.sample(range(1,60001), 60000)  
    # TODO when you have the list of dead IDs, remove them from this list
    blacklist = existing_ids + dead_ids

    shortlist = [x for x in randomlist if x not in blacklist]
    retrylist = []

    random_Api_calls = [BASEURL+str(i) for i  in shortlist] 


    start_time = time.time()
    for i in randomlist: 
        r = requests.get(BASEURL+str(i))
        if (r.status_code == 200):
            blob = r.json()
            
            name = blob['name']
            set_abr = blob['card_set']['abbreviation']
            rarity = blob['rarity']
            reserved_list = blob['card']['reserved']
            latest_market_price = blob['latest_price']['market']
            mtg_stocks_id = blob['id']
            
            postgres_mtg.insert_prints_data(name, set_abr, mtg_stocks_id, r.text)
            
            print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(None)) + " Added: "+" | " + name +" | " + str(set_abr) +" | " + str(latest_market_price))

        elif (r.status_code == 502) or (r.status_code == 404):
            # black list this id because it doesn't exist anymore
            print (str(r.status_code) + " on Id " + str(i))
            postgres_mtg.insert_dead_id(i)
            
        else:
            retrylist.append(i)
            print (str(r.status_code) + " on Id " + str(i))
            # log id, log status, probably retry
        
    end_time = time.time()

    print (end_time - start_time)
    print (retrylist)


if __name__ == "__main__":
    test_stocks_api(9177)
    postgres_mtg = db_interface("conn_info_pi.ini")
    get_all_cards_magic(postgres_mtg.existing_ids, postgres_mtg.dead_ids)
    postgres_mtg.close()

    