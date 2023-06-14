import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GameOfLife:
    def __init__(self, width, height):
        """
        Creates a grid of size (height, width) with all cells initially set to False (dead).
        """
        self.width = width
        self.height = height
        self.grid = np.full((height, width), False, dtype=bool)
        
    def set_initial_state(self, initial_state):
        """
        Sets the initial state of the grid based on the provided initial_state.
        The initial_state is a numpy array where 'X' represents alive cells and '-' represents dead cells.
        The initial_state is placed at the center of the grid.
        """
        rows, cols = initial_state.shape
        x = (self.width - cols) // 2
        y = (self.height - rows) // 2
        
        self.grid[y:y+rows, x:x+cols] = (initial_state == 'X')
    
    def randomize_initial_state(self):
        """
        Randomizes the initial state of the grid.
        Sets each cell in the grid randomly to either True (alive) or False (dead).
        """
        self.grid = np.random.choice([False, True], size=(self.height, self.width))
    
    def get_neighbors(self, x, y):
        """
        Gets the neighboring cells around the given cell at coordinates (x, y).
        Returns a 2D numpy array containing the neighboring cells.
        """
        x_min = max(0, x-1)
        x_max = min(self.width-1, x+1)
        y_min = max(0, y-1)
        y_max = min(self.height-1, y+1)
        
        return self.grid[y_min:y_max+1, x_min:x_max+1]
    
    def count_live_neighbors(self, x, y):
        """
        Counts the number of live (alive) neighbors around the given cell at coordinates (x, y).
        Returns the count of live neighbors.
        """
        neighbors = self.get_neighbors(x, y)
        return np.count_nonzero(neighbors)
    
    def update(self):
        """
        Updates the grid based on the rules of the Game of Life.
        Creates a new grid and updates each cell based on its current state and the state of its neighbors.
        """
        new_grid = np.full((self.height, self.width), False, dtype=bool)
        
        for y in range(self.height):
            for x in range(self.width):
                live_neighbors = self.count_live_neighbors(x, y)
                
                if self.grid[y, x]:  # Cell is currently alive
                    if live_neighbors == 2 or live_neighbors == 3:
                        new_grid[y, x] = True
                else:  # Cell is currently dead
                    if live_neighbors == 3:
                        new_grid[y, x] = True
        
        self.grid = new_grid
    
    def simulate(self, num_steps):
        """
        Simulates the game of life for the specified number of steps.
        Displays the animation of the grid evolution using matplotlib.
        """
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, cmap='binary')
        
        def animate(frame):
            self.update()
            img.set_array(self.grid)
        
        ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=1000)
        plt.show()


# Prompt the user for the desired options
width = int(input("Enter the width of the grid: "))
height = int(input("Enter the height of the grid: "))

randomize = input("Randomize initial state? (y/n): ").lower() == "y"

# Create the game and set the initial state
game = GameOfLife(width, height)

if randomize:
    game.randomize_initial_state()
else:
    print("Enter the initial state row by row (use 'X' for alive cells and '-' for dead cells):")
    initial_state = []
    for _ in range(height):
        row = list(input())
        initial_state.append(row)

    initial_state = np.array(initial_state)
    game.set_initial_state(initial_state)

# Start simulation for 100 steps using the simulate method
game.simulate(100)
