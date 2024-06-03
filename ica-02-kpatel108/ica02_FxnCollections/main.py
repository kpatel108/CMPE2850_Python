"""
Name: Kalpan Patel
Assignment: CMPE2850 ICA02
Submission Code: 1221
"""

import random as r
import collections as c

menu_list = [['s', 'Shuffle Stats'], ['a', 'Analyze Stats']]


# Initial menu
def menu():
    for x in menu_list:
        print(f'{x[0]}\t : {x[1]}')

    return input('Selection : ')

def validanswer(val):
    for o in menu_list:
        if val == o[0]:
            return True


# Shuffle
def shuffled(list_vals):
    shuffled_copy = list.copy(list_vals)

    for val in range(len(shuffled_copy)):
        rand_index = r.randrange(val, len(shuffled_copy))
        tmp = shuffled_copy[val]
        shuffled_copy[val] = shuffled_copy[rand_index]
        shuffled_copy[rand_index] = tmp

    return shuffled_copy


def shuzzled(list_val):
    shuzzled_list = list.copy(list_val)

    for val in range(len(shuzzled_list)):
        rand_index = r.randrange(val, len(shuzzled_list))
        if val + 1 != len(shuzzled_list):
            rand_index = r.randrange(val + 1, len(shuzzled_list))
        tmp = shuzzled_list[val]
        shuzzled_list[val] = shuzzled_list[rand_index]
        shuzzled_list[rand_index] = tmp

    return shuzzled_list


def shufflestats(runs, items, **kwargs):
    if 'algo' in kwargs:
        algorithm = kwargs['algo']
        algorithm(items)
        stats_collection = [0] * len(items)
        
        for num in range(runs):
            shuff_collection = algorithm(items)

            for curr_index in range(len(shuff_collection)):
                stats_collection[curr_index] += shuff_collection[curr_index]

        expected_value = sum(stats_collection) / (len(items) * runs)

        print(f'Shuffle Stats for : {algorithm.__name__}')

        for i in range(len(items)):
            deviation = (stats_collection[i] / runs - expected_value) / expected_value * 100
            print(f'[{i:03d}] = {stats_collection[i]} error\t\t{deviation:0.3f}%')

        print('\n')     # leave an empty line at the end

        return stats_collection


def analyzestats(stats_data):
    print(f'Analyze stats for {len(stats_data)} elements')
    data = c.Counter(stats_data)
    data_list = dict(data)
    mode_list = []

    min_value = min(stats_data)
    max_value = max(stats_data)
    average_value = sum(stats_data) / len(stats_data)
    print(f'Min : {min_value}')
    print(f'Max : {max_value}')
    print(f'Avg : {average_value}')

    highest_frequency = max(list(data.values()))
    for key in data_list:
        if data_list[key] == highest_frequency:
            mode_list.append(key)
    print(f'Modes : {mode_list} with frequency of {highest_frequency}')

    return min_value, max_value, average_value, mode_list, highest_frequency


if __name__ == '__main__':
    ans = None

    while not validanswer(answer := menu()):
        continue

    # Shuffle Stats
    stats = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 2, 4, 2, 4, 3, 3]
    if answer == 's':
        num_runs = input('Input runs : ')

        while not num_runs.isnumeric():
            num_runs = input('Input runs : ')

        num_runs = int(num_runs)
        num_range = input('Input range : ')

        while not num_range.isnumeric():
            num_range = input('Input range : ')

        num_range = int(num_range)
        algo_selection = input('Algorithm Selection, default = Shuffled, z = Shuzzled : ')

        list_new = []
        for num in range(num_range):
            list_new.append(r.randint(0, num_range))

        if algo_selection == 'z':
            stats = shufflestats(num_runs, list_new, algo=shuzzled)
        elif algo_selection == 's':
            stats = shufflestats(num_runs, list_new, algo=shuffled)

        # Analyze Stats
        new_answer = menu()
        if new_answer == 'a':
            print(f'Stats List : {stats}')
            new_stats = analyzestats(stats)
    elif answer == 'a':
        print(f'Stats List : {stats}')
        new_stats = analyzestats(stats)