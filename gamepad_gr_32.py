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


def decrypt_board(view):
    """function transform state of table from string to list of lists

    parameters
    ----------
    view : the state of the board (str)

    Returns 
    -------
    board : the state of board in the final type list (list)
    """

    board = list()
    line = list()

    for character in view:
        if character != ",":
            line.append(int(character))
        elif character == ",":
            board.append(line)
            line = list()

    board.append(line)

    return board


def show_board(board):
    """show the content of the board in the microbit 

    Parameters
    ----------
    board : the state of the board (str)

    """

    i = 0
    for line in board:
        j = 0
        for column in line:
            microbit.display.set_pixel(j, i, column)
            j += 1
        i += 1


def get_direction():
    """Return the direction after the movement of the micobit

    Returns
    -------
    direction : the direction of the microbit (str)
    """

    direction = "nothing"
    x = microbit.accelerometer.get_x()
    y = microbit.accelerometer.get_y()

    if x > 200:
        direction = "right"
    elif x < -200:
        direction = "left"
    elif y > 200:
        direction = "down"
    elif y < -200:
        direction = "top"
    else:
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
    show_board(decrypt_board(view))

    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction
        radio.send(get_direction())
    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send("drop")
