#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def display_race(horse_l, race_length=2400, bar_width=50):
    """
    This function is used to display the race of horse
    :param horse_l: the sorted list of horses
    :param race_length: length of the race
    :param bar_width: the width of the bar
    :return:
    """
    print("\nRace state:")
    sorted_horses = sorted(horse_l, key=lambda h: h['position'], reverse=True)
    for horse in sorted_horses:
        if horse.get('disqualified', False):
            print(f"Horse {horse['horse']:2} | {'X'*bar_width} | DISQUALIFIED")
        else:
            progress = int((horse['position'] / race_length) * bar_width)
            bar = '█' * progress + '-' * (bar_width - progress)
            print(f"Horse {horse['horse']:2} | {bar} | {horse['position']:4}m")


def kind_of_course():
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
            print("\nPlease enter a valid number (3,4 or 5)")



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
        horse_list.append({'horse': i + 1 , 'position': 0 , 'history': [], 'actual speed':0, 'finish':None, 'disqualified': False})
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

    # The rules about speed and modifiers
    rolling_dice = [
        {'actual speed': 0, 'speed1': 0, 'speed2': +1, 'speed3': +1, 'speed4': +1, 'speed5': +2, 'speed6': +2},
        {'actual speed': 1, 'speed1': 0, 'speed2': 0, 'speed3': +1, 'speed4': +1, 'speed5': +1, 'speed6': +2},
        {'actual speed': 2, 'speed1': 0, 'speed2': 0, 'speed3': +1, 'speed4': +1, 'speed5': +1, 'speed6': +2},
        {'actual speed': 3, 'speed1': -1, 'speed2': 0, 'speed3': 0, 'speed4': +1, 'speed5': +1, 'speed6': +1},
        {'actual speed': 4, 'speed1': -1, 'speed2': 0, 'speed3': 0, 'speed4': 0, 'speed5': +1, 'speed6': +1},
        {'actual speed': 5, 'speed1': -2, 'speed2': -1, 'speed3': 0, 'speed4': 0, 'speed5': 0, 'speed6': +1},
        {'actual speed': 6, 'speed1': -2, 'speed2': -1, 'speed3': 0, 'speed4': 0, 'speed5': 0, 'speed6': 'DQ'}]

    # A dict with correspondance between speed and distance
    base_speed = {0: 0, 1: 23, 2: 46, 3: 69, 4: 92, 5: 115, 6: 138}

    while any(not horse.get('disqualified', False) and horse['position'] < 2400 for horse in horse_l):
        turn += 1
        print(f"\n--- Turn {turn} ---")
        choice = input("Press Enter to continue to the next turn (or type 'q' to quit): ")
        if choice == 'q':
            break
        else:
            active_horses = []
            for horse in horse_l:
                if horse['position'] >= 2400:
                    active_horses.append(horse)
                    continue

                dice = roll_dice()
                current_speed = min(horse['actual speed'],6)
                modifiers = rolling_dice[current_speed]
                key = f'speed{dice}'
                modified_speed = modifiers[key]

                if modified_speed  == 'DQ':
                    print(f"Horse {horse['horse']} disqualified on turn {turn}")
                    horse['disqualified'] = True
                    horse['position'] = -1
                    continue

                adjusted_speed = dice + modified_speed
                adjusted_speed = max(1, min(adjusted_speed, 6))

                distance = base_speed[adjusted_speed]
                horse['actual speed'] = adjusted_speed
                horse['position'] += distance
                if horse['position'] >= 2400 and horse['finish'] is None:
                    horse['finish'] = turn
                horse['history'].append(distance)

                active_horses.append(horse)

        horse_l = active_horses
        display_race(horse_l)

    ranking = sorted(
        horse_l,
        key=lambda horse: (
            horse['finish'] if horse['finish'] is not None else float('inf'),
            -horse['position']
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
    print('================       Race Finished!       =================')
    print('=============================================================\n')
    print('-----------------Final Ranking-----------------')
    medals = ['🥇', '🥈', '🥉']
    for index, horse in enumerate(rank[:type_of_c]):
        if horse['finish'] is not None:
            time_in_second = horse['finish'] * 10
            minutes = time_in_second //60
            secondes = time_in_second % 60
            formatted_time = f"{minutes}m {secondes:02}s"
        else:
            formatted_time = "Did Not Finished"

        # We attribut medals to the first 3
        medal = medals[index] if index < len(medals) else ''
        print(f'{index + 1:2}. Horse {horse["horse"]:2} → Position: {horse["position"]:4}m → Time: {formatted_time}  {medal} ')


def main():
    """
    This is the main function.
    :return:
    """
    while True:
        number_of_horses = int(input("How many horses do you want to simulate? (12-20): "))
        if 12 <= number_of_horses <= 20:
            break
        else:
            print("That is not a valid choice. Please try again. A number between 12 and 20")

    horse_list = generate_list(number_of_horses)
    k = kind_of_course()
    ranking, total_turns = simulate_course(horse_list)
    print_out(ranking, k,total_turns)


if __name__=='__main__':
    main()