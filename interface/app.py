import tkinter as tk
from tkinter import ttk

# --- Functions ---
def add_item():
    """Gets text from the input box and adds it as a new label in the column."""
    item_text = entry.get()
    if item_text:  # Only add if the input is not empty
        # Create a new label for the item
        new_item_label = ttk.Label(items_frame, text=item_text, padding=(5, 2))
        
        # Add the new label to the grid in the next available row
        # .grid_size() returns (columns, rows), so we use the current number of rows
        # as the index for the new row.
        new_item_label.grid(column=0, row=items_frame.grid_size()[1], sticky="w")
        
        # Clear the entry box for the next item
        entry.delete(0, tk.END)

# --- Main Application Window ---
root = tk.Tk()
root.title("Input and Column Display")
root.geometry("300x400") # Set a default size

# --- Main Frame ---
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# --- Input Section ---
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill="x", pady=5)

ttk.Label(input_frame, text="New Item:").pack(side="left", padx=(0, 5))
entry = ttk.Entry(input_frame)
entry.pack(side="left", fill="x", expand=True)
add_button = ttk.Button(input_frame, text="Add", command=add_item)
add_button.pack(side="left", padx=(5, 0))

# --- Display Column Section ---
# Add a separator
ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

# Create a frame to hold the column of items
items_frame = ttk.Frame(main_frame)
items_frame.pack(fill="both", expand=True)
ttk.Label(items_frame, text="Items List:", font=("Helvetica", 10, "bold")).grid(column=0, row=0, sticky="w", pady=(0,5))


# --- Start the application ---
root.mainloop()