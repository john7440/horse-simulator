#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from colorama import Fore, Style, init
# We use this to not have to reset the color each time we print
init(autoreset=True)


def format_horse_bar(horse, race_length=2400, bar_width=50, current_turn =None):
    """
    This function is used to display the race of horse
    :param current_turn: the current turn of the race
    :param horse: each horse
    :param race_length: length of the race
    :param bar_width: the width of the bar
    :return:
    """
    horse_icon = "🐎"
    horse_num = f"Horse {horse['horse']:2}"

    # Disqualified at this turn
    if horse['disqualified'] and horse['disqualified_turn'] == current_turn:
        bar = Fore.RED + 'X' * bar_width
        status = Fore.RED + 'DISQUALIFIED'

    # If the horse is still in the race
    elif not horse['disqualified'] and horse['position'] >= 0:
        progress_ratio = horse['position'] / race_length
        progress = max(0, min(int(progress_ratio * bar_width), bar_width))

        # Dynamic colors for progress
        if progress > bar_width * 0.8:
             bar_color = Fore.GREEN
        elif progress > bar_width * 0.5:
            bar_color = Fore.BLUE
        else:
            bar_color = Fore.YELLOW

        bar = bar_color + '█' * progress + Style.DIM + '-' * (bar_width - progress)
        status = Fore.CYAN + f"{horse['position']:4}m".ljust(10)

    # Disqualified at this turn, ignored after (next turn)
    else:
        return None

    return f"{horse_icon} {horse_num} | {bar} | {status}"


def display_race(horse_l, race_length=2400, bar_width=50, current_turn=None):
    """
    This function is used to display the race,
    sort the list and print the race
    :param horse_l: the list of horses
    :param race_length: the length of the race
    :param bar_width: the width of the bar
    :param current_turn: the current turn of the race
    :return: None
    """
    print(f"\n{Fore.MAGENTA}----------------🏁🏁🏁 Race state — Turn {current_turn} 🏁🏁🏁----------------\n")
    sorted_horses = sorted(horse_l, key=lambda h: h['position'], reverse=True)

    for horse in sorted_horses:
        line = format_horse_bar(horse, race_length, bar_width, current_turn)
        if line:
            print(line)



def kind_of_result():
    """
    This function ask user what kind of course does he want,
    verify if its valid then return the type of result desired.
    :return: the desired kind of result
    """
    while True:
        try:
            user_choice = int(input("\nWhich kind of result do you want (3,4 or 5)? "))
            if 3 <= user_choice <= 5:
                return user_choice
            else:
                print("\nPlease enter a valid kind of result")
        except ValueError:
            print("\nInvalid Input! Please enter a valid number (3,4 or 5)")


def roll_dice():
    """
    This fonction simulate a random dice roll between 1 and 6.
    :return: a number between 1 and 6.
    """
    random_number = random.randint(1,6)
    return random_number


def generate_list(horse_number):
    """
    This function generates a list of horse (dict),
    each of them have a number, their actual speed, a history of each turn,
    the finish and the disqualified status.
    :param horse_number: the number of horses chosen by user.
    :return: a list of dictionaries where each dictionary represents one horse.
    """
    horse_list = []
    for i in range(horse_number):
        horse_list.append({'horse': i + 1 ,
                           'position': 0 ,
                           'actual_speed': 0,
                           'finish_turn':None,
                           'disqualified': False,
                           'disqualified_turn': None})
    return horse_list


def simulate_course(horse_l):
    """
    This function simulates a course for each horse,
    every turn, rolling a dice that will determinate the distance
    the horse will do.
    :param horse_l: the list of dictionaries where each dictionary represents one horse.
    :return: the final ranking
    """
    turn = 0

    # Speed modifiers
    rolling_dice = [
        {'speed1': 0,  'speed2': +1, 'speed3': +1, 'speed4': +1, 'speed5': +2, 'speed6': +2},
        {'speed1': 0,  'speed2':  0, 'speed3': +1, 'speed4': +1, 'speed5': +1, 'speed6': +2},
        {'speed1': 0,  'speed2':  0, 'speed3': +1, 'speed4': +1, 'speed5': +1, 'speed6': +2},
        {'speed1': -1, 'speed2':  0, 'speed3':  0, 'speed4': +1, 'speed5': +1, 'speed6': +1},
        {'speed1': -1, 'speed2':  0, 'speed3':  0, 'speed4': 0,  'speed5': +1, 'speed6': +1},
        {'speed1': -2, 'speed2': -1, 'speed3':  0, 'speed4': 0,  'speed5':  0, 'speed6': +1},
        {'speed1': -2, 'speed2': -1, 'speed3':  0, 'speed4': 0,  'speed5':  0, 'speed6': 'DQ'}
    ]

    base_speed = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}

    while any(not h['disqualified'] and h['position'] < 2400 for h in horse_l):
        turn += 1
        print(f"\n----------------------- Turn {turn} ---------------------------")
        choice = input("Press Enter to continue to the next turn (or 'Q' to quit): ").lower()
        if choice == 'q':
            print('\nThank you for playing!')
            break

        for horse in horse_l:
            if horse['position'] >= 2400 or horse['disqualified']:
                continue

            dice = roll_dice()
            current_speed = min(horse['actual_speed'], 6)
            modifiers = rolling_dice[current_speed]
            key = f'speed{dice}'
            modified = modifiers[key]

            if modified == 'DQ':
                horse['disqualified'] = True
                horse['disqualified_turn'] = turn
                horse['position'] = -1
                continue

            new_speed = max(1, min(dice + modified, 6))
            horse['actual_speed'] = new_speed
            horse['position'] += base_speed[new_speed]

            if horse['position'] >= 2400 and horse['finish_turn'] is None:
                horse['finish_turn'] = turn

        display_race(horse_l, current_turn=turn)

    # Final ranking: sorted by order then position
    ranking = sorted(
        horse_l,
        key=lambda h: (
            h['finish_turn'] if h['finish_turn'] is not None else float('inf'),
            -h['position']
        )
    )
    return ranking, turn


def print_out(rank,type_of_c , total_of_turns):
    """
    This function prints out the final ranking and attribute medals.
    :param total_of_turns: the total number of turns
    :param rank: the ranking generated by simulate_course()
    :param type_of_c: type of course (tiercé, quarté or quinté)
    :return: formated ranking
    """
    print('\n=============================================================')
    print('================🏁🏁🏁Race Finished!🏁🏁🏁=================')
    print('=============================================================\n')
    print('-----------------Final Ranking-----------------')
    medals = ['🥇', '🥈', '🥉']

    for index, horse in enumerate( rank[:type_of_c]):
        if horse['finish_turn'] is not None:
            time_in_second = horse['finish_turn'] * 10
            minutes = time_in_second //60
            secondes = time_in_second % 60
            formatted_time = f"{minutes}m {secondes:02}s"

        else:
            formatted_time = "Did Not Finished"

        # We attribut medals to the first 3
        medal = medals[index] if index < len(medals) else ''
        print(f'{index + 1:2}. Horse {horse["horse"]:2} → Position: {horse["position"]:4}m → Time: {formatted_time}  {medal} ')


def how_many_horses() -> int:
    while True:
        number_of_horses = int(input("How many horses do you want to simulate? (12-20): "))
        if 12 <= number_of_horses <= 20:
            break
        else:
            print("That is not a valid choice. Please try again. A number between 12 and 20")
    return number_of_horses

def main():
    """
    This is the main function.
    It contains the multiples calls to other functions.
    :return: None
    """
    number_of_horses = how_many_horses()
    horse_list = generate_list(number_of_horses)
    k = kind_of_result()
    ranking, total_turns = simulate_course(horse_list)
    print_out(ranking, k,total_turns)




if __name__=='__main__':
    main()