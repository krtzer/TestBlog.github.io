import psycopg2
from configparser import ConfigParser
from typing import Dict

# References 
# This describes concerns about character encoding 
#   https://www.programmersought.com/article/8419605951/
# Users in Postgres need a password (be careful of spaces), need to be created, and it users 
# the super user from linux to authenticate, meaning, you need to make a postgres user 
# Don't forget to edit the nano /etc/postgresql/10/main/pg_hba.conf and 
# nano /etc/postgresql/10/main/postgresql.conf
#   https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e
#   https://blog.logrocket.com/setting-up-a-remote-postgres-database-server-on-ubuntu-18-04/
#   https://dba.stackexchange.com/questions/100564/cant-connect-to-remote-postgresql-database
# For VS code and python 3.9, virtual environments and the debugger just do not work!
#   https://code.visualstudio.com/docs/python/debugging 
#   https://stackoverflow.com/questions/56794940/debugger-not-stopping-at-breakpoints-in-vs-code-for-python
#   need to file a bug on this 
# Basically copying this for database design
#   https://medium.com/swlh/create-your-first-postgresql-database-in-python-with-psycopg2-9d0986e0e9ac
# For some reason, i cannot click on the this website, but it's very useful to design of this as well
# 
# https://www.analyticsvidhya.com/blog/2020/08/analysing-streaming-tweets-with-python-and-postgresql/

def load_connection_info(ini_filename: str) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info

def create_db(conn_info: Dict[str, str],) -> None:
    # Connect just to PostgreSQL with the user loaded from the .ini file
    psql_connection_string = f"user={conn_info['user']} password={conn_info['password']} host={conn_info['host']} dbname={conn_info['database']}"
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']}"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")

        if e.pgcode == '42P04':
            print(str(e.pgerror))
            pass
        else:
            cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False

def create_table(sql_query: str, conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()

if __name__ == "__main__":
    # host, database, user, password
    conn_info = load_connection_info("conn_info_pi.ini")

    # Create the desired database
    create_db(conn_info)

    # Connect to the database created
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    # Create the "prints" table
    prints_sql = """
        CREATE TABLE IF NOT EXISTS prints (
            id SERIAL NOT NULL PRIMARY KEY,
            card_name VARCHAR (100),
            mtg_set VARCHAR (5),
            mtgstocks_id INT,
            raw_print_json JSONB NOT NULL
        )
    """
    create_table(prints_sql, connection, cursor)


    # Create the "prices" table
    prices_sql = """
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY, 
            print_id INT REFERENCES prints(id),
            raw_price_json JSONB NOT NULL
        )
    """
    create_table(prices_sql, connection, cursor)

    # Create the "dead_ids" table
    dead_id_sql = """
        CREATE TABLE IF NOT EXISTS dead_ids (
            id SERIAL PRIMARY KEY,
            mtgstocks_id integer NOT NULL
        )
    """
    create_table(dead_id_sql, connection, cursor)

    # Close all connections to the database
    connection.close()
    cursor.close()
