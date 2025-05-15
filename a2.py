# a2.py 
#I WROTE ALL THE COMMENTS SO WHEN I REFER TO THIS ASSIGNMENT IN THE FUTURE I CAN IMMEDIETELY UNDERSTAND FUNCTIONALITY AND REUSE CODE!
#ALSO YES I KNOW THE COMMENTS ARE SIMILAR TO WHATS IN THE DOC STRING I WROTE THE COMMENTS FIRST WHILE CODING THEN THE DOC STRING
# I find having the comments in the code after everything done helpful

from game import DrMarioGame

def main() -> None:
    """
    Main function to run the Dr. Mario game simulation. Handles input for the game configuration,
    initializes the game, and processes commands until the game is over or the user exits the loop.
    Takes configurations from user via input of rows, columns, and field type (EMPTY or CONTENTS).
    The game field is displayed after each command, and the game continues until a game-over condition is met.

    """

    #Input handling for game configuration
    rows = int(input())  #  number of rows in the game field
    cols = int(input())  # number of columns in the game field
    config = input().strip()  # configuration type: EMPTY or CONTENTS

    # Read initial field if provided. If EMPTY, set to None. If CONTENTS, read the field from input.

    if config == "EMPTY":
        initial_field = None

    elif config == "CONTENTS":
        initial_field = []
        for _ in range(rows):
            line = input()
            # Purpose of following branches: to trim or pad the input to fit the game field 
            # < -> requirees padding & > -> requires trimming
            if len(line) < cols:
                line = line.ljust(cols)
                #.ljust() pads the string with spaces on the right, essentially filling it to the required length, 
                #In this context, it ensures that the line has exactly `cols` characters so it fits the game field!
            elif len(line) > cols:
                line = line[:cols]
            initial_field.append(list(line))
        # Convert each line to a list of characters
        # This is necessary because the game field is represented as a list of lists of characters.
        # Each character represents a cell in the game field, and we need to ensure that the input is in the correct format.

    else:
        raise ValueError("Invalid configuration line.")
    #raise ValueError if the configuration via input is neither EMPTY nor CONTENTS

    # Initialize game object with the specified rows, columns, and initial field
    # DrMarioGame class is defined in the game.py file
    game = DrMarioGame(rows, cols, initial_field)

    # Dispalys the intial game field
    # This function is defined in the field.py file
    game.display_field()

    # Main input loop, waites and processes commands until the game is over
    # The game continues until the user enters 'Q' to quit or a game-over condition is met.
    while True:
        try:
            cmd = input()
            # The input command is read from the user
            # The command can be a game command (like F, A, B, <, >, V) or an empty string for a tick
        except EOFError:
            break
            
        keep_playing = game.process_command(cmd)
        # The command is processed by the game object if the game is not over
        # The process_command method handles the command and updates the game field accordingly.
        if not keep_playing:
            # If the game over flag is set, display the final game field
            # "Q" command will not display the field
            if game.game_over:
                game.display_field()
                #dispalys the final game field
            # The game is over, exit the loop
            break

        # Otherwise, still playing → draw updated field
        game.display_field()

if __name__ == "__main__":
    main()
    # This is the main entry point of the script. The function main() is called to start the game simulation.
