from os import system, name
import string
import re

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

ALPHABET = list(string.ascii_uppercase)

number_of_rows = 10 #(max 26)
number_of_columns = 10
number_of_carriers = 1
number_of_battleships = 1
number_of_cruisers = 2
number_of_submarines = 1
number_of_patrol_boats = 3

boats = {}

def define_boats(number_of_patrol_boats, number_of_submarines, number_of_cruisers, number_of_battleships, number_of_carriers):
    boats["carrier"] = {"size" : 5, "number" : number_of_carriers}
    boats["battleship"] = {"size" : 4, "number" : number_of_battleships}
    boats["cruiser"] = {"size" : 3, "number" : number_of_cruisers}
    boats["submarine"] = {"size" : 3, "number" : number_of_submarines}
    boats["patrol_boat"] = {"size" : 3, "number" : number_of_patrol_boats}
    return boats

def get_input(prompt):
    string = input(prompt)
    letter = (re.findall(r'\D', string))[0].upper()
    number = int(re.findall(r'\d+', string)[0])
    return [letter, number]

def suggest_placement(boat, board):
    length = boat['size']
    start_point = get_input('Where would you like to put this ship\'s bow? ')
    looper = True
    while looper == True:
        try:
            if not board[start_point[1]][start_point[0]] == []:
                looper == false
                return False
            else:
                return True
                looper == false
        except KeyError:
            string = get_input('Please enter a valid and empty location ')


boats = define_boats(number_of_patrol_boats, number_of_submarines, number_of_cruisers, number_of_battleships, number_of_carriers)

carrier_size = 5
battleship_size = 4
cruiser_size = 3
submarine_size = 3
patrol_boat_size = 2

player_board = {}
computer_board = {}
player_radar = {}
player_display = {}

def create_board(board, number_of_rows, number_of_columns):
    for i in range(number_of_rows):
        line = {}
        for n in range(number_of_columns):
            line[ALPHABET[n]] = []
        board[i + 1] = line
    return board

import pandas
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

def display(board):
    clear()
    for row in board.keys():
        line_display = []
        for column in board[row].keys():
            line_display.append(board[row][column])
        print(line_display)

def datadisplay(board):
    df = pd.DataFrame(data=board)
    print(df)

player_board = create_board(player_board, number_of_rows, number_of_columns)
computer_board = create_board(computer_board, number_of_rows, number_of_columns)
player_radar = create_board(player_radar, number_of_rows, number_of_columns)
player_display = create_board(player_display, number_of_rows, number_of_columns)

sample_board = {1: {'A': [], 'B': [], 'C': [], 'D': ['s'], 'E': ['s'], 'F': ['s'], 'G': [], 'H': [], 'I': ['s'], 'J': []}, 2: {'A': ['s'], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': ['s'], 'J': []}, 3: {'A': ['s'], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': ['s'], 'J': []}, 4: {'A': ['s'], 'B': [], 'C': ['s'], 'D': [], 'E': [], 'F': ['s'], 'G': ['s'], 'H': [], 'I': ['s'], 'J': []}, 5: {'A': [], 'B': [], 'C': ['s'], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 6: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 7: {'A': [], 'B': ['s'], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 8: {'A': [], 'B': ['s'], 'C': [], 'D': [], 'E': [], 'F': ['s'], 'G': ['s'], 'H': ['s'], 'I': [], 'J': []}, 9: {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}, 10: {'A': [], 'B': ['s'], 'C': ['s'], 'D': ['s'], 'E': ['s'], 'F': ['s'], 'G': [], 'H': [], 'I': [], 'J': []}}

