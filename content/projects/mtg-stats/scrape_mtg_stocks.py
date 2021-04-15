import requests
import json
import urllib
import random
from use_db import db_interface
import time

BASEURL = 'https://api.mtgstocks.com/prints/'

# need to find api to get list of cards 
# 59893 is max currently
# What happens when we fail or lose a connection?

def check_if_in_db(id):
    #TODO look up if in db already. If entry exists, skip pinging 
    return 0
    
def get_all_cards_magic(existing_ids, dead_ids):
    randomlist = random.sample(range(1,60001), 60000)  
    # TODO when you have the list of dead IDs, remove them from this list
    blacklist = existing_ids + dead_ids

    shortlist = [x for x in randomlist if x not in blacklist]
    retrylist = []
    start_time = time.time()
    for i in randomlist: 
        r = requests.get(BASEURL+str(i))
        if (r.status_code == 200):
            blob = r.json()
            multiverse_id = blob['multiverse_id']
            mtg_stocks_id = blob['id']
            name = blob['name']
            latest_avg = blob['latest_price']['avg']
            set_abr = blob['card_set']['abbreviation']
            postgres_mtg.insert_prints_data(name, set_abr, mtg_stocks_id, r.text)
            
            print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(None)) + " Added: "+" | " + name +" | " + str(set_abr) +" | " + str(latest_avg))

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
    postgres_mtg = db_interface("conn_info_pi.ini")
    get_all_cards_magic(postgres_mtg.existing_ids, postgres_mtg.dead_ids)
    postgres_mtg.close()

    