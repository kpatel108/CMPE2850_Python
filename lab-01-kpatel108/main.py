"""
Lab01_ElectionSim_1221.ipynb_
Notebook unstarred
Lab01 - Election Simulations - Kalpan Patel
"""

from mysimulation import *
from readmyway import *

lab01_menu = [['l', 'List and select candiate files'],
        ['p', ''],
        ['s', '']]

# as usual, display the menu to the user
def print_lab01_menu():
    print('Menu :')
    for items in lab01_menu:
        c = 0
        for item in items:
            if c == 1:
                print('   : ', end='')
            print(f'{item}', end='')
            c += 1
        print('')


# Main Loop
if __name__ == '__main__':
    while True:
        print_lab01_menu()
        userSel = input('Selection: ')
        if userSel == 'l':
            cFNames = FindCandidateFiles()
            for key, value in cFNames.items():
                print(f'[{key}]-{value}')
            userSel = input('File to load: ')

            # candidate and weighting dictionary
            cw = ReadCandidateFile(cFNames[int(userSel)])

            vParam = input('How many votes? ')
            # eParam = input('How many elections?: ')

            stats = RunElection(cw,vParam)

            break