"""
Name: Kalpan Patel
Assignment: CMPE2850 ICA04
Submission Code: 1221
"""
import math
import random as rnd
import requests as req
from bs4 import BeautifulSoup
import os as inout
from datetime import datetime

# Global variables
ica4_menu_options = [['g','Web Search'], ['p', 'Parse Page'], ['s', 'Save']]


# display the initial ica 4 menu selection for user
def ica4_menu():
    print('\nICA04 - Menu :')
    for x in ica4_menu_options:
        print(f'{x[0]}: {x[1]}')

    return input('Selection : ')


# verify valid user input for proceeding the respective operation
def check_user(user_val):
    for menu_item in ica4_menu_options:
        if user_val == menu_item[0]:
            return True


# Part A - Web page retrieval using requests
# try to connect the given web page using "GET" web request
def getpage(**kwargs):
    base_url = 'https://www.memoryexpress.com/Search/Products?'
    if 'Search' in kwargs or 'PageSize' in kwargs:
        for item in kwargs:
            kwargs['Search'] = 'psu'
            kwargs['PageSize'] = '80'
            kwargs['Sort'] = 'Manufacturer'
            # append the name/value pairs on the baseURL in standard query
            base_url += f'{item}={kwargs[item]}&'
    # print(f'Base URL : {base_url}')

    req_obj = req.get(base_url)

    if req_obj.status_code == 200:
        print(f'Web Request : {req_obj.url}')
        print(f'Request status code : {req_obj.status_code}')
        return req_obj.text
    else:
        return None


# Part B - Parse Web Response
def parse_page(parse_text):
    bs = BeautifulSoup(parse_text, features='html.parser')
    num_of_price = 0
    web_data = bs.findAll('div', class_='c-shca-icon-item__summary-list')
    f_price = 0.0
    price_dict = {}

    # iterate through returned object from the web
    for span in web_data:
        # save all <span> objects into a collection
        span_object = span.findAll('span')
        # now iterate the inner group as each line of <span> objects
        for inner_object in span_object:
            # now entering specific part of price section
            for new_obj in inner_object:
                # sanity check, to make sure we don't iterate anything funny or extraneous
                if len(str(new_obj)) != 0:
                    price = str(new_obj).strip()        # remove any whitespaces found
                    # look for dollar sign to be sure that we got the price
                    if price.startswith('$'):
                        num_of_price += 1
                        price = price.strip('$')        # remove the dollar sign
                        # remove unnecessary punctuations like comma with empty string
                        if price.__contains__(','):
                            price = price.replace(',', '')
                        f_price = float(price)
                        min_range = math.floor(f_price / 10) * 10
                        max_range = math.ceil(f_price / 10) * 10

                        if (min_range, max_range) not in price_dict:
                            price_list = [f_price]
                            price_dict[(min_range, max_range)] = price_list
                        else:
                            price_dict[(min_range, max_range)].append(f_price)

    header = f'In {bs.title.text}, Found {[num_of_price]} prices'
    print(header)

    for k in price_dict:
        print(f'Price Range :{k} : {price_dict[k]}')
    return price_dict


# Part C - Save the dictionary
def save(some_dict, file_name):
    file_num = 1
    file_path = inout.path.join(inout.getcwd(), file_name)

    # if file exists, append _N to the name part of the file doesn't exist
    while (inout.path.isfile(file_path) and file_num <= 99):
        tup_files = inout.path.splitext(file_name)
        file_path = f'{tup_files[0]}_{file_num}{tup_files[1]}'
        file_num += 1

    fd = inout.open(file_path, inout.O_RDWR | inout.O_CREAT)

    extract_file_name = inout.path.split(file_path)
    file_path = extract_file_name[1]

    price_range = dict(sorted(some_dict.items(), key=lambda x:x[1]))
    inout.write(fd, f'{file_path}_saved\nPrice information as of : {datetime.now().isoformat()}\n').encode()

    for key, val in price_range.items():
        inout.write(fd, f'Price Range : {key} : {val}\n'.encode())

    return file_path


# MAIN MENU
if __name__ == '__main__':
    user_ans = None

    while not check_user(user_ans := ica4_menu()):
        continue

    if user_ans == 'g':         # Web Search
        user_search = input('Search : ')
        user_pg_size = input('PageSize 40/[80]/120 : ')
        user_sort_val = input('Sort - Relevance/Price/PriceDesc/[Manufacturer] : ')

        web_req_txt = getpage(Search=user_search, PageSize=user_pg_size, Sort=user_sort_val);

        while not check_user(user_ans := ica4_menu()):
            continue

        if user_ans == 'p':
            parse_dict = parse_page(web_req_txt)

            while not check_user(user_ans := ica4_menu()):
                continue

            if user_ans == 's':
                user_file_name = input('Please input file name [out.txt] : ')

                if len(user_file_name) <= 0:
                    user_file_name = 'out.txt'

                name = save(parse_dict, user_file_name)
                print(f'{name} saved')