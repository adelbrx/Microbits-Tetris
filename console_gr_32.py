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


def create_new_piece(pieces,board):
    """function create a random piece and return this piece and the state of board and if it will be a collision
    
    Parameters
    ----------
    pieces : all pieces we can create (dict)
    board : state of the board (list)

    Returns
    -------
    random_piece : the new piece created (list)
    is_collide : True if it will be a collision after the creation of the new piece (bool)
    board : state of the board (list)
    """
    
    is_collide = False

    random_number = random.randint(8)
    random_piece = pieces[random_number]

    for point in random_piece : 

        if board[point[1]][point[0]] == 9:
            is_collide = True
        else :    
            board[point[1]][point[0]] = 5

       

    return random_piece , is_collide , board  

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
    for line in board :
        for element in line : 
            result += str(element)
        result +=","
    return result[0:len(result)-1]

def drop_piece(piece,board):
    """function change state piece cases on the board state
    
    Parameters
    ----------
    piece : the piece created (list)
    board : the state of the board (list)

    Returns
    -------
    board : the state of board (list)
    """

    for case in piece :
        board[ case[1] ][ case[0] ] = 9
    return board

def left_move_piece(piece,board):
    """function moves piece cases to left on the board state 
    
    Parameters
    ----------
    piece : the piece created (list)
    board : the state of the board (list)

    Returns
    -------
    list_final : list after moving (list)
    board : the state of board (list)
    """
    collision = False
    for case in piece:
        if (case[0] == 0) or (not([case[0]-1 , case[1]] in piece) and board[ case[1] ][ case[0] - 1 ] == 1):
            collision = True

    if not collision : 

        list_final = list()

        for case in piece :
            board[case[1]][case[0]] = 0
            list_final.append([case[0]-1 , case[1]])
            board[case[1]][case[0] - 1] = 5

        return list_final , board   
    else :
        return piece , board        

def right_move_piece(piece,board):
    """function moves piece cases to right on the board state 
    
    Parameters
    ----------
    piece : the piece created (list)
    board : the state of the board (list)

    Returns
    -------
    list_final : list after moving (list)
    board : the state of board (list)
    """
    collision = False
    for case in piece:
        if (case[0] == 4) or (not([case[0] + 1,case[1]] in piece) and board[ case[1] ][ case[0] + 1 ] == 1):
            collision = True
    if not collision : 
        list_final = list()

        for case in piece :
            board[case[1]][case[0]] = 0
            list_final.append([case[0]+1 , case[1]])
            board[case[1]][case[0] + 1] = 5

        return list_final , board  
    else :
        return piece , board        

def top_move_piece(piece,board):
    """function moves piece cases to top on the board state 
    
    Parameters
    ----------
    piece : the piece created (list)
    board : the state of the board (list)

    Returns
    -------
    list_final : list after moving (list)
    board : the state of board (list)
    """
    collision = False

    for case in piece:
        if (case[1] == 0) or (not([case[0],case[1]-1] in piece) and board[ case[1] - 1][ case[0] ] == 1):
            collision = True

    if not collision : 

        list_final = list()
        for case in piece :
            board[case[1]][case[0]] = 0
            list_final.append([case[0] , case[1]-1])
            board[case[1] - 1][case[0]] = 5

        return list_final , board   
    else :
        return piece , board        

def down_move_piece(piece,board):
    """function moves piece cases to down on the board state 
    
    Parameters
    ----------
    piece : the piece created (list)
    board : the state of the board (list)

    Returns
    -------
    list_final : list after moving (list)
    board : the state of board (list)
    """
    collision = False

    for case in piece:
        if (case[1] == 4) or (not([case[0],case[1]+1] in piece) and board[ case[1] + 1][ case[0] ] == 1):
            collision = True

    if not collision : 

        after_move = list()
        for case in piece :
            board[case[1]][case[0]] = 0
            after_move.append([case[0] , case[1]+1])
            board[case[1] + 1][case[0] ] = 5

        return after_move , board 
    else :
        return piece , board        
            
                  
            


# settings
group_id = 32

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
    ]

microbit.display.clear()

piece_0 = [[0,0] , [0,1] , [1,0] , [1,1]]
piece_1 = [[0,0] , [0,1] , [1,0]]
piece_2 = [[0,0] , [1,0] , [1,1]]
piece_3 = [[0,0] , [0,1] , [1,1]]
piece_4 = [[0,1] , [1,0] , [1,1]]
piece_5 = [[0,0] , [0,1]]
piece_6 = [[0,0] , [1,0]]
piece_7 = [[0,0]]

pieces = {0:piece_0 , 1:piece_1 , 2:piece_2 , 3:piece_3 , 4:piece_4 , 5:piece_5 , 6:piece_6 , 7:piece_7}

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner
    new_piece , is_collide , board = create_new_piece(pieces,board)
    
    # check if the new piece collides with dropped pieces
    game_is_over = is_collide
    
    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            radio.send(crypt_board(board))
            
            # wait until gamepad sends an order
            order = get_message()
            
            # execute order (drop or move piece)
            if order == "drop" : 
                board = drop_piece(new_piece,board)
            elif order == "left" :
                new_piece ,board = left_move_piece(new_piece,board)
            elif order == "right" :
                new_piece ,board = right_move_piece(new_piece,board)
            elif order == "top" :
                new_piece ,board = top_move_piece(new_piece,board)
            elif order == "down" :
                new_piece ,board = down_move_piece(new_piece,board)
            else :
                pass
        
        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()
    
# tell that the game is over
microbit.display.scroll('Game is over', delay=100)