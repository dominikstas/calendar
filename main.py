import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Schedule")
root.geometry("600x400")

# Define days of the week
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Create a frame to hold the days of the week
frame = tk.Frame(root)
frame.pack(pady=20)

# Loop through each day and create a label with a text entry
for day in days:
    day_frame = tk.Frame(frame, borderwidth=1, relief="solid")
    day_frame.pack(side="left", padx=5, pady=5, expand=True)

    day_label = tk.Label(day_frame, text=day, font=("Arial", 12, "bold"))
    day_label.pack(pady=5)

    # Placeholder entry for tasks (can be expanded later)
    task_entry = tk.Entry(day_frame, width=15)
    task_entry.pack(padx=5, pady=5)

# Run the application
root.mainloop()
