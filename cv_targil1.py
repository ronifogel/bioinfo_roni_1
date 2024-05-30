# targil 1

import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

# Step 1: Initialize the Grid
def initialize_grid(size):
    """
    Initializes 80x80 grid with 50% of cells randomly assigned to 0 (black)
    and 50% to 1 (white).
    """
    grid = np.random.choice([0, 1], size=(size, size))
    return grid

# Step 2: Define Non-Deterministic Rules
def update_cell(grid, x, y):
    """
    Applies non-deterministic rules to the cell to encourage the formation of
    alternating stripe patterns. Each cell's new state is determined by its
    neighbors and some randomness.
    """
    # Count horizontal neighbors (left and right)
    neighbors = [
        grid[(x-1) % grid.shape[0], (y-1) % grid.shape[1]],  # Top-left
        grid[(x-1) % grid.shape[0], (y+1) % grid.shape[1]],  # Top-right
        grid[x, (y-1) % grid.shape[1]],                      # Left
        grid[x, (y+1) % grid.shape[1]],                      # Right
        grid[(x+1) % grid.shape[0], (y-1) % grid.shape[1]],  # Bottom-left
        grid[(x+1) % grid.shape[0], (y+1) % grid.shape[1]]   # Bottom-right
    ]
    
    # Rule: Prefer alternating pattern based on majority of horizontal neighbors
    if neighbors.count(1) > neighbors.count(0): # most of the neighbors is 1 - be 0
        return 0
    elif neighbors.count(0) > neighbors.count(1): # most of the neighbors is 0 - be 1
        return 1
    else:
        # Count vertical neighbors
        neighbors = [
        grid[(x-1) % grid.shape[0], y],                      # Top
        grid[(x+1) % grid.shape[0], y],                      # Bottom
        ]

        if neighbors.count(1) > neighbors.count(0): # most of the colum is 1 - be 1
            return 1
        elif neighbors.count(0) > neighbors.count(1): # most of the colum is 0 - be 0
            return 0
        # else: return 0 # top differeent from bottom
        else: return np.random.choice([0, 1]) # top differeent from bottom


def update_grid(grid):
    """
    Applies non-deterministic rules to the update the cells grid to encourage the formation of
    alternating stripe patterns.
    """
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            new_grid[x, y] = update_cell(grid, x, y)
    return new_grid

# Step 3: Define the Measurement Metric
def measure_pattern(grid):
    """
    Measures how close the rows is to an alternating pattern (either starting with 1 or 0).
    The more balanced the sums, the lower the difference, indicating a better stripe pattern.
    """
    total_score = 0
    for x in range(grid.shape[0]):  # Iterate over each row
        row = grid[x, :]  # All column elements in row x
        # Count the number of consecutive elements that are different
        row_score = np.sum(row[:-1] != row[1:]) # Compare indexes between row[0:n-1] to row[1:n]
        total_score += row_score # Increment the total score by the row score
    
    # Normalize the total score by the maximum possible score
    max_score = grid.shape[0] * (grid.shape[1] - 1)  # Each row has size-1 pairs, perfect score = 1
    normalized_score = total_score / max_score
    # print(total_score / 80)
    print(normalized_score)
    # print(max_score)
    return normalized_score

# Step 4: Visualize the Progress with Tkinter
class CellularAutomatonVisualizer:
    """
    Class to present the cellular automaton visualizer
    """
    # constractor of the cellular automaton visualizer
    def __init__(self, root, grid_size):
        self.root = root
        self.grid_size = grid_size
        self.grid = initialize_grid(grid_size) # initialize the cells grid random
        self.canvas = tk.Canvas(root, width=grid_size*10, height=grid_size*10)
        self.canvas.pack()
        self.draw_grid() # present the first random generation

    # update the generation of the cellular automaton visualizer
    def update(self):
        self.grid = update_grid(self.grid)
        self.draw_grid()
    
    # present the cellular automaton visualizer grid
    def draw_grid(self):
        self.canvas.delete("all") # delete the last generation
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                color = "black" if self.grid[x, y] == 1 else "white"
                self.canvas.create_rectangle(y*10, x*10, (y+1)*10, (x+1)*10, fill=color)


# Step 5: Plot the Progress Over Generations
def run_simulation(grid_size, generations, runs):
    """
    Applies the simulation of the cellular automaton visualizer grid for 250 generations.
    """
    root = tk.Tk()
    visualizer = CellularAutomatonVisualizer(root, grid_size) # initialize the cellular automaton visualizer
    pattern_scores = []

    def run_generations(gen):
        if gen < generations:
            print(gen)
            visualizer.update() # update the next generation
            score = measure_pattern(visualizer.grid)
            pattern_scores.append(score)
            root.after(100, run_generations, gen+1) # Update every 100ms
        else:
            root.destroy()
    
    run_generations(0) # start run_generation loop
    root.mainloop()
    return pattern_scores

    # progress = []

    # for _ in range(runs):
    #     grid = initialize_grid(grid_size)
    #     run_progress = []

    #     for _ in range(generations):
    #         grid = update_grid(grid)
    #         score = measure_pattern(grid)
    #         run_progress.append(score)

    #     progress.append(run_progress)

    # return progress

if __name__ == "__main__":
    grid_size = 80
    generations = 200
    runs = 1
    # progress = run_simulation(grid_size, generations, runs)
    pattern_scores = run_simulation(grid_size, generations, runs)

    # Plot the progress over generations
    plt.plot(range(generations), pattern_scores)
    plt.xlabel('Generation')
    plt.ylabel('Stripe Score')
    plt.title('Progress of Cellular Automaton')
    plt.show()

    # Average progress across runs
    # avg_progress = np.mean(progress, axis=0)

    # plt.plot(range(generations), avg_progress)
    # plt.xlabel('Generation')
    # plt.ylabel('Stripe Score')
    # plt.title('Progress of Cellular Automaton')
    # plt.show()

