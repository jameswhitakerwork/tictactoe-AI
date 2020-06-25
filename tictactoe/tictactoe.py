# JetBrains Academy TicTacToe Exercise
# Use the "start user hard" command to play against the optimal mimimax algorithm
from typing import List
import random
from collections import defaultdict


class Board(object):
    def __init__(self):
        self.grid = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]  # Data structure for board
        self.winning_rows = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)]
        ]

    def print_board(self):
        # TODO: reformat to required output
        print("---------")
        print("| " + self.grid[0][0] + " " + self.grid[0][1] + " " + self.grid[0][2] + " |")
        print("| " + self.grid[1][0] + " " + self.grid[1][1] + " " + self.grid[1][2] + " |")
        print("| " + self.grid[2][0] + " " + self.grid[2][1] + " " + self.grid[2][2] + " |")
        print("---------")

    def populate(self, starting_marks: str):
        self.grid[0][0], self.grid[0][1], self.grid[0][2] = starting_marks[0], starting_marks[1], starting_marks[2]
        self.grid[1][0], self.grid[1][1], self.grid[1][2] = starting_marks[3], starting_marks[4], starting_marks[5]
        self.grid[2][0], self.grid[2][1], self.grid[2][2] = starting_marks[6], starting_marks[7], starting_marks[8]

    def add_mark(self, x, y, mark):
        inverse_x = 3 - x
        self.grid[inverse_x][y - 1] = mark

    def get_mark(self, x, y):
        inverse_x = 3 - x
        return self.grid[inverse_x][y - 1]

    def get_winning_player(self):
        """returns X or O if the game is won, otherwise returns None"""
        for i in range(0, 3):
            # check horizontal
            if self.grid[i] == ['X', 'X', 'X']:
                return 'X'
            if self.grid[i] == ['O', 'O', 'O']:
                return 'O'
            # check vertical
            if [self.grid[0][i], self.grid[1][i], self.grid[2][i]] == ['X', 'X', 'X']:
                return 'X'
            if [self.grid[0][i], self.grid[1][i], self.grid[2][i]] == ['O', 'O', 'O']:
                return 'O'
        # check diagonals
        if [self.grid[0][0], self.grid[1][1], self.grid[2][2]] == ['X', 'X', 'X']:
            return 'X'
        if [self.grid[0][0], self.grid[1][1], self.grid[2][2]] == ['O', 'O', 'O']:
            return 'O'
        if [self.grid[2][0], self.grid[1][1], self.grid[0][2]] == ['X', 'X', 'X']:
            return 'X'
        if [self.grid[2][0], self.grid[1][1], self.grid[0][2]] == ['O', 'O', 'O']:
            return 'O'
        return None

    def count_empty_spaces(self):
        empty_spaces = 0
        for row in self.grid:
            for item in row:
                if item == "_":
                    empty_spaces += 1
        return empty_spaces

    def get_random_empty_coords(self):
        # TODO: Use this for easy move logic instead of inside Game
        pass


class Game(object):
    def __init__(self):
        self.board = Board()
        self.state = "Game not finished"
        self.turn = "X"  # X starts by default in TicTacToe
        self.playerX = None
        self.playerO = None
        self.minimax_iterations = int()
        self.start_game()

    def run_menu(self):
        valid_menu_options = ["start", "exit"]
        valid_player_choices = ["user", "easy", "medium", "hard"]
        menu_resolved = False
        while not menu_resolved:
            command = input("Input command: ")
            if command == "exit":
                quit()
            commands = command.split(" ")
            if len(commands) == 3:
                if commands[0] not in valid_menu_options:
                    print("Bad parameters!")
                elif commands[0] == "start":
                    if commands[1] in valid_player_choices and commands[2] in valid_player_choices:
                        self.playerX = commands[1]
                        self.playerO = commands[2]
                        menu_resolved = True
            else:
                print("Bad parameters!")

    def start_prepopulated_game(self):
        first_board = input("Enter cells: ")
        if verify_starting_board(first_board):
            self.board.populate(first_board)
        else:
            self.start_game()
        self.set_turn(first_board)
        self.board.print_board()
        self.game_step()

    def start_game(self):
        while True:
            board = "_________"
            self.board.populate(board)
            self.set_turn(board)
            self.run_menu()
            self.game_step()

    def set_turn(self, first_board):
        x, o = 0, 0
        for mark in first_board:
            if mark == "X":
                x += 1
            elif mark == "O":
                o += 1
        # print("x is " + x + ", O is " + o)
        if (x == o - 1) or (x == o):
            self.turn = "X"
        elif o == x - 1:
            self.turn = "O"
        else:
            print("Board has an invalid starting state.")
            self.start_game()
        # print(self.turn)

    def check_and_set_state(self):
        # TODO: change input to any board, and return state instead of setting it here.
        if self.board.count_empty_spaces() == 0:
            self.state = "Draw"
        elif self.board.get_winning_player() == 'X':
            self.state = "X wins"
        elif self.board.get_winning_player() == 'O':
            self.state = "O wins"
        print(self.state)

    @staticmethod
    def check_state(board):
        if board.count_empty_spaces() == 0:
            return "_"
        elif board.get_winning_player() == 'X':
            return "X"
        elif board.get_winning_player() == 'O':
            return "O"
        else:
            return None

    def change_turn(self):
        # TODO: replace this function with get_other_turn which has more application
        if self.turn == "X":
            self.turn = "O"
        elif self.turn == "O":
            self.turn = "X"

    @staticmethod
    def get_other_turn(turn):
        if turn == "X":
            return "O"
        else:
            return "X"

    def get_easy_move(self):
        # selects a random available square
        valid_move = False
        while not valid_move:
            x = random.randint(1, 3)
            y = random.randint(1, 3)
            if self.board.get_mark(x, y) == "_":
                valid_move = True
        print('Making move level "easy"')
        return x, y

    def get_medium_move(self):
        for row in self.board.winning_rows:
            three_marks = []
            for coords in row:
                three_marks.append(self.board.get_mark(coords[0] + 1, coords[1] + 1))
            move = self.get_medium_move_from_a_row(three_marks)
            if move:
                print([row[move][0] + 1, row[move][1] + 1])
                return [row[move][0] + 1, row[move][1] + 1]
        return self.get_easy_move()

    def get_hard_move(self):
        #  https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
        m, px, py = self.max()
        print("Getting hard move at {}, {}".format(px, py))
        return px, py

    def max(self):
        maxv = -2  # worse than the worst case
        px = None
        py = None
        result = self.check_state(self.board)
        if result == self.get_other_turn(self.turn):
            return -1, 0, 0
        elif result == self.turn:
            return 1, 0, 0
        elif result == "_":
            return 0, 0, 0

        for i in range(1, 4):
            for j in range(1, 4):
                if self.board.get_mark(i, j) == "_":
                    self.board.add_mark(i, j, self.turn)
                    (m, min_i, min_j) = self.min()
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.board.add_mark(i, j, "_")  # set back to empty
        return maxv, px, py

    def min(self):
        minv = 2  # worse than the worst case
        qx = None
        qy = None
        result = self.check_state(self.board)
        if result == self.get_other_turn(self.turn):
            return -1, 0, 0
        elif result == self.turn:
            return 1, 0, 0
        elif result == "_":
            return 0, 0, 0

        for i in range(1, 4):
            for j in range(1, 4):
                if self.board.get_mark(i, j) == "_":
                    self.board.add_mark(i, j, self.get_other_turn(self.turn))
                    (m, max_i, max_j) = self.max()
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.board.add_mark(i, j, "_")  # set back to empty
        return minv, qx, qy

    def get_medium_move_from_a_row(self, row):
        # see if the game can be won
        counter = defaultdict(int)
        for mark in row:
            counter[mark] += 1
        if counter[self.turn] == 2:
            for i in range(len(row)):
                if row[i] == "_":
                    return i  # return index of winning square
        # otherwise see if a loss can be prevented
        elif counter[self.get_other_turn(self.turn)] == 2:
            for i in range(len(row)):
                if row[i] == "_":
                    return i  # return index of saving square
        else:
            return None

    def get_user_input(self):
        input_string = input("Enter the coordinates: ")
        return input_string

    def check_input(self, input_string: str):
        x_y_check = False
        range_check = False
        occupied_check = False
        length_check = False
        coordinates: List[str] = input_string.split(" ")
        if len(coordinates) == 2:
            length_check = True
            if coordinates[0].isdigit() and coordinates[1].isdigit():
                x_y_check = True
                if (coordinates[0] in ["1", "2", "3"]) and (coordinates[1] in ["1", "2", "3"]):
                    y, x = int(coordinates[0]), int(coordinates[1])
                    range_check = True
                    if self.board.get_mark(y, x) == "_":
                        occupied_check = True
                    else:
                        print("This cell is occupied! Choose another one!")
                else:
                    print("Coordinates should be from 1 to 3!")
            else:
                print("You should enter numbers!")
        else:
            print("Please enter two numbers!")
        return x_y_check and range_check and occupied_check and length_check

    @staticmethod
    def checked_input_into_coords(checked_input):
        coordinates: List[str] = checked_input.split(" ")
        y, x = int(coordinates[0]), int(coordinates[1])
        return y, x

    def game_step(self):
        self.check_and_set_state()
        if self.state == "Draw":
            print("Draw!")
            return
        while self.state == "Game not finished":
            if self.turn == "X":
                if self.playerX == "user":
                    input_command = "initial invalid command"
                    while not self.check_input(input_command):
                        input_command = self.get_user_input()
                        coords = self.checked_input_into_coords(input_command)
                elif self.playerX == "easy":
                    coords = self.get_easy_move()
                elif self.playerX == "medium":
                    coords = self.get_medium_move()
                elif self.playerX == "hard":
                    coords = self.get_hard_move()
            if self.turn == 'O':
                if self.playerO == 'user':
                    input_command = "initial invalid command"
                    while not self.check_input(input_command):
                        input_command = self.get_user_input()
                        coords = self.checked_input_into_coords(input_command)
                elif self.playerO == "easy":
                    coords = self.get_easy_move()
                elif self.playerO == "medium":
                    coords = self.get_medium_move()
                elif self.playerO == "hard":
                    coords = self.get_hard_move()
            self.board.add_mark(coords[0], coords[1], self.turn)
            self.board.print_board()
            self.change_turn()
            self.check_and_set_state()


def verify_starting_board(starting_marks):
    valid_characters = ["X", "O", "_"]
    characters_are_valid = True
    for char in starting_marks:
        if char not in valid_characters:
            characters_are_valid = False
    return characters_are_valid and len(starting_marks) == 9


game = Game()
