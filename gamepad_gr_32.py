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
    
def decrypt_board(state):
    """function transform state of table from string to list of lists
    
    parameters
    ----------
    state : the state of the table (str)

    Returns 
    -------
    board : the state of board in the final type list (list)
    """
    board = list()
    el = list()
    for character in state : 
        if character != "," : 
            el.append(int(character))
        elif character == "," :
            board.append(el)
            el = list()
    board.append(el)

    return board 

def show_board(board):
    """function alight cases of the microbit wich have the same coordinate with the state of table
    
    Parameters
    ----------
    board : state of the board (list)
    """
    i = 0
    for line in board :
        j = 0
        for column in line :
            if column > 0 :
                microbit.display.set_pixel(j,i,column)
            j += 1
        i += 1   
            
def get_direction():
    """function return the direction of the acceleremoter in the microbit 
    
    Returns 
    -------
    direction : the direction of the mouvement in the microbit (str)
    """
    direction = "nothing"
    x = microbit.accelerometer.get_x()
    y = microbit.accelerometer.get_y()
        
    if x > 20 :
        direction = "right"
    elif x < -20 : 
        direction = "left"
    elif y > 20 :
        direction = "top"
    elif y < -20 :
        direction = "down"
    else :
        direction = "nothing"                

    return direction

# settings
group_id = 32

# setup radio to receive/send messages
radio.on()
radio.config(group=group_id)
    
# loop forever (until micro:bit is switched off)
while True:
    # get view of the board
    view = get_message()
    
    # clear screen
    microbit.display.clear()
    
    # show view of the board
    board = decrypt_board(view)
    show_board(board)
    
    
    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction       
        radio.send(get_direction())
    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send("drop")