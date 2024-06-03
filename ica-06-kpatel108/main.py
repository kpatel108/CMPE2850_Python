"""
Name: Kalpan Patel
Assignment: CMPE2850 ICA06
Submission Code: 1221
"""

# packages
import mysql.connector
from mysql.connector import cursor
from decimal import Decimal
from statistics import mean
from functools import  reduce
import locale
# my includes
from Bars import *
import BarsTest

# Global variables
ica6_menu_options = [['c', 'Connect to the DB'], ['gt','Get Tables'], ['gd', 'Get Data'],
                     ['t', 'Get Titles'], ['s', 'Get Sales'], ['b', 'Bar Test']]
mysql_db = None


# Global functions ( to be used by all parts )
def ica6_menu():
    print('ica06 - Menu : ')
    # iterate through the list for displaying
    for index in ica6_menu_options:
        print(f'{index[0]}\t : {index[1]}')

    return input('Selection : ')


# verify valid user input for proceeding the respective operation
def check_user(user_val):
    for menu_item in ica6_menu_options:
        if user_val == menu_item[0]:
            return True


#   Part A - mySQL DB connections and queries
#def db_connect(db_pass):
def db_connect(db_pass) -> 'mysql':
    try:
        my_host = 'thor.cnt.sast.ca'
        my_user = 'kpatel18_rebel'
        my_pass = db_pass
        my_db_name = 'kpatel18_pubs'

        mysql_db = mysql.connector.connect( host=my_host, user=my_user, password=my_pass, database=my_db_name )

    except mysql_db.connector.Error as err:
        print(f'db_connect() : except Error : {err}')

    if mysql_db != None and mysql_db.is_connected():
        print(f'Connected to : {mysql_db.get_server_info()}\n')

    return mysql_db;


#   Part B - Get Book Titles
# Custom function (not part of ica) to get all details regarding any given table name from the database
# to further analyze the data
def get_data(conn_obj, table_name):     # function to see all data from the table for debugging
    try:
        cursor = conn_obj.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        data_col_names = cursor.column_names
        returned_data = cursor.fetchall()
        print(data_col_names)
        print(f'{returned_data}\n')

    except mysql_db.connector.Error as err:
        print(f'get_data() : Error : {err}')
        returned_data = None

    finally:
        cursor.close()  # remember to close the cursor(), you are done with it


def get_tables(conn_obj):
    try:
        table_cursor = conn_obj.cursor(buffered=True)
        table_cursor.execute("SHOW TABLES")
        mytables = [table[0] for table in table_cursor.fetchall()]
        print(f'{mytables}\n')

    except mysql_db.connector.Error as err:
        print(f'get_tables() : Error : {err}')


def get_titles(conn_obj, titles_filter):
    titles_col_names = None
    titles_resultset = None
    try:
        titles_cursor = conn_obj.cursor(buffered=True)

        """ 
            SELECT * FROM Titles"
            title = %s 
            LIMIT 100
        """
        titles_query = f"SELECT * FROM Titles WHERE title like %s LIMIT 100"

        # placeholder for filter to be specified by the user
        titles_params = ( f'%{titles_filter}%', )     # comma for a TUPLE, or result is just a single expression

        # save data into a TUPLE
        titles_cursor.execute(titles_query, titles_params)

        # retrieve the column names
        titles_col_names = titles_cursor.column_names
        #print(f'column_names : {titles_col_names}')

        titles_resultset = titles_cursor.fetchall()

    except mysql_db.connector.Error as err:
        print(f'get_titles() : except Error : {err}')
        titles_resultset = None

    finally:
        titles_cursor.close()  # remember to close the cursor(), you are done with it

    return titles_col_names, titles_resultset


# Part C - Get Book Sales
def get_book_sales(conn_obj, book_filter):
    sales_resultset = None
    try:
        sales_cursor = conn_obj.cursor( buffered=True, dictionary=True )

        sales_query = f"SELECT t.title_id, t.title, t.type, t.price, ROUND( SUM( s.qty * t.price ), 2 ) AS 'sales' " \
                      f"FROM Titles AS t JOIN Sales AS s ON t.title_id = s.title_id " \
                      f"WHERE title LIKE %s GROUP BY t.title_id, t.title, t.type, t.price"
        """
            SELECT	t.title_id, title, [type], price,
                    ROUND( SUM( qty * price ), 2 ) AS 'sales'
                    FROM Titles AS t
                    JOIN Sales AS s ON t.title_id = s.title_id
                    WHERE title LIKE '%bu%'
                    GROUP BY t.title_id, t.title, t.[type], price
            GO
        """
        sales_param = ('%' + book_filter + '%', )           # save parameter(s) into a tuple
        sales_cursor.execute(sales_query, sales_param)      # execute the query
        sales_resultset = sales_cursor.fetchall()           # fetch the resulting data as a TUPLE from the query

    except mysql_db.connector.Error as err:
        print(f'get_book_sales() : except Error : {err}')
        sales_resultset = None

    finally:
        sales_cursor.close()  # remember to close the cursor(), you are done with it

    return sales_resultset


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mydb = None
    user_ans = None

    # initial user prompt when the program loads
    while not (check_user(user_ans := ica6_menu())):
        continue

    # Connect with database using supplied password from the user
    if user_ans == 'c':
        mydb = db_connect('Demo_03_')
        #user_pass = str.input("Password for demo_user : ")
        while not (check_user(user_ans := ica6_menu())):
            continue

    if user_ans == 'gd':
        get_data(mydb, 'Authors')

        # Let's ask for other operation
        while not (check_user(user_ans := ica6_menu())):
            continue

    if user_ans == 'gt':
        get_tables(mydb)

        # Let's ask for other operation
        while not (check_user(user_ans := ica6_menu())):
            continue

    if user_ans == 't':
        filter_input = input("Enter filter for [titles] : ")
        titles_data = get_titles(mydb, filter_input)
        print(f'Column names : {titles_data[0]}')
        print('Result set :')

        # iterate the resulting data from the function based on the correct index
        for t in titles_data[1]:
            print(t)

        prices_data = [t[4] for t in titles_data[1]]        # list-comprehension method
        mean_amount = mean(prices_data)

        print(f'Average price : ${mean_amount:0.2f}\n')

        # Let's ask for other operation
        while not (check_user(user_ans := ica6_menu())):
            continue

    if user_ans == 's':
        filter_input = input('Enter filter for [titles] : ')
        sales_data = get_book_sales(mydb, filter_input)

        for x in sales_data:
            print(x)

        # iterate and extract the sales from the tuple using lambda
        sales_amount = map(lambda item: item['sales'], sales_data)
        sum_of_sales = sum(sales_amount)

        print(f'Sum of Sales : ${sum_of_sales}')

        # Let's ask for other operation
        while not (check_user(user_ans := ica6_menu())):
            continue