from use_db import *
from use_sheets import *
import pandas as pd
import math
import time

TODAY_UNIX_TIME = time.time() * 1000
ONE_MONTH = TODAY_UNIX_TIME - (1000 * 60 * 60 * 24 * 30)
THREE_MONTHS = TODAY_UNIX_TIME - (1000 * 60 * 60 * 24 * 90)
ONE_YEAR = TODAY_UNIX_TIME - (1000 * 60 * 60 * 24 * 365)
TWO_YEARS = TODAY_UNIX_TIME - (1000 * 60 * 60 * 24 * 365 *2)
ALL_TIME = 0

time_dict = {'ONE_MONTH':ONE_MONTH,'THREE_MONTHS':THREE_MONTHS,'ONE_YEAR':ONE_YEAR,'TWO_YEARS':TWO_YEARS,'ALL_TIME':ALL_TIME}

def readable_date(timestamp):
    timestamp = timestamp/1000
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def data_formatter(dataframes):
    formatted_list = []

    for price_df in dataframes:
        if not price_df.empty:
            
            # price_df.sort_values(by='timestamp')
            # Current info 
            mtg_set = price_df['mtg_set'].values[0]
            most_recent_price_index = price_df['timestamp'].idxmax()
            most_recent_price = price_df['avg'][most_recent_price_index]
            
            cols = ['timestamp']
            for time in time_dict:
                # Alternative to copying is to order the timespans list by greatest to lowest, that way, the same DF is used, but is reduced each time
                # I decided to go with the more general solution where order doesn't matter
                filtered_df = price_df.copy()
                filtered_df[cols] = filtered_df[price_df[cols] > time_dict[time]][cols]
                time_df = filtered_df.dropna()
                if not time_df.empty:
                    min_time_span = time_df['avg'].min()
                    money_min_index = time_df['avg'].idxmin()
                    price_std = time_df['avg'].std()
                    min_date = readable_date(time_df['timestamp'][money_min_index])
                    percent_change = 100*((most_recent_price - min_time_span)/min_time_span)
                    price_list = [time, mtg_set, most_recent_price, min_time_span, min_date, round(percent_change, 2), round(price_std, 3)]
                    formatted_list.append(price_list)
                    # print (price_list)

            # one_year_df = price_df[price_df[cols] > ONE_YEAR].dropna()
            
            #formatted_list.append([mtg_set, most_recent_price, \
            #percent_change_all_time, money_min_all_time, min_date_all_time,all_time_std]) #, \
            #percent_change_one_month, one_month_min, one_month_min_date, one_month_std, \
            #percent_change_three_month, three_month_min, three_month_min_date, three_month_std, \
            #percent_change_one_year, one_year_min, one_year_min_date, one_year_std, \
            #])
            
    return formatted_list

if __name__ == "__main__":
    cards = ['Mirari\'s Wake', 'Jace, the Mind Sculptor', 'Rofellos, Llanowar Emissary']
    conn_info = load_connection_info("conn_info_windows.ini")
    postgres_mtg = db_interface("conn_info_windows.ini")
    for card in cards:
        prices_df = postgres_mtg.get_avg_data(card)
        print (card)
        results = data_formatter(prices_df)
        for result in results:
            print(result)

    postgres_mtg.close()
