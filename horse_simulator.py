#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from sys import base_prefix


def kind_of_course():
    """
    This function ask user what kind of course does he want
    :return: the desired kind of course
    """
    user_choice = int(input("What kind of course do you want? 3,4 or 5?"))
    while True:
        if user_choice == 3:
            return 3
        elif user_choice == 4:
            return 4
        elif user_choice == 5:
            return 5
        else:
            print("That is not a valid choice")


def roll_dice():
    """
    This fonction simulate a random dice roll between 1 and 6.
    :return: a number between 1 and 6.
    """
    random_number = random.randint(1,6)
    return random_number


def generate_list(horse_number):
    """
    This function generates a list of horse (dict)

    :param horse_number: the number of horses chosen by user.
    :return: a list of dictionaries where each dictionary represents one horse.
    """
    horse_list = []
    for i in range(horse_number):
        horse_list.append({'horse': i + 1 , 'position': 0 , 'history': [], 'actual speed':0})
    return horse_list


def simulate_course(horse_l,type_of_course):
    """
    This function simulates a course for each horse,
    every turn, we roll a dice that will determinate the distance
    the horse will do.
    :param horse_l: the list of dictionaries where each dictionary represents one horse.
    :return: the final ranking
    """
    turn = 0
    rolling_dice = [
        {'actual speed': 0, 'speed1': 0, 'speed2': +1, 'speed3': +1, 'speed4': +1, 'speed5': +2, 'speed6': +2},
        {'actual speed': 1, 'speed1': 0, 'speed2': 0, 'speed3': +1, 'speed4': +1, 'speed5': +1, 'speed6': +2},
        {'actual speed': 2, 'speed1': 0, 'speed2': 0, 'speed3': +1, 'speed4': +1, 'speed5': +1, 'speed6': +2},
        {'actual speed': 3, 'speed1': -1, 'speed2': 0, 'speed3': 0, 'speed4': +1, 'speed5': +1, 'speed6': +1},
        {'actual speed': 4, 'speed1': -1, 'speed2': 0, 'speed3': 0, 'speed4': 0, 'speed5': +1, 'speed6': +1},
        {'actual speed': 5, 'speed1': -2, 'speed2': -1, 'speed3': 0, 'speed4': 0, 'speed5': 0, 'speed6': +1},
        {'actual speed': 6, 'speed1': -2, 'speed2': -1, 'speed3': 0, 'speed4': 0, 'speed5': 0, 'speed6': 'DQ'}]
    base_speed = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}
    while all(horse['position'] < 2400 for horse in horse_l):
        turn += 1
        for horse in horse_l:
            if horse['position'] < 2400:
                dice = roll_dice()
                current_speed = min(horse['actual speed'],6)
                modifiers = rolling_dice[current_speed]
                key = f'speed{dice}'
                modified_speed = modifiers[key]

                if modified_speed  == 'DQ':
                    print(f"Horse {horse['horse']} disqualified on turn {turn}")
                    horse['position'] = -1
                    continue

                adjusted_dice = dice + modified_speed
                adjusted_dice = max(1, min(adjusted_dice, 6))

                distance = base_speed[adjusted_dice]
                horse['actual speed'] = current_speed
                horse['position'] += distance
                horse['history'].append(distance)

    print('===============Course ended!========================')
    ranking = sorted(horse_l, key = lambda horse: horse['position'], reverse = True)
    for index, horse in enumerate(ranking[:type_of_course]):
        print(f'{index+1:2}. Horse : {horse["horse"]:2}  -> position: {horse["position"]}')



def main():
    """
    This is the main function.
    :return:
    """
    number_of_horses = int(input("How many horses do you want to simulate? (12-20): "))
    if not 12 <= number_of_horses <= 20:
        print('Invalid Input')
        return
    horse_list = generate_list(number_of_horses)
    k = kind_of_course()

    simulate_course(horse_list, k)


if __name__=='__main__':
    main()