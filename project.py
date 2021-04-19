from os import system, name
import string
import re
import pandas

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

ALPHABET = list(string.ascii_uppercase)



def define_boats(number_of_patrol_boats, number_of_submarines, number_of_cruisers, number_of_battleships, number_of_carriers):
    boats["aircraft carrier"] = {"size" : 5, "tag" : "a", "number" : number_of_carriers}
    boats["battleship"] = {"size" : 4, "tag" : "b", "number" : number_of_battleships}
    boats["cruiser"] = {"size" : 3, "tag" : "c", "number" : number_of_cruisers}
    boats["submarine"] = {"size" : 3, "tag" : "s", "number" : number_of_submarines}
    boats["patrol boat"] = {"size" : 2, "tag" : "p", "number" : number_of_patrol_boats}
    return boats

def get_input(prompt):
    string = input(prompt)
    letter = (re.findall(r'\D', string))[0].upper()
    number = int(re.findall(r'\d+', string)[0])
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

def suggestionverifier(stern, aftlist, board):
    sternletternum = ALPHABET.index(stern[0])
    result = []
    for aft in aftlist:
        aftletternum = ALPHABET.index(aft[0])
        if not stern[0] == aft[0]:
            tracker = True
            if sternletternum > aftletternum:
                for number in range(aftletternum + 1, sternletternum + 1):
                    print([ALPHABET[number], stern[1]])
                    if not board[stern[1]][ALPHABET[number]] == []:
                        tracker = False
                if tracker == True:
                    result.append(aft)
            else:
                for number in range(sternletternum + 1, aftletternum + 1):
                    print([ALPHABET[number], stern[1]])
                    if not board[stern[1]][ALPHABET[number]] == []:
                        tracker = False
                if tracker == True:
                    result.append(aft)
        else:
            tracker = True
            if stern[1] > aft[1]:
                for number in range(aft[1] + 1, stern[1] + 1):
                    print([stern[0], number])
                    if not board[stern[1]][stern[0]] == []:
                        tracker = False
                if tracker == True:
                    result.append(aft)
            else:
                for number in range(stern[1] + 1, aft[1] + 1):
                    print([stern[0], number])
                    if not board[stern[1]][stern[0]] == []:
                        tracker = False
                if tracker == True:
                    result.append(aft)
    return result

def suggest_placement(boat, board, number_of_columns, number_of_rows):
    length = boats[boat]['size'] - 1
    point = get_input(f'Where would you like to put this {boat}\'s bow? ')
    letternumber = ALPHABET.index(point[0])
    letter = point[0]
    number = point[1]
    looper = True
    options = []
    while looper == True:
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
                    result = suggestionverifier([letter, number], result, player_board)
                if result == []:
                    string = get_input('Please enter a valid and empty location ')
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
    choice = get_input(f"Where would you like to put this {boat}'s stern? {string}")
    while tracker == False:
        if choice in options:
            tracker = True
        else:
            choice = get_input(f"Please choose one of these two options: {string}")
    return [bow, choice]

def place_boat(boat, board, number_of_columns, number_of_rows, boat_tag):
    print('------------------------------------------------------------------------------------------------')
    print(pandas.DataFrame(board))
    placement = take_suggestion(boat, board, number_of_columns, number_of_rows)
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
        player_board = place_boat(boat, player_board, number_of_columns, number_of_rows, tag)
    return player_board


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


def turn_display(board):
    clear()
    print(pandas.DataFrame(board))

def quick_display(board):
    print(pandas.DataFrame(board))

sample_board = {1: {'A': [], 'B': [], 'C': [], 'D': ['c1'], 'E': ['c1'], 'F': ['c1'], 'G': [], 'H': [], 'I': ['b'], 'J': []}, 2: {'A': ['c2'], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': ['b'], 'J': []}, 3: {'A': ['c2'], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': ['b'], 'J': []}, 4: {'A': ['c2'], 'B': [], 'C': ['p1'], 'D': [], 'E': [], 'F': ['p2'], 'G': ['p2'], 'H': [], 'I': ['b'], 'J': []}, 5: {'A': [], 'B': [], 'C': ['p1'], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 6: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 7: {'A': [], 'B': ['p3'], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 8: {'A': [], 'B': ['p3'], 'C': [], 'D': [], 'E': [], 'F': ['s'], 'G': ['s'], 'H': ['s'], 'I': [], 'J': []}, 9: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 10: {'A': [], 'B': ['a'], 'C': ['a'], 'D': ['a'], 'E': ['a'], 'F': ['a'], 'G': [], 'H': [], 'I': [], 'J': []}}
player_board = create_board(player_board, number_of_rows, number_of_columns)
#computer_board = create_board(computer_board, number_of_rows, number_of_columns)
computer_board = sample_board
player_radar = create_board(player_radar, number_of_rows, number_of_columns)
player_display = create_board(player_display, number_of_rows, number_of_columns)

boats = define_boats(number_of_patrol_boats, number_of_submarines, number_of_cruisers, number_of_battleships, number_of_carriers)
tags = boats_and_tags(boats)




#print(pandas.DataFrame(sample_board))
#print("------------------------------------")
#print(take_suggestion("aircraft carrier", player_board, number_of_columns, number_of_rows))
#quick_display(player_boat_placement(player_board, tags, number_of_columns, number_of_rows))
