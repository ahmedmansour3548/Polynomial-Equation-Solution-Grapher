import itertools
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the possible values for wildcard slots (both digits and operators)
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
OPERATORS = ['+', '-', '*', '/', '%', '^']
FRACTIONS = [f'{i/100:.3f}' for i in range(1, 100)]  # Generate fractional values up to the thousandth place

# Define a function to map operators and digits to their respective x/y/z coordinates
def map_to_axis_value(item):
    if item in OPERATORS:
        return OPERATORS.index(item) + 1  # Map operators to x = 1 to 6
    elif item in DIGITS:
        return DIGITS.index(item) + 7     # Map digits 0-9 to x = 7 to 16
    elif item in FRACTIONS:
        return 17  # Map fractions to x = 17 (arbitrary value)
    else:
        raise ValueError(f"Invalid item {item}")

def generate_combinations(formula, enable_fractions):
    """Generate all possible variations of the formula by replacing ? with digits or operators."""
    wildcards = formula.count('?')
    replacements = OPERATORS + DIGITS
    if enable_fractions:
        replacements += FRACTIONS
    combinations = itertools.product(replacements, repeat=wildcards)

    formulas = []
    for combo in combinations:
        new_formula = formula
        for item in combo:
            new_formula = new_formula.replace('?', item, 1)
        formulas.append((new_formula, combo))
    
    return formulas

def evaluate_formula(formula):
    """Evaluate the formula and return whether it's valid."""
    try:
        # Replace the custom '^' operator with Python's '**' operator
        formula = formula.replace('^', '**')
        left_side, right_side = formula.split('=')
        left_value = eval(left_side.replace(" ", ""))
        right_value = eval(right_side.replace(" ", ""))
        return left_value == right_value
    except Exception as e:
        return False

def graph_1D_solutions(valid_solutions, canvas, root):
    """Graph the valid solutions using a 1D number line."""
    plt.close()
    x_values = []
    labels = []

    for solution, combo in valid_solutions:
        x = map_to_axis_value(combo[0])
        x_values.append(x)
        labels.append(solution.replace(" ", ""))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x_values, np.zeros(len(x_values)), color='blue')

    for i, label in enumerate(labels):
        ax.annotate(label, (x_values[i], 0), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_xlim(1, 16)
    tick_labels = OPERATORS + DIGITS
    ticks = np.arange(1, 17)
    
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([])  # Remove y-axis ticks for 1D graph

    ax.set_title('1D Valid Solutions of Formula')
    ax.set_xlabel('Wildcard Value')
    ax.grid(True)

    canvas.figure = fig
    canvas.draw()

def graph_2D_solutions(valid_solutions, canvas, root):
    """Graph the valid solutions using a 2D scatter plot."""
    plt.close()
    x_values = []
    y_values = []
    labels = []

    for solution, combo in valid_solutions:
        x = map_to_axis_value(combo[0])
        y = map_to_axis_value(combo[1])
        x_values.append(x)
        y_values.append(y)
        labels.append(solution.replace(" ", ""))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x_values, y_values, color='blue')

    for i, label in enumerate(labels):
        ax.annotate(label, (x_values[i], y_values[i]), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_xlim(1, 16)
    ax.set_ylim(1, 16)
    
    tick_labels = OPERATORS + DIGITS
    ticks = np.arange(1, 17)
    
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(ticks)
    ax.set_yticklabels(tick_labels)

    ax.set_title('2D Valid Solutions of Formula')
    ax.set_xlabel('First Wildcard Value')
    ax.set_ylabel('Second Wildcard Value')
    ax.grid(True)

    canvas.figure = fig
    canvas.draw()

def graph_3D_solutions(valid_solutions, canvas, root):
    """Graph the valid solutions using a 3D scatter plot."""
    plt.close()
    x_values = []
    y_values = []
    z_values = []
    labels = []

    for solution, combo in valid_solutions:
        x = map_to_axis_value(combo[0])
        y = map_to_axis_value(combo[1])
        z = map_to_axis_value(combo[2])
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)
        labels.append(solution.replace(" ", ""))

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_values, y_values, z_values, color='blue')

    for i, label in enumerate(labels):
        ax.text(x_values[i], y_values[i], z_values[i], label, size=10, zorder=1)

    ax.set_xlim(1, 16)
    ax.set_ylim(1, 16)
    ax.set_zlim(1, 16)

    tick_labels = OPERATORS + DIGITS
    ticks = np.arange(1, 17)
    
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(ticks)
    ax.set_yticklabels(tick_labels)
    ax.set_zticks(ticks)
    ax.set_zticklabels(tick_labels)

    ax.set_title('3D Valid Solutions of Formula')
    ax.set_xlabel('First Wildcard Value')
    ax.set_ylabel('Second Wildcard Value')
    ax.set_zlabel('Third Wildcard Value')

    canvas.figure = fig
    
    canvas.draw()

def find_and_graph_solutions(input_formula, enable_fractions, canvas, root):
    """Main function to find and graph all valid solutions based on wildcard count."""
    wildcards = input_formula.count('?')
    possible_formulas = generate_combinations(input_formula, enable_fractions)
    valid_solutions = [(formula, combo) for formula, combo in possible_formulas if evaluate_formula(formula)]

    if valid_solutions:
        if wildcards == 1:
            graph_1D_solutions(valid_solutions, canvas, root)
        elif wildcards == 2:
            graph_2D_solutions(valid_solutions, canvas, root)
        elif wildcards == 3:
            graph_3D_solutions(valid_solutions, canvas, root)
    else:
        print("No valid solutions found.")
        canvas.figure.clf()  # Clear canvas if no valid solutions
        canvas.draw()

def start_gui():
    """Create a tkinter GUI for input and graph visualization."""
    root = tk.Tk()
    root.title("Formula Solver")

    # Create a frame for the input and button
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Input label and entry field for formula
    label = tk.Label(frame, text="Enter a formula (e.g., '10 ? 1 ? 1 = 1'): ")
    label.pack(side=tk.LEFT, padx=5)
    
    formula_input = tk.Entry(frame, width=30)
    formula_input.pack(side=tk.LEFT, padx=5)

    # Checkbox for enabling fractional solutions
    enable_fractions_var = tk.BooleanVar()
    enable_fractions_checkbox = tk.Checkbutton(frame, text="Enable Fractional Solutions", variable=enable_fractions_var)
    enable_fractions_checkbox.pack(side=tk.LEFT, padx=5)

    # Create a matplotlib figure inside a tkinter canvas
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Create a button that triggers the graph update
    def on_button_click():
        input_formula = formula_input.get()
        enable_fractions = enable_fractions_var.get()
        find_and_graph_solutions(input_formula, enable_fractions, canvas, root)

    button = tk.Button(frame, text="Graph Solutions", command=on_button_click)
    button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

# Start the GUI application
start_gui()