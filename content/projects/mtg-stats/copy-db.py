import requests
import json
import urllib

baseurl = 'https://api.mtgstocks.com/prints/'

# need to find api to get list of cards 
# 59893 is max currently

for i in range (1, 59893):
    r = requests.get(baseurl+str(i))
    if (r.status_code != 502):
        blob = r.json()
        multiverse_id = blob['multiverse_id']
        name = blob['name']
        latest_avg = blob['latest_price']['avg']
        set_abr = blob['card_set']['abbreviation']
        print (r.text)

