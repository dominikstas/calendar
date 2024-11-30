# functions.py
import tkinter as tk
from tkinter import messagebox

class TaskManager:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.tasks = {day: [] for day in self.days}
        self.task_entries = {}

    def open_terminal(self):
        terminal = tk.Toplevel()
        terminal.title("Add Event")
        terminal.geometry("400x300")

        # Create input fields for Event Name, Day, and Time
        tk.Label(terminal, text="Event Name").pack(pady=5)
        event_name_entry = tk.Entry(terminal)
        event_name_entry.pack(pady=5)

        tk.Label(terminal, text="Day").pack(pady=5)
        day_entry = tk.Entry(terminal)
        day_entry.pack(pady=5)

        tk.Label(terminal, text="Time").pack(pady=5)
        time_entry = tk.Entry(terminal)
        time_entry.pack(pady=5)

        def submit_event():
            event_name = event_name_entry.get()
            day = day_entry.get().capitalize()
            time = time_entry.get()

            if not event_name or not day or not time:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            self.add_task(event_name, day, time)
            terminal.destroy()

        tk.Button(terminal, text="Submit", command=submit_event).pack(pady=20)

    def add_task(self, event, day, hour):
        if day not in self.days:
            messagebox.showerror("Error", f"Invalid day: {day}")
            return
        task = f"{hour}: {event}"
        self.tasks[day].append(task)
        self.task_entries[day].insert(tk.END, task)
        self.sort_tasks(day)

    def sort_tasks(self, day):
        tasks = list(self.task_entries[day].get(0, tk.END))
        tasks.sort(key=lambda x: x.split(":")[0])
        self.task_entries[day].delete(0, tk.END)
        for task in tasks:
            self.task_entries[day].insert(tk.END, task)

    def print_all_events(self):
        all_events = tk.Toplevel()
        all_events.title("All Scheduled Events")
        all_events.geometry("500x400")

        for day, tasks in self.tasks.items():
            tk.Label(all_events, text=day, font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
            for task in tasks:
                tk.Label(all_events, text=f"  - {task}", font=("Helvetica", 10)).pack(anchor="w")
