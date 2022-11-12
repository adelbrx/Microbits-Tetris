import math
import random

import radio
import microbit

# definition of functions


def get_message():
    """Wait and return a message from another micro:bit.

    Returns
    -------
    message: message sent by another micro:bit (str)    
    """
    message = None
    while message == None:
        microbit.sleep(250)
        message = radio.receive()

    return message


def create_new_piece(pieces, board):
    """function create a random piece and return this piece and the state of board

    Parameters
    ----------
    pieces : all pieces we can create (dict)
    board : state of the board (list)

    Returns
    -------
    random_piece : the new piece created (list)
    board : state of the board (list)

    """

    random_piece = pieces[random.randint(0, 2)]

    if not is_game_over(random_piece, board):

        for case in random_piece:
            board[case[1]][case[0]] = 5

        return random_piece, board
    else:

        return random_piece, board


def is_game_over(piece, board):
    """function test if it will be a collision after the creation of new piece so it tests 
    if the game is over or not

    Parameters
    ----------
    piece : the piece created (dict)
    board : state of the board (list)

    Return : 
    --------
    is_over : True if it will be a collision after the creation of the new piece (bool)
    """

    is_over = False

    for case in piece:
        if board[case[1]][case[0]] == 9:
            is_over = True

    return is_over


def crypt_board(board):
    """function transforms the state of the board list of lists to a string

    Parameters
    ----------
    board : the state of the board (list)

    Returns
    -------
    result : state of the board after the cryption (str)
    """

    result = ""

    for line in board:
        for column in line:
            result += str(column)
        result += ","

    return result[0:len(result)-1]


def is_collide(direction, piece, board):
    """function test if it will be a collision after the movement or not

    Parameters
    ----------
    direction : the direction of the movement (str)
    piece : the piece created (dict)
    board : state of the board (list)

    Return : 
    --------
    is_piece_collide : True if it will be a collision after the movement of the new piece (bool)
    """

    is_piece_collide = False

    if direction == "left":

        for case in piece:

            if (case[0] == 0) or ((board[case[1]][case[0] - 1] == 9) and not([case[0]-1, case[1]] in piece)):
                is_piece_collide = True

    elif direction == "right":

        for case in piece:

            if (case[0] == 4) or ((board[case[1]][case[0] + 1] == 9) and not([case[0]+1, case[1]] in piece)):
                is_piece_collide = True

    elif direction == "top":

        for case in piece:

            if (case[1] == 0) or ((board[case[1] - 1][case[0]] == 9) and not([case[0], case[1]-1] in piece)):
                is_piece_collide = True

    elif direction == "down":

        for case in piece:

            if (case[1] == 4) or ((board[case[1] + 1][case[0]] == 9) and not([case[0], case[1]+1] in piece)):
                is_piece_collide = True

    return is_piece_collide


def move_left(piece, board):
    """Move the piece to left 

    Parameters
    ----------
    piece : the piece created (dict)
    board : state of the board (list)

    Returns
    -------
    modified_piece : piece after the movement (list)
    board : state of the board (list)   
    """

    modified_piece = list()

    if not is_collide("left", piece, board):

        for case in piece:
            board[case[1]][case[0]] = 0

        for case in piece:
            board[case[1]][case[0]-1] = 5
            modified_piece.append([case[0]-1, case[1]])

        return modified_piece, board
    else:
        modified_piece = piece
        return modified_piece, board


def move_right(piece, board):
    """Move the piece to right 

    Parameters
    ----------
    piece : the piece created (dict)
    board : state of the board (list)

    Returns
    -------
    modified_piece : piece after the movement (list)
    board : state of the board (list)
    """

    modified_piece = list()

    if not is_collide("right", piece, board):

        for case in piece:
            board[case[1]][case[0]] = 0

        for case in piece:
            board[case[1]][case[0]+1] = 5
            modified_piece.append([case[0]+1, case[1]])

        return modified_piece, board
    else:
        modified_piece = piece
        return modified_piece, board


def move_top(piece, board):
    """Move the piece to top 

    Parameters
    ----------
    piece : the piece created (dict)
    board : state of the board (list)

    Returns
    -------
    modified_piece : piece after the movement (list)
    board : state of the board (list)
    """

    modified_piece = list()

    if not is_collide("top", piece, board):

        for case in piece:
            board[case[1]][case[0]] = 0

        for case in piece:
            board[case[1]-1][case[0]] = 5
            modified_piece.append([case[0], case[1]-1])

        return modified_piece, board
    else:
        modified_piece = piece
        return modified_piece, board


def move_down(piece, board):
    """Move the piece to down 

    Parameters
    ----------
    piece : the piece created (dict)
    board : state of the board (list)

    Returns
    -------
    modified_piece : piece after the movement (list)
    board : state of the board (list)
    """

    modified_piece = list()

    if not is_collide("down", piece, board):

        for case in piece:
            board[case[1]][case[0]] = 0

        for case in piece:
            board[case[1]+1][case[0]] = 5
            modified_piece.append([case[0], case[1]+1])

        return modified_piece, board
    else:
        modified_piece = piece
        return modified_piece, board


def drop_piece(piece, board):
    """droping the piece in the board

    Parameters
    ----------
    piece : the piece created (dict)
    board : state of the board (list)

    Returns
    -------
    board : state of the board (list)
    """

    for case in piece:
        board[case[1]][case[0]] = 9

    return board


# settings
group_id = 32

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
piece_0 = [[0, 0]]
piece_1 = [[0, 0], [1, 0]]
piece_2 = [[0, 0], [0, 1]]

pieces = {0: piece_0, 1: piece_1, 2: piece_2}

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner
    new_piece, board = create_new_piece(pieces, board)

    # check if the new piece collides with dropped pieces
    game_is_over = is_game_over(new_piece, board)

    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            radio.send(crypt_board(board))

            # wait until gamepad sends an order
            order = get_message()

            # execute order (drop or move piece)
            if order == "left":
                new_piece, board = move_left(new_piece, board)
            elif order == "right":
                new_piece, board = move_right(new_piece, board)
            elif order == "top":
                new_piece, board = move_top(new_piece, board)
            elif order == "down":
                new_piece, board = move_down(new_piece, board)
            elif order == "drop":
                board = drop_piece(new_piece, board)
                piece_dropped = True
                nb_dropped_pieces += 1
                new_piece = list()
            else:
                pass

        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
microbit.display.show(nb_dropped_pieces)
