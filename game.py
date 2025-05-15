# game.py
#I WROTE ALL THE COMMENTS SO WHEN I REFER TO THIS ASSIGNMENT IN THE FUTURE I CAN IMMEDIETELY UNDERSTAND FUNCTIONALITY!
#ALSO YES I KNOW THE COMMENTS ARE SIMILAR TO WHATS IN THE DOC STRING I WROTE THE COMMENTS FIRST WHILE CODING THEN THE DOC STRING
# I find having the comments in the code after everything done helpful
from field import display_field, add_virus
from faller import create_faller, rotate_faller, move_faller, update_faller

class DrMarioGame:
    def __init__(self, rows, cols, initial_field=None) -> None:
        """
        Initialize the Dr. Mario game with arguments as follows:
        rows (int): Number of rows in the game field.
        cols (int): Number of columns in the game field.
        initial_field (list of list of str): Optional initial game field configuration.
        If None, the field is initialized to empty spaces.
        """
        self.rows = rows
        self.cols = cols
        self.field = [[' ' for _ in range(cols)] for _ in range(rows)]
        # Initialize the game field with empty spaces if EMPTY was the initial field type
        self.faller = None
        self.game_over = False
        #Flag to indicate if that hthe game over condition has been met
        
        #Implemented to skip gracity in the next tick so gracvity is not applied to the faller during matching
        self.skip_gravity_next = False
        # If CONTENTS was the initial field type, self.field is set to the provided initial field created by the user
        if initial_field:
            for r in range(rows):
                for c in range(cols):
                    self.field[r][c] = initial_field[r][c]

    def display_field(self) -> None:
        """
        Display the current state of the game field. Calls the display_field function from the field module.
        This function is responsible for rendering the game field to the console.
        It uses the display_field function from the field module to print the current state of the game field.
        """
        display_field(self)

    def process_command(self, command: str) -> bool:
        """
        Processes a command from user input and updates the game state accordingly to the rules of the game.
        When a certain command is received, the game state is updated by calling the corresponding function.
        When called the game state is updated and the game field is displayed.
        The command can be one of the following:
        - 'F' followed by a character: Create a new faller of the specified type.
        - 'A': Rotate the current faller clockwise.
        - 'B': Rotate the current faller counterclockwise.
        - '<': Move the current faller left.
        - '>': Move the current faller right.
        - 'V' followed by a character: Add a virus of the specified type to the field.
        - 'Q': Quit the game.
        - '': Update the game state (advance faller, apply gravity, etc.).
        The function returns True if the game should continue, or False if the game over condition is met.
        """
        cmd = command.strip()

        if cmd == 'Q':
            return False
        elif cmd.startswith('F'):
            if self.check_game_over():
                self.game_over = True
            create_faller(self, cmd)
        elif cmd == 'A':
            rotate_faller(self, clockwise=True)
        elif cmd == 'B':
            rotate_faller(self, clockwise=False)
        elif cmd == '<':
            move_faller(self, -1)
        elif cmd == '>':
            move_faller(self, 1)
        elif cmd.startswith('V'):
            add_virus(self, cmd)
        elif cmd == '':
            self.update()
        return True

    def update(self) -> None:
        """
        Update the game state by performing the following actions:
        1) If there’s an active faller, advance it or make it fall by one level if it's not at the bottom.
        2) If we just placed last tick, skip gravity this tick.
        3) Otherwise, do one tick of “static gravity” the fallers 

        Creates a list of boolean values to check if a cell has been visted. Then checks for clusters
        via stack loop and checks if gravity can be applied. 

        """
        # If there is a active faller that was just placed then we skip gravity
        if self.faller:
            just_placed = update_faller(self)
            if just_placed:
                # skip gravity in next tick so orphan blocks stay put till next update
                self.skip_gravity_next = True
            return

        # If we just placed last tick, skip gravity this tick
        if self.skip_gravity_next:
            self.skip_gravity_next = False
            return

        # 3) Otherwise, do one tick of “static gravity” on fallers
        visited = [[False]*self.cols for _ in range(self.rows)]
        #Creates a 2D list, sets a boolean value for each cell in order to track if we have checked it

        for r in range(self.rows):
            for c in range(self.cols):
                #Iterates by row and column
                if not visited[r][c] and self.field[r][c] in 'RBY':
                    #if we have not checked the cell & it contains a vitamin 
                    stack   = [(r,c)]
                    #initiailizes stack as a list of tuple of number of rows and columns
                    cluster = [] #empty list
                    visited[r][c] = True
                    #overwrites boolean value for cell if "visted" aka checked

                    
                    while stack:
                        cr, cc = stack.pop()
                        #gives the next cell to explore
                        cluster.append((cr,cc))
                        #adds the cell to the cluster
                        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                            #explores the 4 adjacent cells: up, left, right and down
                            nr, nc = cr+dr, cc+dc
                            #if a neighbor is inside the grid bounds, not already visted, contains a vitamin cell ->
                            #mark it as visted -> append it to the stack for further exploration, continues until
                            #the full cluster is found
                            if (0 <= nr < self.rows and
                                0 <= nc < self.cols and
                                not visited[nr][nc] and
                                self.field[nr][nc] in 'RBY'):
                                visited[nr][nc] = True
                                stack.append((nr,nc))
                    can_fall = True
                    for cr, cc in cluster:
                        #if the cluster is on the bottom row it means that it can no longer fall and the loop is broken
                        if (cr+1 >= self.rows or
                            (self.field[cr+1][cc] != ' ' and (cr+1,cc) not in cluster)):
                            can_fall = False
                            break
                    if can_fall:
                        #if it passes the previous branch that means it can fall, so the cluster moves down by one row
                        #to the cells directly below them
                        for cr, cc in sorted(cluster, key=lambda x: -x[0]):
                            #key = lambda x: -x[0]: each item x is a (row, col) tuple, x[0] is the row number
                            #by -x[0] we negate it and sort in descending order by row, from the bottom row to top row
                            
                            self.field[cr+1][cc] = self.field[cr][cc]
                            self.field[cr][cc]   = ' '
                        return

    def check_game_over(self) -> bool:
        """
        Creates the flag for the game over condition. Essentially checks if spawning a new faller triggers game over.

        Returns a True or False value dependent on the result. If True the game triggers game over.
        
        """
        #Finds the middle column, checks the first row, if the first row is empty returns False
        
        if self.cols % 2 == 0:
            mid_cols = [self.cols // 2 - 1, self.cols // 2]
        else:
            mid = self.cols // 2 # by finding the int value of dividing by 2 we can find the middle collumn 
            mid_cols = [mid]
        return any(self.field[1][c] != ' ' for c in mid_cols)
    #If not empty returns True signifying it cannot spawn there and the game is over