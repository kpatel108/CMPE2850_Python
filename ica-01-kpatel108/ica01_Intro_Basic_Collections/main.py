import numpy as n
import matplotlib.pyplot as plt
import random as r

menu = [['p', 'Palindrome'],['r', 'Random Distribution Stats'], ['s', 'Shuffle Distribution Stats'], ['l', 'List Comparisons']]

pStrings = ["abcdefghgfedcbb",      # boundary outside
            "abcdefghigfedcba",     # boundary inside
            "abczefghgfedcba",      # boundary midsize
            "abcdefghijklmnop",     # plainly, NO
            "abcdefghgfedcba",      # odd number
            "abcdefggfedcba"]       # even number

def Menu() -> None:
    print('Menu :')
    for a in menu:
        print(f'{a[0]:3}: {a[1]}')
    # return input("Selection : ")

# check whether the string passed into ia s palindrome or not
def Palindrome(sWord) -> None:
    user_char_len = len(sWord)
    mid_length = user_char_len // 2
    rev_num = -1

    # scan each char in the word to reach the mid-length of the word
    for x in range(mid_length):
        if sWord[x] == sWord[rev_num]:
            x += 1
            rev_num -= 1
        else:
            print("is not a palindrome")
            break
    else:
        print(sWord, "is a palindrome")

def palindromeV2(testStr):
    head = 0
    tail = len(testStr) - 1

    # scan until the end of the word
    while head < len(testStr):
        if (testStr[head] == testStr[tail]):
            print(f'{head} - {testStr[head]} = {testStr[tail]}')    # show the  correct result
        else:
            print(f'{head} - {testStr[head]}')

        head = head + 1
        tail = tail - 1

    return testStr == testStr[::-1]


def RandomDistribution( runs, rand_range ):
    print("Not implemented yet")
    distribution = [0] * rand_range
    dict = {}

    # generate random numbers from 0 to user choice specified
    for iNum in range(runs):
        rand_num = r.randrange(0, rand_range, 1)
        distribution[rand_num] += 1

        # add all occurrence of each number in the dictionary as a value
        if not (rand_num in dict):
            dict[rand_num] = 1
        else:
            dict[rand_num] += 1

    for value in range(rand_range):
        distribution[value] /= runs

    expected_distribution = 100 / rand_range
    return expected_distribution, distribution, dict


def ShuffleDistribution(runs, rand_range):
    start_arr = [0] * (rand_range // 10)
    current_index = 0

    for a in range(0, rand_range, 10):
        start_arr[current_index] = a
        current_index += 1

    print(start_arr)

    sum_arr = [0] * (rand_range // 10)
    for i in range(runs):
        current_index = 0
        r.shuffle(start_arr)

        for rarr in start_arr:
            sum_arr[current_index] += start_arr[current_index]
            current_index += 1
    sum_of_all = sum(sum_arr)
    current_index = 0
    for i in sum_arr:
        dif = i - (sum_of_all / (rand_range // 10))
        perdif = (dif / (sum_of_all / (rand_range // 10))) * 100
        print(f'[{current_index:03d}] = {i} error\t\t {round(perdif, 3)}%')
        current_index += 1


def ListComparisons( leftList, rightList ):
    left, right, intersect, leftOnly, rightOnly = [], [], [], [], []
    left = list.copy(leftList)
    print(f'left : {left}')
    right = list.copy(rightList)
    print(f'right : {right}')

    for left_item in left:
        for right_item in right:
            if left_item == right_item:
                intersect.append(left_item)

    # popping the elements in the intersect list and display them
    i = 0
    intersect_count = len(intersect)
    print('Intersect : ', end='')
    while i < intersect_count:
        print(f'{intersect.pop()} + ', end='')
        i += 1

    # populate leftOnly with elements only in the leftList
    print('\nLeftOnly : ', end='')
    for my_item in left:
        if my_item not in right:
            leftOnly.append(my_item)
            print(f'{my_item}<<', end='')


# while True:
#     # Press the green button in the gutter to run the script.
#     if __name__ == '__main__':
#         Menu()
#
#         # user prompt to pick menu options
#         userChar = input('Selection: ').lower()
#         if userChar == 'p':
#             # iterate each word from the array
#             for sWord in pStrings:
#                 print(f'{sWord} : Palindrome = {palindromeV2(sWord)}')
#             #Palindrome('abcdefghgfedcba')
#         elif userChar == 'r':
#             RandomDistribution(1, 1)
#         elif userChar == 's':
#             print("Not done")
#         elif userChar == 'l':
#             print('Not done')


def check_input(choice):
    for item in menu:
        if choice == item[0]:
            return True


if __name__ == '__main__':
    userChoice = None
    Menu()
    userChoice = input("Selection : ")
    while not check_input(userChoice):
        continue
    # This looks way cleaner than above using "Walrus operator"
    # userChoice = input("Selection : ")
    # while not check_input(userChoice := Menu()):
    #     continue

    if userChoice == 'p':
        # iterate each word from the array
        for sWord in pStrings:
            print(f'{sWord} : Palindrome = {Palindrome(sWord)}')

    if userChoice == 'r':
        print("Not finish")
        user_ans_1 = int(input('Input runs : '))
        user_ans_2 = int(input('Input range : '))
        expected_distribution, distribution, count = RandomDistribution(user_ans_1, user_ans_2)
        sum_percent = 0
        index = 0

        for a in distribution:
            sum_percent += distribution[index]
            print(f'[{index}] = {count[index]} actual {round(distribution[index] * 100, 4):0.2f}'
                  f'% expected : {expected_distribution}%')
            index += 1
        print(f'Sum of % : {sum_percent * 100:0.3f}')

    if userChoice == 's':
        num_of_runs = int(input("Input runs : "))
        range_val = int(input("Input range : "))
        ShuffleDistribution(num_of_runs, range_val)

    if userChoice == 'l':
        defaultLeftList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']
        defaultRightList = ['j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        left_input = list(input(f'Left list [{defaultLeftList}] : '))
        right_input = list(input(f'Right List : [{defaultRightList}] : '))

        if left_input == '' and right_input == '':
            ListComparisons(defaultLeftList, defaultRightList)
        else:
            ListComparisons(left_input, right_input)

# THE END