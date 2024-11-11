import tkinter as tk
from tkinter import ttk, messagebox

# Initialize the main window
root = tk.Tk()
root.title("Schedule")
root.geometry("600x400")

# Define days of the week and storage for tasks
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
tasks = {day: [] for day in days}

# Create a frame to hold the days of the week
frame = tk.Frame(root)
frame.pack(pady=20)

# Create dictionary to store task entries
task_entries = {}

# Loop through each day and create a label with a text entry
for day in days:
    day_frame = tk.Frame(frame, borderwidth=1, relief="solid")
    day_frame.pack(side="left", padx=5, pady=5, expand=True)

    day_label = tk.Label(day_frame, text=day, font=("Arial", 12, "bold"))
    day_label.pack(pady=5)

    # Placeholder entry for tasks (can be expanded later)
    task_entry = tk.Listbox(day_frame, width=15, height=5)
    task_entry.pack(padx=5, pady=5)

    # Store the listbox in the task_entries dictionary
    task_entries[day] = task_entry

# Function to add task
def add_task(event, day, hour):
    if day not in days:
        messagebox.showerror("Error", f"Invalid day: {day}")
        return
    task = f"{hour}: {event}"
    tasks[day].append(task)
    task_entries[day].insert(tk.END, task)

# Function to process terminal commands
def process_command(command):
    parts = command.split()
    if len(parts) >= 4 and parts[0] == "add":
        event = parts[1]
        day = parts[2].capitalize()
        hour = parts[3]
        add_task(event, day, hour)
    else:
        messagebox.showerror("Error", "Invalid command format. Use: add <event> <day> <hour>")

# Function to open terminal
def open_terminal():
    terminal = tk.Toplevel(root)
    terminal.title("Terminal")
    terminal.geometry("400x200")

    command_label = tk.Label(terminal, text="Enter Command:")
    command_label.pack(pady=5)

    command_entry = tk.Entry(terminal, width=50)
    command_entry.pack(pady=5)
    
    def on_enter(event=None):
        command = command_entry.get()
        process_command(command)
        command_entry.delete(0, tk.END)

    # Bind enter key in terminal to process command
    command_entry.bind("<Return>", on_enter)

    # Add instructions for the user
    instructions = tk.Label(
        terminal,
        text="Format: add <event> <day> <hour>\nExample: add Meeting Monday 10:00",
        fg="gray"
    )
    instructions.pack(pady=5)

# Bind F1 key to open the terminal
root.bind("<F1>", lambda event: open_terminal())

# Run the application
root.mainloop()
