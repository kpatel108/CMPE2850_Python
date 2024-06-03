"""
Name: Kalpan Patel
Assignment: CMPE2850 ICA03
Submission Code: 1221
"""
import random as rnd
import string as s
from collections import deque

# Global variable
menu_options = [['h', 'Histogram'], ['f', 'File to Histogram'], ['p', 'Play Cards']]


# Default menu for various selections
def menu():
    print('Menu :')
    for index in menu_options:
        print(f'{index[0]}\t : {index[1]}')


# -----------------     Part A - Dictionary Histogram       -----------------
# generate a random word based on the length specified by the user
def make_big_string(str_size):
    my_letters = rnd.choice(s.ascii_lowercase)

    my_word = ''.join(rnd.choice(s.ascii_lowercase) for i in range(str_size))
    #print(my_word)
    return my_word


# create a dictionary to store letters as key and its frequency as value
def make_dict( big_str ):
    ret_dict = {}
    ret_dict.clear()

    for c in big_str:
        if c in ret_dict:
            ret_dict[c] += 1
        else:
            ret_dict[c] = 1

    return ret_dict


# show the histogram along with each letter and their frequency in the random word
def show_dict( letter_dict ):
    for c in letter_dict.items():
        print(f'{c[0]}\t: {c[1]:04} :{chr(9608) * c[1]}')


# -----------------     Part B - Histogram - File       -----------------
def process_file(file_name):
    file_contents = ''      # save file info
    try:
        with open(file_name, 'r', encoding='utf-8-sig') as fd:
            for single_word in fd:
                "I needed to iterate through each char in the word"
                for curr_letter in single_word:
                    if curr_letter.islower() or curr_letter.isupper():
                        file_contents += curr_letter
                #print('', single_word, end='')
                "Iteration was wrong as this iterates through the line, not each word"
                #print(file_contents.join( [ curr for curr in single_word if curr.isupper()  and single_word.islower() ] ))

    except Exception as exc:
        print(f'Type of exception : {type(exc)}')
        print(f'Exception was : {exc}')
        print(f'File Input failed')
    finally:
        print('Always, even on an exception')

    #print(file_contents)
    return file_contents


# -----------------     Part C - Deck of cards       -----------------
def play_cards():
    # suit : spade, heart, diamond, club
    suite_cards = [chr(9824), chr(9827), chr(9829), chr(9830)]
    # cards_values = list(v for v in range(1,14), suite_cards)
    card_values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck_cards = []
    hands_list = []

    # iterate through each element from the supplied suite collection to make cards value collection
    for card in card_values:
        for val in suite_cards:
            current_card = card + val
            deck_cards.append(current_card)
    print(f'Deck : {deck_cards}')

    # use random.shuffle() to mix'em up
    rnd.shuffle(deck_cards)
    print(f'Shuffled : {deck_cards}')

    dq_cards = deque(deck_cards)

    while len(dq_cards) >= 5:
        hand = []               # begin as a list
        for num in range(5):
            hand.append(dq_cards.popleft())
        hands_list.append(tuple(hand))          # this now a list of tuples

    for curr_index, curr_hand in enumerate(hands_list):
        print(f'Hand{curr_index + 1} : {curr_hand}')
    print(f'Leftovers : {dq_cards}')


# main loop within a while loop so menu is shown all the time after each operation
while True:
    if __name__ == '__main__':
        # show the default menu to user
        menu()

        # user prompt to pick menu options
        userChar = input('Selection: ').lower()

        if userChar == menu_options[0][0]:      # Part A - Dict Histogram
            user_num = int(input("How many characters : "))     # extract the length of a word
            rand_word = make_big_string(int(user_num))  # create a word based on the specified length
            words_dict = make_dict(rand_word)           # a dictionary consisting of letter and their occurrences
            show_dict(words_dict)                       # display Part A result

            # extract the keys fom dictionary as a set()
            key_set = set(words_dict.keys())

            """ Now find letters not used in the random word from method above
                CollectionA.difference(CollectionB) will return a Set of elements
                only from CollectionA not from CollectionB
            """
            not_chose_keys = set(s.ascii_lowercase).difference(set(key_set))

            """ Another way to achieve this without using set().
                Weird handy way of iterating and saving into a collection
            """
            # not_chose_keys2 = {c for c in s.ascii_lowercase if c not in key_set}

            " Show final result for keys not used in the word"
            print(f'Never selected : {not_chose_keys}\n')

        if userChar == menu_options[1][0]:      # Part B - Histo-file
            user_file = str(input('Enter a local filename [stuff.txt] : '))
            file_str = process_file(user_file)      # store the data from the file
            file_dict = make_dict(file_str)         # store the letter and their occurrences in a dictionary
            show_dict(file_dict)                    # display Part B display

            # extract the keys fom dictionary as a set()
            file_key_set = set(file_dict.keys())

            # Figure out letters not used in the dictionary
            file_new_keys = set(s.ascii_lowercase).difference(set(file_key_set))

            print(f'Never selected : {file_new_keys}\n')

        if userChar == menu_options[2][0]:      # Part C - Deck of Cards
            play_cards()