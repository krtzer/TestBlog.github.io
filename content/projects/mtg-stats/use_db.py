from configparser import ConfigParser
import psycopg2
import psycopg2.extras as psql_extras
from create_db import * 
import pandas as pd

# https://stackoverflow.com/questions/41272454/python-custom-module-name-not-defined/55361835#55361835
# https://www.csee.umbc.edu/courses/331/fall10/notes/python/python3.ppt.pdf 
# https://stackoverflow.com/questions/26703476/how-to-perform-update-operations-on-columns-of-type-jsonb-in-postgres-9-4 

class db_interface:

    def __init__(self, conn_file):
        self.conn_info = load_connection_info(conn_file)
        self.connection = psycopg2.connect(**self.conn_info)
        self.cursor = self.connection.cursor()
        self.existing_ids = self.get_mtg_stock_indices()
        self.dead_ids = self.get_dead_ids()

    def close(self):
        # Close all connections to the database
        self.connection.close()
        self.cursor.close()

    def insert_dead_id(self, mtgstocks_id: int) -> None:
        dead_id_query = "INSERT INTO dead_ids(mtgstocks_id) VALUES (%s)"
        
        try:
            self.cursor.execute(dead_id_query, (mtgstocks_id,))
            print("Query:", self.cursor.query)

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            print("Query:", self.cursor.query)
            self.connection.rollback()
            self.cursor.close()
            raise

        else:
            self.connection.commit() 

    def insert_price_data(self, print_id: int, raw_price_json: str) -> None:
        price_query = "INSERT INTO price(print_id, raw_price_json) VALUES %s"
        
        try:
            psql_extras.execute_values(
                self.cursor, price_query, [print_id, raw_price_json])
            print("Query:", self.cursor.query)

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            print("Query:", self.cursor.query)
            self.connection.rollback()
            self.cursor.close()

        else:
            self.connection.commit()        

    def insert_prints_data(self, cardname: str, mtg_set: str, mtgstocks_id: int, raw_print_json: str) -> None:        
        prints_query = "INSERT INTO prints(card_name, mtg_set, mtgstocks_id, raw_print_json) VALUES %s"

        try:
            psql_extras.execute_values(
                self.cursor, prints_query, [(cardname, mtg_set, mtgstocks_id, raw_print_json)])
            print("Success: ", prints_query)

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            print("Query:", self.cursor.query)
            self.connection.rollback()
            self.cursor.close()

        else:
            self.connection.commit()

    def print_test_insert(self):
        card_name = "Force of Will"
        mtg_set = "ALR"
        mtgstocks_id = 1111
        raw_print_json = R'{"id":34655,"slug":"34655-bat-token","name":"Bat Token"}'

        data_tuple = [(card_name, mtg_set, mtgstocks_id, raw_print_json)]

        test_df = pd.DataFrame({
            "cardname": ["Force of Will"],
            "mtg_set": ["ALR"],
            "mtgstocks_id": [1111],
            "raw_print_json": [R'{"id":34655,"slug":"34655-bat-token","name":"Bat Token"}']
        })

        test_query = "INSERT INTO prints(card_name, mtg_set, mtgstocks_id, raw_print_json) VALUES %s"
        data_tuples = [tuple(row.to_numpy()) for index, row in test_df.iterrows()]

        try:
            psql_extras.execute_values(
                self.cursor, test_query, data_tuple)
            print("Query:", self.cursor.query)

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            print("Query:", self.cursor.query)
            self.connection.rollback()
            self.cursor.close()

        else:
            self.connection.commit()

    def get_mtg_stock_indices(self):
        existing_id_query = "SELECT mtgstocks_id FROM prints;"
        results = []
        try: 
            self.cursor.execute(existing_id_query)
            while True:
                # Fetch rows
                result = self.cursor.fetchmany(100)
                if result == list():
                    break
                for row in result:
                    results.append(row[0])

            return results

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            print("Query:", self.cursor.query)
            self.connection.rollback()

    def get_dead_ids(self):
        existing_id_query = "SELECT mtgstocks_id FROM dead_ids;"
        results = []
        try: 
            self.cursor.execute(existing_id_query)
            while True:
                # Fetch rows
                result = self.cursor.fetchmany(100)
                if result == list():
                    break
                for row in result:
                    results.append(row[0])

            return results

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            print("Query:", self.cursor.query)
            self.connection.rollback()    


if __name__ == "__main__":
    
    my_db = db_interface("conn_info_pi.ini")
    result = my_db.get_mtg_stock_indices()
    my_db.close()