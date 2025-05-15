# faller.py
# I WROTE ALL THE COMMENTS SO WHEN I REFER TO THIS ASSIGNMENT IN THE FUTURE I CAN IMMEDIETELY UNDERSTAND FUNCTIONALITY! 
#ALSO YES I KNOW THE COMMENTS ARE SIMILAR TO WHATS IN THE DOC STRING I WROTE THE COMMENTS FIRST WHILE CODING THEN THE DOC STRING
# I find having the comments in the code after everything done helpful
def create_faller(game : any, command: str) -> None:
    """
    Initializes a new faller in the game if one does not exist.

    The function takes the parameters of:
    command (str) : essentially user command via string e.g.  'F <color1> <color2>'
    game (DrMario): game instance from a2.py, it is a redudant paramter so I will only define it once

    """
    parts = command.split()
    if len(parts) < 3:
        return
    #if length is less than expected length of 3 then return
    color1 = parts[1]
    color2 = parts[2]
    #indexs the vitamin colors which is the user input taken from command list assigns them to seperate variables
    if game.faller is None:
        middle_col = game.cols // 2 - 1 if game.cols % 2 == 0 else game.cols // 2
        game.faller = {
            'colors': [color1, color2],  # now mutable list
            'row': 1,
            'column': middle_col,
            'orientation': 'horizontal',
            'state': 'falling'
        }
        #creates a dictionary representing the faller
        #if faller does not exist create the faller in the middle column on the first->second row since we index 0
        #Set the colors as a mutable list, set the orientation to horizontal as default, the state as falling

def update_faller(game : any):
    """
    Advances the current faller in the game by one tick.

    If the faller can fall, it falls one row.
    If it cannot fall, then we -> return True 
    if this call stamped the faller into the field dependent on the orientation the vitamins will hav varying directions.
    """
    if not game.faller:
        return False

    f_row  = game.faller['row']
    f_col  = game.faller['column']
    orient = game.faller['orientation']
    left, right = game.faller['colors'] #left and right defined here!
    #sets the fallers characteristics as variables (set from dictionary)

    # determine below positions based on orientation (Horizontal or Vertical)
    if orient == 'horizontal':
        below = [(f_row+1, f_col), (f_row+1, f_col+1)]
    else:
        below = [(f_row+2, f_col)]

    # Checks for anything below the faller
    can_fall = all(
        0 <= r < game.rows and 0 <= c < game.cols and game.field[r][c] == ' '
        for (r, c) in below
    )

    #if it can fall move it down a row
    if can_fall:
        game.faller['row'] += 1
        return False

    # stamp into the field immediately so it becomes part of the static game baord, 
    # left and right are the faller colors (aka left and right were taken by the dict)
    if orient == 'horizontal':
        game.field[f_row][f_col]     = left
        game.field[f_row][f_col + 1] = right
    else:
        game.field[f_row][f_col]     = left
        game.field[f_row + 1][f_col] = right

    #faller is removed
    game.faller = None
    return True


def rotate_faller(game : any, clockwise: bool) -> None:
    """
    Rotate the current faller 90° around its bottom-left anchor, implementing wall kick:
      - Horizontal → Vertical: anchor at the bottom left cell
      - Vertical → Horizontal: anchor is the bottom block
      - Uses a wall kick mechanic if space is blocked
    
      clockwise (bool) : True to rotate clockwise, False for counterclockwise

    """
    if not game.faller:
        return

    # Current state
    f_row = game.faller['row']
    f_col = game.faller['column']
    orient = game.faller['orientation']
    colors = game.faller['colors']
    rows, cols = game.rows, game.cols
    field = game.field

    # HORIZONTAL -> VERTICAL , X this part of the code shifts the orientation of a faller X
    if orient == 'horizontal':
        # Anchor is at bottom-left: (f_row, f_col)
        anchor_r, anchor_c = f_row, f_col
        # Compute new top cell: one row up
        new_top_r, new_top_c = anchor_r - 1, anchor_c
        # Finds the location of the new orientation
        if new_top_r < 0 or field[new_top_r][new_top_c] != ' ':
            return
        #checks for boundaries
        # Commit rotation by now changing the current state of the faller via the dictionary
        game.faller['orientation'] = 'vertical'
        game.faller['row'] = new_top_r
        game.faller['column'] = anchor_c
        left, right = colors
        if not clockwise:
            # CCW: right->top, left->bottom - was used to help depict, now there to remind myself what clockwise means
            game.faller['colors'] = [right, left]
        # CW: left->top, right->bottom (colors unchanged)

    # VERTICAL -> HORIZONTAL  same thing as above but with wall kick mechanic
    else:
        # Anchor is at bottom-left: (f_row+1, f_col)
        anchor_r, anchor_c = f_row + 1, f_col
        # Default target is same anchor
        new_r, new_c = anchor_r, anchor_c
        # Check space to the right
        if not (new_c + 1 < cols and field[new_r][new_c + 1] == ' '):
            # Wall kick: shift left if possible
            kick_c = anchor_c - 1
            if kick_c < 0 or field[anchor_r][kick_c] != ' ' or field[anchor_r - 1][kick_c] != ' ':
                return
            new_c = kick_c
        # Commit rotation
        game.faller['orientation'] = 'horizontal'
        game.faller['row'] = new_r
        game.faller['column'] = new_c
        top, bottom = colors
        if clockwise:
            # CW: bottom->right, top->left
            game.faller['colors'] = [bottom, top]
        # CCW: top->left, bottom->right (colors unchanged)
# The orientation changing ends here


def move_faller(self, direction: int) -> None:
    """
    Moves the ACTIVE faller left or right by one collumn, if within boundaries.

    -Checks for the boundary limits and other obstructions
    -If the faller was landed, but now can fall reverts its state back to 'falling'

    direction (int) : recieved as -1 or +1 dependent on processed user input was a ">" or "<" command
    """
    if not self.faller:
        return
       
    f_row = self.faller['row']
    f_col = self.faller['column']
    orient = self.faller['orientation']
       
    new_col = f_col + direction
       
    # Check if the move is valid or that the faller can even move in the wanted direction
    if new_col < 0:
        return  # Can't move left of the field
       
    if orient == 'horizontal':
        if new_col + 1 >= self.cols:
            return  # Can't move right of the field/obstructed
        if self.field[f_row][new_col] != ' ' or self.field[f_row][new_col + 1] != ' ':
            return  # Path is blocked/obstructed
    else:  # Vertical
        if new_col >= self.cols:
            return  # Can't move right of the field
        if self.field[f_row][new_col] != ' ' or self.field[f_row + 1][new_col] != ' ':
            return  # Path is blocked by something? Essentialy indexes the field to check that
       
    # Move is valid now, update position
    self.faller['column'] = new_col
       
    # Check if the faller was landed but can now fall
    if self.faller['state'] == 'landed':
        below_row = f_row + 1 if orient == 'horizontal' else f_row + 2
        #finds the below rows
        below_cols = [new_col, new_col + 1] if orient == 'horizontal' else [new_col]
           #checks if the faller can fall
        can_fall = (below_row < self.rows and
                    all(c < self.cols and self.field[below_row][c] == ' ' for c in below_cols))
           #if can fall then changes the state to falling
        if can_fall:
            self.faller['state'] = 'falling'
