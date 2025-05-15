import sys
from typing import List, Set, Tuple
#I WROTE ALL THE COMMENTS SO WHEN I REFER TO THIS ASSIGNMENT IN THE FUTURE I CAN IMMEDIETELY UNDERSTAND FUNCTIONALITY!
#ALSO YES I KNOW THE COMMENTS ARE SIMILAR TO WHATS IN THE DOC STRING I WROTE THE COMMENTS FIRST WHILE CODING THEN THE DOC STRING
# I find having the comments in the code after everything done helpful
def get_match_positions(field: List[List[str]]) -> Set[Tuple[int, int]]:
    """
    Scan the board for horizontal or vertical runs of 4 or more matching color blocks e.g.(R,r,R,r).
    This part of the code follows the matching logic presented in the description of Dr Mario
    If a match is found it reports back to the main program like a scout to the commander 
    field : 2D list representing the game field (rows x columns)

    Returns a set of (row,col) coordinates of all matched cells for the purpose of removing them in the main program later.

    """
    rows = len(field)
    cols = len(field[0]) if rows else 0
    #checks the lengths of the fiels row x columns
    matches = set()
    # Horizontal checker, (checks via rows matches)
    for r in range(rows):
        c = 0
        while c < cols:
            if field[r][c] in 'RBYrby':
                #sets all vitamin color symbols to lower case to easily idenitfy matches (Corresponds to the dr mario logic)
                color = field[r][c].lower()
                run = [(r,c)]
                #r will always be in the range of rows -> represents rows
                #c will always be smaller than columns and stops when its equal to collumns -> represents collumns
                #We run this to create coordinates for the purpose of finding matching cells
                c2 = c+1
                while c2 < cols and field[r][c2].lower() == color:
                    run.append((r,c2))
                    c2 += 1
                if len(run) >= 4:
                    matches.update(run)

                c = c2
            else:
                c += 1
    # Vertical checker (checks via column matches)
    for c in range(cols):
        r = 0
        while r < rows:
            #if contains a virus block or a vitamin
            if field[r][c] in 'RBYrby':
                color = field[r][c].lower()
                #so uppercase and lower case are treated the same
                run = [(r,c)]
                #starts a list to collect data on matching cells
                r2 = r+1
                while r2 < rows and field[r2][c].lower() == color:
                    #keep moving down as long as your within the board & there has been a match prior
                    run.append((r2,c))
                    #add the matching cell to run
                    r2 += 1
                if len(run) >= 4:
                    matches.update(run)
                    #if a match of four has been found update the empty set we initialized earlier
                r = r2
            else:
                r += 1
    return matches


def display_field(game: any) -> None:
    """
    Prints the game field to the terminal on screen as output to the user.
    Essentially key factor for allowing the user to see the game.
    Without it nothing would really function.
    Follows Game Logic Listed Below:
    - Highlights matched positions with asterisks (e.g., *R*).
    - Displays the faller using:
        - [C] for falling blocks
        - |C| for landed blocks
    - Draws static cells and viruses.
    - Removes matched cells from the field after displaying.
    - Ends the game or declares level clear based on game state.
    Matched cells are the highest priority since they can be connected to another vitamin 
    so if matching occurs after that other vitamin will have gravity applied to it making it so it does not follow
    the expected logic

    """
    # Get the coordinates of matches from the current field, returned by the function get_match_postions
    matches = get_match_positions(game.field)
    
    # Create a temporary frozen field for display purposes 
    frozen = [row[:] for row in game.field]
    
    # Determine display state of faller
    display_state = None
    if game.faller:
        display_state = game.faller['state']
        fr, fc = game.faller['row'], game.faller['column']
        orient = game.faller['orientation']
        # Check if faller should be displayed as landed
        if display_state == 'falling':
            if orient == 'horizontal':
                if fr+1 >= game.rows or (fr+1 < game.rows and 
                                         (game.field[fr+1][fc] != ' ' or game.field[fr+1][fc+1] != ' ')):
                    display_state = 'landed'
            else:  # Vertical - usually else at the same branching level will always represent the Vertical orientation option of the faller
                if fr+2 >= game.rows or (fr+2 < game.rows and game.field[fr+2][fc] != ' '):
                    display_state = 'landed'

    # Render the field row by row
    for r in range(game.rows):
        line = '|'
        for c in range(game.cols):
            # Handle matched cells (highest priority), aka match drawing, highlights matched cells with asterisks
            if (r, c) in matches:
                line += f'*{game.field[r][c]}*'
                continue
            
            drawn = False
            # Handle active faller
            if game.faller:
                fr, fc = game.faller['row'], game.faller['column']
                cols_pair = game.faller['colors']
                orient = game.faller['orientation']
                
                # Horizontal faller, handles faller drawing
                if orient == 'horizontal' and r == fr and c in (fc, fc+1):
                    idx = c - fc
                    if idx == 0:  # Left piece
                        line += '[' + cols_pair[0] + '-' if display_state == 'falling' else '|' + cols_pair[0] + '-'
                    else:  # Right piece
                        line += '-' + cols_pair[1] + ']' if display_state == 'falling' else '-' + cols_pair[1] + '|'
                    drawn = True
                    
                # Vertical faller, handles faller drawing
                elif orient == 'vertical' and c == fc and r in (fr, fr+1):
                    idx = r - fr
                    if idx == 0:  # Top piece
                        line += '[' + cols_pair[0] + ']' if display_state == 'falling' else '|' + cols_pair[0] + '|'
                    else:  # Bottom piece
                        line += '[' + cols_pair[1] + ']' if display_state == 'falling' else '|' + cols_pair[1] + '|'
                    drawn = True
            
            # Handle static cells, adds - between adjacent static cells
            if not drawn:
                cell = game.field[r][c]
                if cell in 'RBY' and c+1 < game.cols and game.field[r][c+1] in 'RBY':
                    line += f' {cell}-'  # Connected horizontally right
                elif cell in 'RBY' and c-1 >= 0 and game.field[r][c-1] in 'RBY':
                    line += f'-{cell} '  # Connected horizontally left
                elif cell == ' ':
                    line += '   '  # Empty space
                else:
                    line += f' {cell} '  # Single cell or virus
        
        line += '|'
        print(line)
    
    # Print bottom border
    print(' ' + '-' * (game.cols * 3) + ' ')
    
    # Remove matched cells from the game field after displaying
    for r, c in sorted(matches, reverse=True):
        game.field[r][c] = ' '
        
    # Check if level is cleared, we get this when the game over function flags the condition as true
    if game.game_over:
        print('GAME OVER')
        sys.exit(0)
        #if flag was triggerd: since we cannot break since this isnt a loop we use sys.exit to end the program 
    if not matches and not any(cell in 'rby' for row in game.field for cell in row):
        print('LEVEL CLEARED')


def add_virus(game : any, command: str) -> None:
    """
    Adds a virus of a specified color at a specified position in the game field.
    - command (str): A string in the format "V <row> <col> <color>", where
    <row> and <col> are integers and <color> is one of 'r', 'b', or 'y' (lowercase).
    if its not a lower case it returns, if its out of bounds it retuns, generally not following the board rules returns
    """
    parts = command.split()
    if len(parts) != 4:
        return
    try:
        row = int(parts[1])
        col = int(parts[2])
        color = parts[3].lower()
        #checks if it follows the rules of a virus and the general game board
        if color not in 'rby':
            return
        if not (0 <= row < game.rows and 0 <= col < game.cols):
            return
        if game.field[row][col] != ' ':
            return
        #sets the game board with such viruses
        game.field[row][col] = color
    except ValueError:
        return