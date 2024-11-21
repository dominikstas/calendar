import tkinter as tk
from tkinter import ttk, messagebox

# Initialize the main window
root = tk.Tk()
root.title("Schedule")
root.geometry("900x600")  # Updated resolution for better visibility

# Define days of the week and storage for tasks
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
tasks = {day: [] for day in days}

# Create a frame to hold the days of the week
frame = tk.Frame(root)
frame.pack(pady=20, padx=10)

# Create dictionary to store task entries
task_entries = {}

# Loop through each day and create a label with a text entry
for day in days:
    day_frame = tk.Frame(frame, borderwidth=1, relief="solid", padx=5, pady=5)
    day_frame.grid(row=0 if days.index(day) < 4 else 1, column=days.index(day) % 4, padx=10, pady=10)

    day_label = tk.Label(day_frame, text=day, font=("Arial", 12, "bold"))
    day_label.pack(pady=5)

    # Listbox with a vertical scrollbar
    task_frame = tk.Frame(day_frame)
    task_frame.pack(pady=5)

    task_entry = tk.Listbox(task_frame, width=20, height=8)
    task_entry.pack(side="left")

    scrollbar = tk.Scrollbar(task_frame, orient="vertical", command=task_entry.yview)
    scrollbar.pack(side="right", fill="y")
    task_entry.config(yscrollcommand=scrollbar.set)

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

# Function to delete task
def delete_task(event, day, hour):
    if day not in days:
        messagebox.showerror("Error", f"Invalid day: {day}")
        return
    task = f"{hour}: {event}"
    if task in tasks[day]:
        tasks[day].remove(task)
        # Remove from Listbox
        index = task_entries[day].get(0, tk.END).index(task)
        task_entries[day].delete(index)
    else:
        messagebox.showinfo("Info", f"Task '{task}' not found for {day}.")

# Function to process terminal commands
def process_command(command):
    parts = command.split()
    if len(parts) >= 4:
        action = parts[0]
        event = parts[1]
        day = parts[2].capitalize()
        hour = parts[3]

        if action == "add":
            add_task(event, day, hour)
        elif action == "delete":
            delete_task(event, day, hour)
        else:
            messagebox.showerror("Error", "Invalid command. Use 'add' or 'delete'.")
    else:
        messagebox.showerror("Error", "Invalid command format. Use: add <event> <day> <hour> or delete <event> <day> <hour>")

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
        text="Format: add <event> <day> <hour> or delete <event> <day> <hour>\nExample: delete Meeting Monday 10:00",
        fg="gray"
    )
    instructions.pack(pady=5)

# Bind F1 key to open the terminal
root.bind("<F1>", lambda event: open_terminal())

# Run the application
root.mainloop()
