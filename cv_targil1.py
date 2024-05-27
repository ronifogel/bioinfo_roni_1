# targil 1

import numpy as np
import tkinter as tk

from tkinter import Canvas
import time


# Step 1: Initialize the Grid
def initialize_grid(size):
    """
    Initializes 80x80 grid with 50% of cells randomly assigned to 0 (black)
    and 50% to 1 (white).
    """
    grid = np.random.choice([0, 1], size=(size, size))
    return grid


# Step 2: Define Non-Deterministic Rules
def apply_rules(grid):
    """
    Applies non-deterministic rules to the grid to encourage the formation of
    alternating stripe patterns. Each cell's new state is determined by its
    neighbors and some randomness.
    """
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = grid[i - 1:i + 2, j - 1:j + 2].sum() - grid[i, j]
            if grid[i, j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if neighbors == 3:
                    new_grid[i, j] = 1
    return new_grid

# Draw the grid using tkinter
def draw_grid(canvas, grid, rects, cell_size):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            color = "black" if grid[i, j] == 1 else "white"
            canvas.itemconfig(rects[i][j], fill=color)

# Run the automaton and visualize with tkinter
def run_automaton(initial_grid, generations, cell_size=10, delay=100):
    grid = initial_grid
    root = tk.Tk()
    canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
    canvas.pack()

    rects = [[canvas.create_rectangle(j * cell_size, i * cell_size,
                                      (j + 1) * cell_size, (i + 1) * cell_size,
                                      fill="white", outline="gray")
              for j in range(grid_size)] for i in range(grid_size)]

    def update():
        nonlocal grid
        grid = apply_rules(grid)
        draw_grid(canvas, grid, rects, cell_size)
        root.after(delay, update)

    root.after(delay, update)
    root.mainloop()

# Parameters
grid_size = 80
generations = 250
cell_size = 5
delay = 100  # milliseconds

# Initialize grid and run the automaton
initial_grid = initialize_grid(grid_size)
run_automaton(initial_grid, generations, cell_size, delay)

# # Step 3: Measure Pattern Formation
# def measure_pattern(grid):
#     """
#     Measures how close the grid is to the ideal alternating stripe pattern.
#     The score is the proportion of columns that match the desired pattern.
#     """
#     size = grid.shape[0]
#     score = 0
#     for j in range(size):
#         col = grid[:, j]
#         if np.all(col[::2] == 1) and np.all(col[1::2] == 0):
#             score += 1
#         elif np.all(col[::2] == 0) and np.all(col[1::2] == 1):
#             score += 1
#     return score / size




# # Step 4: Simulate Generations with Animation
# def update(frame, grid, img, scores):
#     """
#     Update function for the animation that applies rules to the grid,
#     measures the pattern, and updates the image.
#     """
#     new_grid = apply_rules(grid)
#     score = measure_pattern(new_grid)
#     scores.append(score)
#     img.set_data(new_grid)
#     ax.set_title(f"Generation {frame}")
#     grid[:] = new_grid  # Update grid in place
#     return [img]
#
#
# # Main Execution
# if __name__ == "__main__":
#     size = 80
#     generations = 250
#     runs = 1
#
#     # Initialize the grid
#     grid = initialize_grid(size)
#     scores = []
#
#     # Prepare the figure and axis
#     fig, ax = plt.subplots()
#     img = ax.imshow(grid, interpolation='nearest')
#     ax.set_title("Generation 0")
#
#     # Animation function
#     ani = FuncAnimation(
#         fig, update, fargs=(grid, img, scores), frames=10, interval=500,
#                                   save_count=50
#     )
#
#     # Show the animation
#     plt.show()
