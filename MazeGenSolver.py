# Import libraries needed
import pygame  # For creating games and interactive graphics
import random  # To generate random numbers
import heapq   # For implementing heap queue algorithms

# Initialise pygame and set the clock
pygame.init()  # Initialise all imported pygame modules
clock = pygame.time.Clock()  # Create a clock object to manage frame rate

# Let the user input their desired maze dimensions
rows = int(input('enter an odd number to be the width and height of the maze'))  # User input for number of rows in the maze
cellSize = int(input('enter the size you would like for each maze cell'))  # User input for the size of each cell

# Calculate screen dimensions and create a display
screenWidth = rows * cellSize  # Compute screen width
screenHeight = screenWidth  # Screen height is equal to the width for a square layout
screenSize = (screenWidth, screenHeight)  # Tuple representing screen size
screen = pygame.display.set_mode(screenSize)  # Initialise window for display
columns = rows  # Number of columns is equal to the number of rows
print("dimensions", rows, columns)  # Print out the dimensions for confirmation



# Define a series of color constants using RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
YELLOW = (255, 255, 0)
GREY = (143, 143, 143)
BROWN = (186, 127, 50)
DARK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
DARK_BLUE = (0, 0, 128)

# Construct Cell object to store each cell's coordinates and details
class Cell:
    def __init__(self, row, col):
        self.__row = row  # Row position of the cell
        self.__col = col  # Column position of the cell
        self.__is_wall = True  # Is the cell a wall?
        self.__is_route = False  # Is the cell part of the route?
        self.__is_start = False  # Is the cell the starting point?
        self.__is_end = False  # Is the cell the ending point?
        self.__is_heavy = False  # Does the cell have a heavy weight?
        self.__is_visit = False  # Has the cell been visited?
        self.__is_player = False # Is the cell occupied by the player?
        self.__is_enemy = False # Is the cell occupied by the enemy?

    # Getter and setter methods for these attributes
    def get_row(self):
        return self.__row
    
    def get_col(self):
        return self.__col
    
    def set_row(self, input):
        self.__row = input
        return
    
    def set_col(self, input):
        self.__col = input
        return
    
    def get_is_wall(self):
        return self.__is_wall
    
    def get_is_route(self):
        return self.__is_route
    
    def set_is_wall(self, input):
        self.__is_wall = input
        return
    
    def set_is_route(self, input):
        self.__is_route = input
        return
    
    def get_is_start(self):
        return self.__is_start
    
    def get_is_end(self):
        return self.__is_end
    
    def set_is_start(self, input):
        self.__is_start = input
        return
    
    def set_is_end(self, input):
        self.__is_end = input
        return
    def get_is_heavy(self):
        return self.__is_heavy
    
    def get_is_visit(self):
        return self.__is_visit
    
    def set_is_heavy(self, input):
        self.__is_heavy = input
        return
    
    def set_is_visit(self, input):
        self.__is_visit = input
        return
    
    def get_is_player(self):
        return self.__is_player
    
    def get_is_enemy(self):
        return self.__is_enemy
    
    def set_is_player(self, input):
        self.__is_player = input
        return
    
    def set_is_enemy(self, input):
        self.__is_enemy = input
        return

    # For cells with different attributes, colour them differently
    def draw(self, screen):
        x = self.__row * cellSize 
        y = self.__col * cellSize
        cell_rect = pygame.Rect(x, y, cellSize, cellSize)
        if self.__is_wall:
                pygame.draw.rect(screen, BLACK, cell_rect)
        elif self.__is_route:
                pygame.draw.rect(screen, YELLOW, cell_rect)
        elif self.__is_enemy:
                pygame.draw.rect(screen, RED, cell_rect)
        elif self.__is_player:
                pygame.draw.rect(screen, YELLOW, cell_rect)
        elif self.__is_start:
            pygame.draw.rect(screen, GREEN, cell_rect)
        elif self.__is_end:
            pygame.draw.rect(screen, BLUE, cell_rect)
        else:                
            if self.__is_heavy and self.__is_visit:
                pygame.draw.rect(screen, PURPLE, cell_rect)
            elif self.__is_visit:
                pygame.draw.rect(screen, LIGHT_BLUE, cell_rect)
            elif self.__is_heavy:
                pygame.draw.rect(screen, BROWN, cell_rect)
            else:
                pygame.draw.rect(screen, WHITE, cell_rect)

            
# Construct Maze object to have a grid which stores each Cell object
class Maze:
    def __init__(self, rows, columns):
        self.__rows = rows # The number of rows in the maze
        self.__columns = columns # The number of columns in the maze
        self.__grid = [[Cell(row,col) for col in range(self.__columns)] for row in range(self.__rows)] # The grid of cell objects

    # Getter and setter methods for each private attribute
    def get_cell(self, x, y):
        return self.__grid[x][y] 
    
    

    def draw(self, screen): 
        for row in range(self.__rows):
            for col in range(self.__columns):
                cell = self.__grid[row][col]
                cell.draw(screen)
    
    def reset(self):
        for row in range(self.__rows):
            for col in range(self.__columns):
                cell = self.__grid[row][col]
                cell.set_is_start(False)
                cell.set_is_end(False)
                cell.set_is_route(False)
                cell.set_is_heavy(False)
                cell.set_is_visit(False)
                cell.set_is_player(False)
                cell.set_is_enemy(False)
                cell.set_is_wall(True)
                
        set.clear(generator.generated)
        set.clear(solution.visited)
        self.draw(screen)
        solution.startcell = (0,0)
        solution.endcell = (0,0)
        player.set_row(0)
        player.set_col(0)
        player.set_power1(3)
        player.set_power2(3)
        enemy.row, enemy.col = 0,0
        pygame.display.flip()


# Create a Generator class which stores the generation methods
class Generator:
    def __init__(self, maze):
        self.maze = maze  # Stores a reference to the maze object
        self.generated = set()  # A list to store cells that are already generated

    # Method to generate the entire maze
    def generate(self):
        # Choose a random cell from the perimeter to start generation
        startCell = random.choice(self.get_perimeter_cells())
        # Make the start cell an open space
        self.maze.get_cell(startCell[0], startCell[1]).set_is_wall(False)

        # Initialise a list to keep track of adjacent cells
        adjacents = []
        # Set the current cell to the starting cell
        currentcell = startCell 
        # Get the adjacent cells for the current cell
        adjacents = self.get_adjacent_cells(currentcell, adjacents, self.generated)
        
        # Continue the loop as long as there are adjacent cells to process
        while adjacents:
            # Update the list of adjacent cells for the current cell
            adjacents = self.get_adjacent_cells(currentcell, adjacents, self.generated)

            # Choose a random cell from the list of adjacent cells
            chosenCell = random.choice(adjacents)

            
            print("chosen cell", chosenCell[0], chosenCell[1]) # Print message for debugging

            # Make chosen cell a passage
            self.maze.get_cell(chosenCell[0], chosenCell[1]).set_is_wall(False)
            # Add the current cell to the set of generated cells
            self.generated.add(currentcell)
            # Draw the updated maze state and update the display
            self.maze.draw(screen)
            pygame.display.flip()
            
            wall = self.get_wall(chosenCell, self.generated) # Get a wall cell adjacent to the chosen cell to remove
            self.maze.get_cell(wall[0], wall[1]).set_is_wall(False)
            self.generated.add(wall) # Add the wall cell to the set of generated cells

            # Redraw and update the display
            self.maze.draw(screen)
            pygame.display.flip()

            # Add the chosen cell to the set of generated cells
            self.generated.add(chosenCell)
            # Redraw and update the display
            self.maze.draw(screen)
            pygame.display.flip()

            print("cc", currentcell[0], currentcell[1]) # Print message for debugging

            # Remove already generated cells from the list of adjacent cells
            for cell in adjacents:
                if cell in self.generated:
                    adjacents.remove(cell)

            # Update the current cell to be the chosen cell
            currentcell = chosenCell
            print("nextc", currentcell[0], currentcell[1]) # Print message for debugging
        
        
        print('generator finished') # Print message for debugging

    # Method to get all perimeter cells in the maze
    def get_perimeter_cells(self):
        perimeterCells = []
        # Adding cells from the first and last columns, skipping one cell each time
        for col in range(1, columns - 1, 2):
            perimeterCells.append((1, col))  # Add cells from the top row
        for col in range(1, columns - 1, 2):
            perimeterCells.append((rows - 2, col))  # Add cells from the bottom row
        # Adding cells from the first and last rows, skipping one cell each time
        for row in range(3, rows - 2, 2):
            perimeterCells.append((row, 1))  # Add cells from the left column
        for row in range(3, rows - 2, 2):
            perimeterCells.append((row, columns - 2))  # Add cells from the right column
        
        # Get a list of the perimeter cells that aren't occupied
        for cell in perimeterCells:
            checkedcell = self.maze.get_cell(cell[0], cell[1]) 
            if checkedcell.get_is_start() or checkedcell.get_is_end() or checkedcell.get_is_enemy(): 
                continue
            else:
                perimeterCells.remove(cell)

        return perimeterCells  # Return the list of perimeter cells

    # Method to get a list of adjacent cells to a given cell
    def get_adjacent_cells(self, currentcell, adjacentlist, visited):
        translations = [(0,-2), (0,2), (-2,0), (2,0)]  # Directions to check for adjacent cells
        for translate in translations:
            row = currentcell[0] + translate[0]
            col = currentcell[1] + translate[1]
            # Check if the adjacent cell is within maze boundaries and is a wall and not visited
            if 0 <= row < rows and 0 <= col < columns and self.maze.get_cell(row,col).get_is_wall() == True and (row,col) not in visited:  
                adjacentlist.append((row, col))  # Add the cell to the list of adjacent cells
            else:
                print('get adj error or finished or first cell') # Print message for debugging
        return adjacentlist  # Return the list of adjacent cells

    # Method to remove the wall between adjacent cells and the current cell
    def get_wall(self, adjacentcell, visited):
        availablecells = [] # Array to contain available cells
        translations = [(0,-2), (0,2), (-2,0), (2,0)]  # Directions to check for available cells
        for translate in translations:
            row = adjacentcell[0] + translate[0]
            col = adjacentcell[1] + translate[1]
            # Check if the cell is in the list of visited cells
            if (row,col) in visited:
                availablecells.append((row,col))  # Add the cell to the list of available cells
                print("length of available cells", len(availablecells)) # Print message for debugging
        # If there are available cells, choose one at random and return the wall to be removed
        if availablecells:
            mazecell = random.choice(availablecells)
            wall = (((mazecell[0] + adjacentcell[0]) // 2), ((mazecell[1] + adjacentcell[1]) // 2))
            return wall
        else:
            return 

# Class to store solution methods
class Solution:
    # Constructor for the Solution class
    def __init__(self, maze):
        self.maze = maze # Stores a reference to the maze object
        self.visited = set()  # Set to keep track of visited cells
        self.startcell = (0,0)  # Coordinates for the starting cell
        self.endcell = (0,0)  # Coordinates for the ending cell

    # Method to create start and end cells if they don't already exist
    def createstartend(self):
        srow, scol = self.startcell
        erow, ecol = self.endcell
            

        # Create start and/or end cells based on their current state
        if self.startcell == (0,0) and self.endcell == (0,0):
            self.createstart()
            self.createend()
        elif self.startcell == (0,0) and self.endcell != (0,0):
            self.createstart()
        elif self.startcell != (0,0) and self.endcell == (0,0):
            self.createend()
        self.draw_endings()
        
        # Update the maze grid with start and end cells
        self.maze.get_cell(srow,scol).set_is_start(False)
        self.maze.get_cell(self.startcell[0],self.startcell[1]).set_is_start(True)
            
        # Update the player's position in the maze
        self.maze.get_cell(player.get_row(), player.get_col()).set_is_player(False)
        player.set_row(self.startcell[0]), player.set_col(self.startcell[1])
        self.maze.get_cell(self.startcell[0], self.startcell[1]).set_is_player(True)
        # Reset the uses of each player's powers
        player.set_power1(3)
        player.set_power2(3)
        player.set_finished(False)

        # Update the end cell in the maze
        self.maze.get_cell(erow,ecol).set_is_end(False)
        self.maze.get_cell(self.endcell[0],self.endcell[1]).set_is_end(True)
        # Update the screen
        self.maze.draw(screen)
        pygame.display.update()

    # Method to draw the shortest path from the end cell to the start cell
    def reconstruct_path(self, startcell, currentcell, cameFrom):
        total_path = []
        currentcell = cameFrom[currentcell]
        while currentcell != startcell:
            self.draw_pathcell(currentcell)
            total_path.append(currentcell)
            currentcell = cameFrom[currentcell]
    
    # Method to use A* pathfinding logic to find the shortest path from start to end cell
    def A_star(self):
        open_set = []  # Priority queue to keep track of cells to be evaluated and shorter paths will have a higher priority.
        cameFrom = {}  # Dictionary to track solution cells and the cell before it

        self.createstartend()
        
        # Initializing cost values for each cell
        g, h, f = {}, {}, {}
        works = False
        for row in range(rows):
            for col in range(columns):
                cell = (row, col)
                g[cell] = float('inf')  # Cost from start to a node
                h[cell] = self.manhattan_distance(self.startcell, self.endcell)  # Heuristic cost estimate from node to end
                f[cell] = g[cell] + h[cell]  # Total cost of node

        # Setting start cell costs
        g[self.startcell] = 0
        f[self.startcell] = g[self.startcell] + h[self.startcell]

        heapq.heappush(open_set, (0, self.startcell))  # Adding start cell to open set
        self.visited.add(self.startcell) # Add cell to visited set

        # A* Algorithm implementation
        while open_set:
            print('solving start') # Print message for debugging
            _, currentcell = heapq.heappop(open_set)  # Get the cell with the lowest f-score from the queue
            print(currentcell) # Print message for debugging
            
            # Check if the current cell is the end cell
            if currentcell == self.endcell:
                print('current is end') # Print message for debugging
                self.reconstruct_path(self.startcell, currentcell, cameFrom)  # Call the method to reconstruct the path found
                works = True # Update the flag
                break # Leave the while loop

            else:
                # Process each neighbour of the current cell
                for neighbour in self.neighbours(currentcell):
                    self.visited.add(neighbour) # Add neighbour cell to visited set
                    self.show_cell_visited(neighbour)  # Call method to display this cell as visited using colour
                    tentative_g = g[currentcell] + self.weight(neighbour)  # Calculate tentative G cost
                    if tentative_g < g[neighbour]:  # Check if this path to neighbor is better than any previously recorded path
                        cameFrom[neighbour] = currentcell  # Record the path
                        print('next cell working')  # Debug message
                        g[neighbour] = tentative_g  # Update G cost
                        f[neighbour] = g[neighbour] + h[neighbour]  # Update F cost (G + H)

                        # If the neighbor is not in the open set, add it
                        if neighbour not in open_set:
                            heapq.heappush(open_set, (f[neighbour], neighbour))

        # Check if the algorithm found a path using the flag
        if works == True:
            print('works')  # Debug message indicating success
            open_set = []  # Clear open set
            cameFrom = {}  # Clear path history
        else:
            print('failure')  # Debug message indicating failure

    # Method to visually indicate cells that have been visited during pathfinding
    def show_cell_visited(self, cell):
        row, col = cell
        self.maze.get_cell(row,col).set_is_visit(True)  # Mark the cell as visited
        self.maze.draw(screen)  # Redraw the maze
        pygame.display.flip()  # Update the display
        print('cell shown')  # Debug message

    # Method to visually indicate the start and end cells in the maze
    def draw_endings(self):
        # Mark start and end cells in the grid
        self.maze.get_cell(self.startcell[0],self.startcell[1]).set_is_start(True)
        self.maze.get_cell(self.endcell[0],self.endcell[1]).set_is_end(True)
        self.maze.draw(screen)  # Redraw the maze with start and end cells coloured
        pygame.display.flip()  # Update the display

    # Method to assign a weight to a cell, used in pathfinding calculations
    def weight(self, neighbour):
        # Heavier weight for cells marked as 'heavy', affecting pathfinding
        if self.maze.get_cell(neighbour[0],neighbour[1]).get_is_heavy():
            return 10  # Assign a high weight
        else:
            return 1  # Assign a normal weight

    # Method to visually indicate the path found by the pathfinding algorithm
    def draw_pathcell(self, cell):
        self.maze.get_cell(cell[0],cell[1]).set_is_route(True)  # Mark the cell as part of the route
        self.maze.draw(screen)  # Redraw the maze
        pygame.display.flip()  # Update the display

    # Method to get a list of neighboring cells of a given cell
    def neighbours(self, cell):
        neighbours = []  # List to store neighboring cells
        translations = [(1,0), (0,1), (-1,0), (0,-1)]  # Possible moves (right, down, left, up)
        for translate in translations:
            # Calculate neighbor cell coordinates
            row = cell[0] + translate[0]
            col = cell[1] + translate[1]
            # Check if neighbor is within maze bounds and not a wall
            if 0 <= row < rows and 0 <= col < columns and not self.maze.get_cell(row,col).get_is_wall():
                neighbours.append((row, col))  # Add the cell to the neighbors list
        return neighbours
    
    # Method to create a starting point for the maze
    def createstart(self):
        # Randomly select a cell from the perimeter as the starting cell
        self.startcell = random.choice(generator.get_perimeter_cells())
        # Ensure that the selected cell is not a wall
        while self.is_wall(self.startcell): 
            print('instart')  # Debug message indicating the process of finding a start cell
            self.startcell = random.choice(generator.get_perimeter_cells())
        return  # End of the method

    # Method to create an end point for the maze
    def createend(self):
        # Randomly select a cell from the perimeter as the ending cell
        self.endcell = random.choice(generator.get_perimeter_cells())
        # Ensure that the selected cell is not a wall and not the same as the start cell
        while self.is_wall(self.endcell) or self.endcell == self.startcell:
            print('inend')  # Debug message indicating the process of finding an end cell
            self.endcell = random.choice(generator.get_perimeter_cells())
        return

    # Method to calculate the Manhattan distance between two cells
    def manhattan_distance(self, cell, endcell):
        # Manhattan distance is a heuristic, the sum of the differences in the x and y coordinates
        distance = abs(cell[0] - endcell[0]) + abs(cell[1] - endcell[1])
        return distance

    # Method to check if a given cell is a wall
    def is_wall(self, cell):
        # Return True if the cell is a wall, False otherwise
        if self.maze.get_cell(cell[0],cell[1]).get_is_wall():
            return True
        elif not self.maze.get_cell(cell[0],cell[1]).get_is_wall():
            return False

    # Method to clear the solution path and visited cells
    def clear_solution(self):
        # Iterate through all cells in the grid
        for row in range(rows):
            for col in range(columns):
                # Clear all visited and path cells
                if self.maze.get_cell(row,col).get_is_visit():
                    self.maze.get_cell(row,col).set_is_visit(False)
                if self.maze.get_cell(row,col).get_is_route():
                    self.maze.get_cell(row,col).set_is_route(False)
                
        # Remove the enemy
        self.maze.get_cell(enemy.get_row(), enemy.get_col()).set_is_enemy(False)
        enemy.set_row(0), enemy.set_col(0)

        

        # Reset player's position to the start cell
        self.maze.get_cell(solution.endcell[0], solution.endcell[1]).set_is_player(False)
        
        player.set_row(solution.startcell[0]), player.set_col(solution.startcell[1])

        self.maze.get_cell(player.get_row(), player.get_col()).set_is_player(True)
        self.maze.draw(screen)  # Redraw the maze
        pygame.display.flip()  # Update the display
        set.clear(self.visited)  # Clear the set of visited cells
        return
            
# Player class to manage the player's character in the maze
class Player:
    # Constructor method to create the player
    def __init__(self, maze, row, col):
        self.__row = row  # Player's current row
        self.__col = col  # Player's current column
        self.maze = maze  # Stores a reference to the maze object
        self.__finished = True  # Flag to check if the player has finished
        self.__power1 = 3  # First power uses 
        self.__power2 = 3  # Second power uses

    def get_row(self):
        return self.__row
    
    def get_col(self):
        return self.__col
    
    def set_row(self, input):
        self.__row = input
        return
    
    def set_col(self, input):
        self.__col = input
        return
    
    def get_finished(self):
        return self.__finished

    def set_finished(self, input):
        self.__finished = input
        return
    
    def get_power1(self):
        return self.__power1
    
    def get_power2(self):
        return self.__power2
    
    def set_power1(self, input):
        self.__power1 = input
        return
    
    def set_power2(self, input):
        self.__power2 = input
        return

    # Method to check if the player has reached the end cell
    def checkfinish(self):
        if (self.__row, self.__col) == solution.endcell:
            self.__finished = True  # Set finished flag to True
            solution.A_star()  # Recalculate the path
            self.maze.get_cell(self.__row, self.__col).set_is_player(False) # Remove the player
            self.__row = 0  # Reset player's row
            self.__col = 0  # Reset player's column
            self.__power1 = 3  # Update power level
            self.__power2 = 3 # Update power level
            return
        if (self.__row, self.__col) == enemy.enemy():
            solution.clear_solution()
    
    # Method to create an 'oil spill' effect around the player
    def oilspill(self):
        # Coordinates around the player to affect
        coordinates = [(2,-2),(2,-1),(2,0),(2,1),(2,2),(1,-2),(1,-1),(1,0),(1,1),(1,2),(0,-2),(0,-1),(0,0),(0,1),(0,2),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2)]
        for coord in coordinates:
            oilcell = (self.__row + coord[0], self.__col + coord[1])
            # Mark cells as 'heavy' if they fall within the maze bounds
            if oilcell[0] < rows and oilcell[0] > 0 and oilcell[1] > 0 and oilcell[1] < columns:
                self.maze.get_cell(oilcell[0],oilcell[1]).set_is_heavy(True)
        self.__power1 -= 1
        self.maze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display

    # Method to simulate an explosion around the player
    def explode(self):
        # Coordinates around the player to affect
        coordinates = [(1,-1),(1,0),(1,1),(0,-1),(0,0),(0,1),(-1,-1),(-1,0),(-1,1)]
        for coord in coordinates:
            clearedcell = (self.__row + coord[0], self.__col + coord[1])
            # Clear walls in the affected cells
            if clearedcell[0] != 0 and clearedcell[0] != rows and clearedcell[1] != 0 and clearedcell[1] != columns:
                self.maze.get_cell(clearedcell[0], clearedcell[1]).set_is_wall(False)
        self.__power2 -= 1
        self.maze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display

    # Method to move the player to the right
    def moveright(self):
        moveto = self.maze.get_cell(self.__row + 1,self.__col)  # Cell to move to
        current = self.maze.get_cell(self.__row,self.__col)   # Current cell
        # Check if the cell to the right is not a wall
        if not moveto.get_is_wall():

            self.__row += 1  # Update player's row
            enemy.checkcaught() # Check if the player moved into the enemy
            current.set_is_player(False)  # Mark current cell as not having the player
            moveto.set_is_player(True)  # Mark the next cell as having the player
            
            self.checkfinish()  # Check if the player has finished
            
            self.maze.draw(screen)  # Redraw the maze
            pygame.display.update()  # Update the display
        
    # Method to move the player to the left
    def moveleft(self):
        moveto = self.maze.get_cell(self.__row - 1,self.__col)  # Cell to move to
        current = self.maze.get_cell(self.__row,self.__col)   # Current cell
        # Check if the cell to the left is not a wall
        if not moveto.get_is_wall():
            self.__row -= 1  # Update player's row
            enemy.checkcaught() # Check if the player moved into the enemy
            current.set_is_player(False)  # Mark current cell as not having the player
            moveto.set_is_player(True)  # Mark the next cell as having the player
            
            self.checkfinish()  # Check if the player has finished
            
            self.maze.draw(screen)  # Redraw the maze
            pygame.display.update()  # Update the display

    # Method to move the player up
    def moveup(self):
        moveto = self.maze.get_cell(self.__row,self.__col - 1)  # Cell to move to
        current = self.maze.get_cell(self.__row,self.__col)  # Current cell
        # Check if the cell above is not a wall
        if not moveto.get_is_wall():
            self.__col -= 1 # Update player's column
            enemy.checkcaught() # Check if the player moved into the enemy
            current.set_is_player(False) # Mark current cell as not having the player
            moveto.set_is_player(True) # Mark the next cell as having the player
            
            self.checkfinish() # Check if the player has finished
            
            self.maze.draw(screen) # Redraw the maze
            pygame.display.update() # Update the display

    # Method to move the player down
    def movedown(self):
        moveto = self.maze.get_cell(self.__row,self.__col + 1)  # Cell to move to
        current = self.maze.get_cell(self.__row,self.__col) # Current cell
        # Check if the cell below is not a wall
        if not moveto.get_is_wall():
            self.__col += 1 # Update player's col
            enemy.checkcaught() # Check if the player moved into the enemy
            current.set_is_player(False) # Mark current cell as not having the player
            moveto.set_is_player(True) # Mark the next cell as having the player
            
            self.checkfinish() # Check if the player has finished
            
            self.maze.draw(screen) # Redraw the maze
            pygame.display.update() # Update the display



# Class for managing enemy character in the maze
class Enemy:
    # Constructor for the Enemy class
    def __init__(self, maze, row, col):
        self.maze = maze  # Stores a reference to the maze object
        self.checked = set()  # Set to keep track of checked cells
        self.__row = row  # Enemy's current row
        self.__col = col  # Enemy's current column
        self.last_movement_time = 0 # The time since the enemy last moved

    # Getter and setter methods for the attributes
    def get_row(self):
        return self.__row
    
    def get_col(self):
        return self.__col
    
    def set_row(self, input):
        self.__row = input
        return
    
    def set_col(self, input):
        self.__col = input
        return

    # Method to return the current position of the enemy
    def enemy(self):
        return self.__row, self.__col

    # Method to create an enemy character in the maze
    def createenemy(self):
        # Randomly select a cell from the perimeter as the enemy's position
        self.maze.get_cell(self.__row, self.__col).set_is_enemy(False) # Remove the old enemy
        (self.__row, self.__col) = random.choice(generator.get_perimeter_cells()) 
        enemycell = self.maze.get_cell(self.__row, self.__col)
        
        enemycell.set_is_enemy(True)  # Mark the cell as having the enemy

    # Method to manage the enemy's movement speed
    def movement_speed(self):
        current_time = pygame.time.get_ticks()  # Get the current time
        # If the enemy is in a 'heavy' cell, move slower
        if realmaze.get_cell(self.__row,self.__col).get_is_heavy():
            if current_time - self.last_movement_time >= 1000:  # Check if enough time has passed
                self.chase_player()  # Enemy chases the player faster
                self.last_movement_time = current_time  # Update the last movement time
                
        else:
            if current_time - self.last_movement_time >= 150:
                self.chase_player()  # Enemy chases the player faster
                self.last_movement_time = current_time  # Update the last movement time
        


        # Call method to check if the enemy has caught the player
        enemy.checkcaught()

    # Method within the Enemy class to initiate the chase of the player
    def chase_player(self):
        self.findpath()  # Call the findpath method to determine the path to the player

    # Method to find a path to the player using a pathfinding algorithm
    def findpath(self):
        open_set = []  # Initialise the open set for pathfinding
        pathCells = {}  # Dictionary to store the path cells
        current_player_pos = (player.get_row(), player.get_col())  # Current position of the player

        # Initialise dictionaries for pathfinding costs
        g = {}  # Cost from the start node
        h = {}  # Heuristic cost to the target
        f = {}  # Total cost (g + h)

        # Set initial cost values for each cell in the maze
        for row in range(rows):
            for col in range(columns):
                cell = (row, col)
                g[cell] = float('inf')  # Set initial cost to infinity
                h[cell] = solution.manhattan_distance(cell, current_player_pos)  # Heuristic distance to the player
                f[cell] = g[cell] + h[cell]  # Total cost

        # Set the cost for the enemy's current position
        g[(self.__row, self.__col)] = 0
        f[(self.__row, self.__col)] = g[(self.__row, self.__col)] + h[(self.__row, self.__col)]

        heapq.heappush(open_set, (0, (self.__row, self.__col)))  # Add enemy's position to the open set
        self.checked.add((self.__row, self.__col))  # Add enemy's position to the checked set

        # Pathfinding loop
        while open_set:
            
            _, currentcell = heapq.heappop(open_set)  # Pop the cell with the lowest cost

            # Check if the current cell is the player's position
            if currentcell == current_player_pos:
                print('path found')  # Debug message
                print('enemy is here', '(' + str(self.__row) + ',' + str(self.__col) + ')')  # Message for debugging Enemy's position
                print('player is here', current_player_pos)  # Message for debugging Player's position
                self.eatplayer() # Method for when the enemy cell has taken the player
                if self.checkcaught():
                    return
                self.move_closer(pathCells)  # Move the enemy closer to the player


                # Reset the sets and lists for the next pathfinding iteration
                open_set = []
                pathCells = {}
                set.clear(self.checked)
                break

            else:
                # Process each neighbor of the current cell
                for neighbour in solution.neighbours(currentcell):
                    self.checked.add(neighbour)  # Add neighbor to checked set
                    tentative_g = g[currentcell] + solution.weight(neighbour)  # Calculate tentative G cost
                    # Check if this path to neighbor is better than previously recorded path
                    if tentative_g < g[neighbour]:
                        pathCells[neighbour] = currentcell  # Update path
                        g[neighbour] = tentative_g  # Update G cost
                        f[neighbour] = g[neighbour] + h[neighbour]  # Update F cost

                        # If the neighbor is not in the open set, add it
                        if neighbour not in open_set:
                            heapq.heappush(open_set, (f[neighbour], neighbour))
            
            

    # Method for the enemy to 'eat' the player if close enough
    def eatplayer(self):
        coordinates = [(1,0),(0,-1),(0,0),(0,1),(-1,0)] 
        for coord in coordinates:
            potentialcell = (self.__row + coord[0], self.__col + coord[1]) 
            if potentialcell[0] == player.get_row() and potentialcell[1] == player.get_col(): # If the player is next to the enemy, the enemy will 'eat' it
                self.maze.get_cell(self.__row, self.__col).set_is_enemy(False) 
                self.maze.get_cell(potentialcell[0], potentialcell[1]).set_is_enemy(True) 
                self.__row, self.__col = potentialcell # Enemy takes player's place
        self.maze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display


    # Method to move the enemy closer to the player
    def move_closer(self, cameFrom):
        print('in move closer')  # Debug message
        nextcell = self.get_next_enemy_cell(cameFrom)  # Determine the next cell for the enemy to move to
        self.maze.get_cell(self.__row,self.__col).set_is_enemy(False)  # Mark the current cell as not having the enemy

        if nextcell is None:  # If there's no next cell, end the method
            return

        # Update the enemy's position to the next cell
        self.__row, self.__col = nextcell[0], nextcell[1]
        self.maze.get_cell(self.__row,self.__col).set_is_enemy(True)  # Mark the new cell as having the enemy
        self.maze.draw(screen)  # Redraw the maze with the enemy's new position
        print('enemy moved to:', self.__row, self.__col)  # Debug message
        pygame.display.update()  # Update the display

    # Method to get the next cell for the enemy to move to
    def get_next_enemy_cell(self, cameFrom):
        player_pos = (player.get_row(), player.get_col())  # Player's position
        total_path = []  # List to store the path from the enemy to the player
        currentcell = cameFrom[player_pos]  # Start from the player's position
        # Trace back the path from the player to the enemy
        while currentcell != (self.__row, self.__col):
            total_path.append(currentcell)  # Add cell to the path
            currentcell = cameFrom[currentcell]  # Move to the next cell in the path
        if total_path:  # If there is a path
            nextcell = total_path[-1]  # The next cell is the last cell in the path
            return nextcell
            
        else:
            return 
        
    # Method to check if the enemy cell has 'eaten' the player    
    def checkcaught(self):
        if self.__row == player.get_row() and self.__col == player.get_col(): # Check if they occupy the same tile
            player.set_finished(True)
            print('finished by caught') # Print message for debugging
            # Remove the cells of the enemy and player
            self.maze.get_cell(self.__row, self.__col).set_is_enemy(False)
            self.__row, self.__col = 0,0
            # Remove any player cells from the grid 
            for row in range(rows):
                for col in range(columns):
                    if self.maze.get_cell(row, col).get_is_player():
                        self.maze.get_cell(row,col).set_is_player(False)
                        print('in remove player loop') # Print message for debugging

            player.set_row(solution.startcell[0]), player.set_col(solution.startcell[1]) # Reset the player to the start
            self.maze.get_cell(player.get_row(), player.get_col()).set_is_player(True) 
            player.set_finished(False)
            self.maze.draw(screen) # Redraw the maze
            pygame.display.update() # Update the display
            return True
        

        

# Class for handling various inputs in the game
class Inputs:
    def __init__(self, maze):
        self.maze = maze  # Stores a reference to the maze object

    # Method for handling input to start maze generation
    def input_for_start_generation(self):
        generator.generate()  # Call the maze generator

    # Method for handling input to start solving the maze
    def input_for_solution_creation(self):
        solution.A_star()  # Start the A* algorithm

    # Method for handling input to clear the solution
    def input_for_clearing_solution(self):
        solution.clear_solution()  # Clear the current solution

    # Method for handling input to start the game
    def input_for_starting_game(self):
        generator.generate()  # Generate the maze
        solution.createstartend()  # Create start and end points
        enemy.createenemy()  # Create an enemy character

    # Method for handling input to reset the maze
    def input_to_reset(self):
        self.maze.reset()  # Reset the maze

    # Method for handling input to place the start cell
    def input_to_place_start(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        row, col = cell_coords(mouse_x, mouse_y)  # Convert mouse position to grid coordinates
        cellpressed = self.maze.get_cell(row,col)  # Get the cell at the mouse position

        # Handling input for placing the start cell
        if cellpressed.get_is_start():
            cellpressed.set_is_start(False)  # Unmark the cell as the start cell
            cellpressed.set_is_player(False)  # Unmark the cell as the player's position
            player.set_row(0), player.set_col(0)  # Reset player's position
        else:
            # Update the current start cell and the player's position
            self.maze.get_cell(solution.startcell[0],solution.startcell[1]).set_is_start(False)  # Unmark the old start cell
            cellpressed.set_is_start(True)  # Mark the new cell as the start cell
            realmaze.get_cell(player.get_row(), player.get_col()).set_is_player(False)  # Unmark the old player position
            solution.startcell = row, col  # Update the start cell in the solution
            player.set_row(row), player.set_col(col)  # Update player's position
            cellpressed.set_is_player(True)  # Mark the new cell as the player's position
            player.set_finished(False)  # Reset the player's finished status

        realmaze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display
    
    # Method for handling input to place the end cell
    def input_to_place_end(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        row, col = cell_coords(mouse_x, mouse_y)  # Convert mouse position to grid coordinates
        cellpressed = self.maze.get_cell(row,col)  # Get the cell at the mouse position

        # Toggle the end cell state
        if cellpressed.get_is_end():
            cellpressed.set_is_end(False)  # Unmark the cell as the end cell
        else:
            realmaze.get_cell(solution.endcell[0],solution.endcell[1]).set_is_end(False)  # Unmark the old end cell
            cellpressed.set_is_end(True)  # Mark the new cell as the end cell
            solution.endcell = row, col  # Update the end cell in the solution

        realmaze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display

    # Methods for handling player movement inputs
    def input_to_move_up(self):
        player.moveup()  # Call player's method to move up

    def input_to_move_down(self):
        player.movedown()  # Call player's method to move down

    def input_to_move_left(self):
        player.moveleft()  # Call player's method to move left

    def input_to_move_right(self):
        player.moveright()  # Call player's method to move right

    # Method for handling input to toggle a wall cell
    def input_to_toggle_wall(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        row, col = cell_coords(mouse_x, mouse_y)  # Convert mouse position to grid coordinates
        cellpressed = self.maze.get_cell(row,col)  # Get the cell at the mouse position

        # Toggle the wall state of the cell
        if cellpressed.get_is_wall():
            cellpressed.set_is_wall(False)  # Unmark the cell as a wall
        else:
            cellpressed.set_is_wall(True)  # Mark the cell as a wall

        realmaze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display

    # Method for handling input to toggle a heavy cell
    def input_to_toggle_heavy_cell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        row, col = cell_coords(mouse_x, mouse_y)  # Convert mouse position to grid coordinates
        cellpressed = self.maze.get_cell(row,col)  # Get the cell at the mouse position

        # Toggle the wall state of the cell
        if cellpressed.get_is_heavy():
            cellpressed.set_is_heavy(False)  # Unmark the cell as heavy
        else:
            cellpressed.set_is_heavy(True)  # Mark the cell as heavy

        realmaze.draw(screen)  # Redraw the maze
        pygame.display.update()  # Update the display

    # Method for handling input to use player's power1 
    def input_for_power1(self):
        # Check if the player hasn't finished the game and has power1 available
        if not player.get_finished() and player.get_power1() > 0:
            player.oilspill()  # Trigger the oil spill ability of the player
            
    # Method for handling input to use player's power2
    def input_for_power2(self):
        if not player.get_finished() and player.get_power2() > 0:
                    player.explode()  # Trigger the explode ability of the player
    
    

# Function to convert x and y screen coordinates to row and column indices
def cell_coords(x, y):
    row = x // cellSize  # Calculate row index based on x-coordinate and cell size
    col = y // cellSize  # Calculate column index based on y-coordinate and cell size
    print(row, col, "been coordinated")  # Debug message displaying the calculated indices
    return row, col  # Return the row and column indices

# Initialization of various objects for the game
end_set = False  # Flag to determine if the end has been set
realmaze = Maze(rows, columns)  # Create a new Maze object
generator = Generator(realmaze)  # Create a Generator object for the maze
solution = Solution(realmaze)  # Create a Solution object for pathfinding in the maze
player = Player(realmaze, 0, 0)  # Create a Player object
enemy = Enemy(realmaze, 0, 0)  # Create an Enemy object 
inputs = Inputs(realmaze)  # Create an Inputs object for handling user inputs

# Main game loop
running = True  # Flag to keep the game running
while running:
    for event in pygame.event.get():  # Event handling loop
        if event.type == pygame.QUIT:  # Check for quit event
            running = False  # Stop the game loop
        elif event.type == pygame.KEYDOWN:
            # Handling the 'K' key press event
            if event.key == pygame.K_k:
                inputs.input_for_start_generation()  # Start maze generation
            # Handling the '1' key press event
            elif event.key == pygame.K_1:
                inputs.input_for_solution_creation()  # Start solving the maze
            # Handling the 'R' key press event
            elif event.key == pygame.K_r:
                inputs.input_to_reset()  # Reset the maze
            # Handling the 'T' key press event
            elif event.key == pygame.K_t:
                inputs.input_for_clearing_solution()  # Clear the solution
        
            # Handling the '2' key press event
            elif event.key == pygame.K_2:
                inputs.input_for_starting_game()  # Call the method to start the game

            # Handling the 'Q' key press event
            elif event.key == pygame.K_q:
                inputs.input_to_place_start()  # Call the method to place the start cell

            # Handling the 'W' key press event
            elif event.key == pygame.K_w:
                inputs.input_to_place_end()  # Call the method to place the end cell

            # Handling the 'N' key press event
            if event.key == pygame.K_z:
                inputs.input_for_power1()

            # Handling the 'X' key press event
            if event.key == pygame.K_x:
                inputs.input_for_power2()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Check if a mouse button was pressed
            if event.button == 1:  # If the left mouse button was pressed
                # Get the mouse coordinates and map them to a cell in your grid
                inputs.input_to_toggle_wall()

            if event.button == 3:  # If the right mouse button was pressed
                inputs.input_to_toggle_heavy_cell()
                print('heavy') # Print message for debugging
                
        # Check if the game is not yet finished
        if not player.get_finished():
            # Handling keyboard events when a key is pressed
            if event.type == pygame.KEYDOWN:
                # If the left arrow key is pressed
                if event.key == pygame.K_LEFT:
                    # Calculate the new position to move to (left)
                    inputs.input_to_move_left()

                # If the right arrow key is pressed
                elif event.key == pygame.K_RIGHT:
                    inputs.input_to_move_right()

                # If the up arrow key is pressed
                elif event.key == pygame.K_UP:
                    inputs.input_to_move_up()

                # If the down arrow key is pressed
                elif event.key == pygame.K_DOWN:
                    inputs.input_to_move_down()
        
    
        

    if not player.get_finished() and enemy.get_row() != 0 and enemy.get_col() != 0: # If the player hasn't finished and the enemy is active
        enemy.movement_speed() # Call method that calls movement with a time delay
        enemy.checkcaught() # Check if the enemy has 'eaten' the player

    
# Fill the screen with a grey background
screen.fill(GREY)

# Redraw the maze and update the display
realmaze.draw(screen)
pygame.display.flip()
clock.tick(60)  # Control frame rate

pygame.quit()  # Quits the game when finished