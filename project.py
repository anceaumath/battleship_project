from os import system, name
import string
import re
import pandas
import random
import time

number_of_rows = 10 #(max 26)
number_of_columns = 10
number_of_carriers = 1
number_of_battleships = 1
number_of_cruisers = 2
number_of_submarines = 1
number_of_patrol_boats = 3

boats = {}

carrier_size = 5
battleship_size = 4
cruiser_size = 3
submarine_size = 3
patrol_boat_size = 2

player_board = {}
computer_board = {}
player_radar = {}
player_display = {}

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

FAST = False
ALPHABET = list(string.ascii_uppercase)

def define_boats(number_of_patrol_boats, number_of_submarines, number_of_cruisers, number_of_battleships, number_of_carriers):
    boats["aircraft carrier"] = {"size" : 5, "tag" : "a", "number" : number_of_carriers}
    boats["battleship"] = {"size" : 4, "tag" : "b", "number" : number_of_battleships}
    boats["cruiser"] = {"size" : 3, "tag" : "c", "number" : number_of_cruisers}
    boats["submarine"] = {"size" : 3, "tag" : "s", "number" : number_of_submarines}
    boats["patrol boat"] = {"size" : 2, "tag" : "p", "number" : number_of_patrol_boats}
    return boats

def get_input(prompt):
    looper = True
    while looper == True:
        try:
            looper = False
            string = input(prompt)
            letter = (re.findall(r'\D', string))[0].upper()
            number = int(re.findall(r'\d+', string)[0])
        except IndexError:
            looper = True
    return [letter, number]

def letterbynumber(number, testnumber, number_of_rows):
    if testnumber > number_of_rows or testnumber < 0:
        return False
    else:
        if number == testnumber:
            return ALPHABET[testnumber]
        else:

            return ALPHABET[testnumber]

def numberbynumber(number, testnumber, number_of_columns):
    if testnumber > number_of_columns or testnumber < 1:
        return False
    else:
        if number == testnumber:
            return testnumber
        else:
            return testnumber

def suggestionverifier(bow, sternlist, board):
    bowletternum = ALPHABET.index(bow[0])
    result = []
    for stern in sternlist:
        sternletternum = ALPHABET.index(stern[0])
        if not bow[0] == stern[0]:
            tracker = True
            if bowletternum > sternletternum:
                for number in range(sternletternum + 1, bowletternum + 1):
                    if not board[bow[1]][ALPHABET[number]] == []:
                        tracker = False
                if tracker == True:
                    result.append(stern)
            else:
                for number in range(bowletternum + 1, sternletternum + 1):
                    if not board[bow[1]][ALPHABET[number]] == []:
                        tracker = False
                if tracker == True:
                    result.append(stern)
        else:
            tracker = True
            if bow[1] > stern[1]:
                for number in range(stern[1], bow[1]):
                    if not board[number][bow[0]] == []:
                        tracker = False
                if tracker == True:
                    result.append(stern)
            else:
                for number in range(bow[1] + 1, stern[1] + 1):
                    if not board[number][bow[0]] == []:
                        tracker = False
                if tracker == True:
                    result.append(stern)
    return result

def suggest_placement(boat, board, number_of_columns, number_of_rows):
    length = boats[boat]['size'] - 1
    looper = True
    options = []
    while looper == True:
        point = get_input(f'Where would you like to put this {boat}\'s bow? ')
        letternumber = ALPHABET.index(point[0])
        letter = point[0]
        number = point[1]
        try:
            if not board[number][letter] == []:
                string = get_input('Please enter a valid and empty location ')
                letternumber = ALPHABET.index(string[0]) + 1
                letter = string[0]
                number = string[1]
            else:
                options.append([letterbynumber(letternumber, letternumber + length, number_of_rows), numberbynumber(number, number, number_of_columns)])
                options.append([letterbynumber(letternumber, letternumber - length, number_of_rows), numberbynumber(number, number, number_of_columns)])
                options.append([letterbynumber(letternumber, letternumber, number_of_rows), numberbynumber(number, number + length, number_of_columns)])
                options.append([letterbynumber(letternumber, letternumber, number_of_rows), numberbynumber(number, number - length, number_of_columns)])
                result = []
                for option in options:
                    if not False in option:
                        result.append(option)
                if not result == []:
                    result = suggestionverifier([letter, number], result, board)
                if result == []:
                    string = get_input('That boat won\'t fit there. Please enter a valid and empty location ')
                    letternumber = ALPHABET.index(string[0])
                    letter = string[0]
                    number = string[1]
                else:
                    looper = False
        except (KeyError, IndexError):
            string = get_input('Please enter a valid and empty location ')
            letternumber = ALPHABET.index(string[0])
            letter = string[0]
            number = string[1]
    return [[letter, number], result]

def take_suggestion(boat, board, number_of_columns, number_of_rows):
    tag = suggest_placement(boat, player_board, number_of_columns, number_of_rows)
    options = tag[1]
    bow = tag[0]
    string = ""
    for option in options:
        string = string + option[0] + str(option[1]) + " "
    tracker = False
    choice = get_input(f"Where would you like to position this {boat}'s stern? {string}")
    while tracker == False:
        if choice in options:
            tracker = True
        else:
            choice = get_input(f"Impossible, admiral. Please choose one of these two options: {string}")
    return [bow, choice]

def computer_position(boat, board, number_of_columns, number_of_rows):
    done = False
    while done == False:
        try:
            spaces = []
            for i in range(number_of_rows):
                for n in range(number_of_columns):
                    spaces.append([ALPHABET[i], n + 1])
            length = boats[boat]['size'] - 1
            point = random.sample(spaces, 1)[0]
            spaces.remove(point)
            letternumber = ALPHABET.index(point[0])
            letter = point[0]
            number = point[1]
            looper = True
            options = []
            while looper == True:
                try:
                    if not board[number][letter] == []:
                        point = random.sample(spaces, 1)[0]
                        spaces.remove(point)
                        letternumber = ALPHABET.index(point[0]) + 1
                        letter = point[0]
                        number = point[1]
                    else:

                        options.append([letterbynumber(letternumber, letternumber + length, number_of_rows), numberbynumber(number, number, number_of_columns)])
                        options.append([letterbynumber(letternumber, letternumber - length, number_of_rows), numberbynumber(number, number, number_of_columns)])
                        options.append([letterbynumber(letternumber, letternumber, number_of_rows), numberbynumber(number, number + length, number_of_columns)])
                        options.append([letterbynumber(letternumber, letternumber, number_of_rows), numberbynumber(number, number - length, number_of_columns)])
                        result = []
                        for option in options:
                            if not False in option:
                                result.append(option)
                        if not result == []:
                            result = suggestionverifier([letter, number], result, board)
                        if result == []:
                            point = random.sample(spaces, 1)[0]
                            spaces.remove(point)
                            letternumber = ALPHABET.index(point[0])
                            letter = point[0]
                            number = point[1]
                        else:
                            looper = False
                except (KeyError, IndexError):
                    point = random.sample(spaces, 1)[0]
                    spaces.remove(point)
                    letternumber = ALPHABET.index(point[0])
                    letter = point[0]
                    number = point[1]
            choice = random.sample(result, 1)[0]
            done = True
        except (ValueError):
            pass
    return [[letter, number], choice]

def place_boat(boat, board, number_of_columns, number_of_rows, boat_tag, iscomputer):
    if iscomputer == False:
        placement = take_suggestion(boat, board, number_of_columns, number_of_rows)
    else:
        placement = computer_position(boat, board, number_of_columns, number_of_rows)
        print(placement)
    letter1 = placement[0][0]
    letternum1 = ALPHABET.index(letter1)
    number1 = placement[0][1]
    letter2 = placement[1][0]
    letternum2 = ALPHABET.index(letter2)
    number2 = placement[1][1]
    if number1 == number2:
        if letternum1 > letternum2:
            for letternumber in range(letternum2, letternum1 + 1):
                board[number1][ALPHABET[letternumber]] = boat_tag
        else:
            for letternumber in range(letternum1, letternum2 + 1):
                board[number1][ALPHABET[letternumber]] = boat_tag
    else:
        if number1 > number2:
            for number in range(number2, number1 + 1):
                board[number][ALPHABET[letternum1]] = boat_tag
        else:
            for number in range(number1, number2 + 1):
                board[number][ALPHABET[letternum1]] = boat_tag
    return board

def boats_and_tags(boats):
    result = []
    for key in boats.keys():
        tag = boats[key]["tag"]
        if boats[key]["number"] == 0:
            pass
        elif boats[key]["number"] == 1:
            result.append([key, tag])
        else:
            for number in range(boats[key]["number"]):
                result.append([key, f"{tag}{number + 1}"])
    return result

def set_hitpoints(boats, tags):
    result = []
    for tag in tags:
        for number in range(boats[tag[0]]["size"]):
            result.append(tag[1])
    return result

def create_board(board, number_of_rows, number_of_columns):
    for i in range(number_of_rows):
        line = {}
        for n in range(number_of_columns):
            line[ALPHABET[n]] = []
        board[i + 1] = line
    return board

def player_boat_placement(player_board, tags, number_of_columns, number_of_rows):
    for tag in tags:
        boat = tag[0]
        tag = tag[1]
        print('------------------------------------------------------------------------------------------------')
        print(pandas.DataFrame(player_board))
        player_board = place_boat(boat, player_board, number_of_columns, number_of_rows, tag, False)
    return player_board

def computer_boat_placement(computer_board, tags, number_of_columns, number_of_rows):
    for tag in tags:
        boat = tag[0]
        tag = tag[1]
        computer_board = place_boat(boat, computer_board, number_of_columns, number_of_rows, tag, True)
    return computer_board

board = pandas.DataFrame(data='O', index=range(1,10+1), columns=list('ABCDEFGHIJ'))

def play():
    input=('Hey Player, where are you shooting this time : ')
    if  board.iloc[input[0],input[1]] != 'S' :
                board.iat[input[0], input[1]] = '0'
                print('You hit the water ... Go next try')
    elif board.iloc[input[0],input[1]] == 'S' :
                board.iat[input[0], input[1]] = 'X'
                print('OMG You hit a boat !')
    else :
        print('You managed to miss the ocean, try again with a letter'
              'between A and J and a digit between 0 and 9')

def turn_display(player_radar, player_display):
    clear()
    print(pandas.DataFrame(player_radar), "              Radar")
    print('------------------------------------------------------')
    print(pandas.DataFrame(player_display), "              Your fleet\n\n")

def mid_display(player_radar, player_display):
    print(pandas.DataFrame(player_radar), "              Radar")
    print('------------------------------------------------------')
    print(pandas.DataFrame(player_display), "              Your fleet\n\n")

def quick_display(board):
    print(pandas.DataFrame(board))

def computer_choice(number_of_columns, number_of_rows):
    number = random.randint(1, number_of_columns)
    letternumber = random.randint(1, number_of_rows)
    return [ALPHABET[letternumber - 1], number]

sample_board = {1: {'A': [], 'B': [], 'C': [], 'D': ['c1'], 'E': ['c1'], 'F': ['c1'], 'G': [], 'H': [], 'I': ['b'], 'J': []}, 2: {'A': ['c2'], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': ['b'], 'J': []}, 3: {'A': ['c2'], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': ['b'], 'J': []}, 4: {'A': ['c2'], 'B': [], 'C': ['p1'], 'D': [], 'E': [], 'F': ['p2'], 'G': ['p2'], 'H': [], 'I': ['b'], 'J': []}, 5: {'A': [], 'B': [], 'C': ['p1'], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 6: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 7: {'A': [], 'B': ['p3'], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 8: {'A': [], 'B': ['p3'], 'C': [], 'D': [], 'E': [], 'F': ['s'], 'G': ['s'], 'H': ['s'], 'I': [], 'J': []}, 9: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 10: {'A': [], 'B': ['a'], 'C': ['a'], 'D': ['a'], 'E': ['a'], 'F': ['a'], 'G': [], 'H': [], 'I': [], 'J': []}}



boats = define_boats(number_of_patrol_boats, number_of_submarines, number_of_cruisers, number_of_battleships, number_of_carriers)
tags = boats_and_tags(boats)

if FAST == True:
    player_board = {1: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': 'b', 'H': 'b', 'I': 'b', 'J': 'b'}, 2: {'A': [], 'B': 'c2', 'C': 'p2', 'D': 'p2', 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 3: {'A': [], 'B': 'c2', 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 4: {'A': [], 'B': 'c2', 'C': [], 'D': [], 'E': 'a', 'F': [], 'G': 's', 'H': 's', 'I': 's', 'J': []}, 5: {'A': [], 'B': [], 'C': [], 'D': [], 'E': 'a', 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 6: {'A': [], 'B': [], 'C': [], 'D': [], 'E': 'a', 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 7: {'A': [], 'B': [], 'C': [], 'D': [], 'E': 'a', 'F': [], 'G': [], 'H': 'c1', 'I': 'c1', 'J': 'c1'}, 8: {'A': [], 'B': [], 'C': [], 'D': [], 'E': 'a', 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 9: {'A': [], 'B': 'p1', 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': 'p3', 'I': 'p3', 'J': []}, 10: {'A': [], 'B': 'p1', 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}}
    computer_board = sample_board
else:
    player_board = create_board(player_board, number_of_rows, number_of_columns)
    computer_board = create_board(computer_board, number_of_rows, number_of_columns)
    quick_display(player_boat_placement(player_board, tags, number_of_columns, number_of_rows))
    quick_display(computer_boat_placement(computer_board, tags, number_of_columns, number_of_rows))

player_radar = create_board(player_radar, number_of_rows, number_of_columns)
player_display = player_board

player_hitpoints = (set_hitpoints(boats, tags))
player_trace = trace = list(set(player_hitpoints))
computer_hitpoints = (set_hitpoints(boats, tags))
computer_trace = trace = list(set(player_hitpoints))

player_moves = []
computer_moves = []

#quick_display(player_boat_placement(player_board, tags, number_of_columns, number_of_rows))

def computer_hitpoint_checker(computer_hitpoints, tags, computer_trace):
    for boat in trace:
        if not boat in computer_hitpoints:
            computer_trace.remove(boat)
            for tag in tags:
                if boat == tag[1]:
                    print(f"We've sunk their {tag[0]}!")
                    return computer_trace

def player_hitpoint_checker(player_hitpoints, tags, player_trace):
    for boat in player_trace:
        if not boat in player_hitpoints:
            player_trace.remove(boat)
            for tag in tags:
                if boat == tag[1]:
                    print(f"The enemy has sunk our {tag[0]}")
                    return player_trace

def get_input(prompt):
    string = input(prompt)
    letter = (re.findall(r'\D', string))[0].upper()
    number = int(re.findall(r'\d+', string)[0])
    return [letter, number]

def player_result(computer_board, player_radar, player_answer, computer_hitpoints, player_display):
    number = player_answer[1]
    letter = player_answer[0]
    if computer_board[number][letter] == []:
        player_radar[number][letter] = 'O'
        turn_display(player_radar, player_display)
        print('We missed!')
    else:

        player_radar[number][letter] = 'X'
        turn_display(player_radar, player_display)
        hit = computer_board[number][letter]
        computer_hitpoints.remove(hit[0])
        print("It's a hit!")
    return [player_radar, computer_hitpoints]

def computer_result(player_board, player_radar, computer_answer, player_hitpoints, player_display, tags):
    clear()
    number = computer_answer[1]
    letter = computer_answer[0]
    if player_board[number][letter] == []:
        player_display[number][letter] = 'O'
        print('\nThe enemy missed!\n')
        hit = False
    else:
        hit = player_board[number][letter]
        player_display[number][letter] = "X"
        player_hitpoints.remove(hit)
        hit = True
        for tag in tags:
            if hit == tag[1]:
                print(f"\nThey've hit our {tag[0]}\n")
    return [player_display, player_hitpoints, hit]

def computer_move():
    letter = random.choice('ABCDEFGHIJ')
    number = random.randint(0,9)
    return [letter,number]

def validated_player_move(player_radar):
    valid = False
    player_answer = get_input('Where should we fire? ')
    letter = player_answer[0]
    number = player_answer[1]
    while valid == False:
        try:
            if not player_radar[number][letter] == []:
                player_answer = get_input('Please enter a valid and location ')
                letter = player_answer[0]
                number = player_answer[1]
            else:
                return player_answer
        except (KeyError, IndexError):
            player_answer = get_input('Please enter a valid location ')
            letter = player_answer[0]
            number = player_answer[1]

def wisemove(hit, computer_moves, computer_board):
    hit = computer_moves[-1]
    hitletter = hit[0]
    hitletternum = ALPHABET.index(hit[0])
    hitnum = hit[1]
    upletter = [ALPHABET[hitletternum + 1], hitnum]
    downletter = [ALPHABET[hitletternum - 1], hitnum]
    upnumber = [hitletter, hitnum + 1]
    downnumber = [hitletter, hitnum - 1]
    results = []
    for result in [upletter, downnumber, downletter, upnumber]:
        if not result in computer_moves:
            if computer_board[result[1]][result[0]] == [] or computer_board[result[1]][result[0]] == [r".*"]:
                results.append(result)
    return results


def validated_computer_move(number_of_columns, number_of_rows, computer_moves, lasthit, computer_board):
    valid = False
    while valid == False:
        try:
            if lasthit == True and counter < 10:
                counter = 0
                computer_answer = sample(wisemove(computer_moves, computer_board))
                counter += 1
            else:
                computer_answer = computer_choice(number_of_columns, number_of_rows)
                letter = computer_answer[0]
                number = computer_answer[1]
            if computer_answer in computer_moves:
                pass
            else:
                return computer_answer
        except (KeyError, IndexError):
            pass

def touched_boat (board,move):
    global cruiser_score
    global battleship_score
    global submarine_score
    global carrier_score
    global patrol_score
    for boat,case in boats.items():
        if str(move) in str(case):
            player_radar[player_answer[1]][player_answer[0]]='X'
            player_board[computer_answer[1]][computer_answer[0]]='X'
            if boat=='Cruiser':
                cruiser_score+=1
            elif boat=='Battleship':
                battleship_score+=1
            elif boat=='Submarine':
                submarine_score+=1
            elif boat=='Carrier':
                carrier_score+=1
            elif boat=='Patrol_boat':
                patrol_score+=1
            return print('Well done you have touched a',boat,'!!!\n')

def sunk_boat(x_score):
    global player_score
    global computer_score
    if cruiser_score == len(boats['Cruiser']) or battleship_score == len(boats['Battleship']) or submarine_score == len(boats['Submarine']) or carrier_score == len(boats['Carrier']) or patrol_score == len(boats['Patrol boat']):
        x_score+=1
        return print('Congratulations, you have sunk your first boat !! \n Your score is', x_score)
    else:
        return print ('Needs to continue to play to shoot an entire boat ! \n')

def datadisplay(board):
    df = pandas.DataFrame(data=board)
    return print(df)

def checker(player_hitpoints, computer_hitpoints):
    if player_hitpoints == [] or computer_hitpoints == []:
        return False
    else:
        return True

game_on = True
clear()
hit_tally = []

while game_on:
    zoned_in = False
    mid_display(player_radar, player_display)
    player_answer = validated_player_move(player_radar)
    player_reslt = player_result(computer_board, player_radar, player_answer, computer_hitpoints, player_display)
    player_radar = player_reslt[0]
    computer_hitpoints = player_reslt[1]
    computer_hitpoint_checker(computer_hitpoints, tags, computer_trace)
    print('\n ---- it\'s the enemy\'s turn to fire!-----\n ')
    time.sleep(2)
    computer_answer = validated_computer_move(number_of_columns, number_of_rows, computer_moves, zoned_in, computer_board)
    print(computer_answer)
    time.sleep(1)
    #print('Computer plays: ', computer_answer)
    computer_reslt = computer_result(player_board, player_radar, computer_answer, computer_hitpoints, player_display, tags)
    player_display = computer_reslt[0]
    player_hitpoints = computer_reslt[1]
    lasthit = computer_reslt[2]
    hit_tally.append(lasthit)
    if hit_tally[-1] == True:
        zoned_in = True
    try:
        if hit_tally[-1] == False and hit_tally[-2] == False and hit_tally[-3] == False:
            zoned_in == False
    except IndexError:
        pass
    game_on = checker(player_hitpoints, computer_hitpoints)

if player_hitpoints == []:
    print("we've lost, admiral!")
else:
    print("We've annihilated the enemy, admiral!")


#print(pandas.DataFrame(sample_board))
#print("------------------------------------")
#print(take_suggestion("aircraft carrier", player_board, number_of_columns, number_of_rows))
#quick_display(player_boat_placement(player_board, tags, number_of_columns, number_of_rows))
