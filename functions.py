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
        terminal.geometry("500x300")

    def process_command(self, command):
        parts = command.split()
        if len(parts) < 4:
            messagebox.showerror("Error", "Invalid command format.")
            return
        action = parts[0]
        if action == "add":
            event, day, hour = parts[1], parts[2].capitalize(), parts[3]
            self.add_task(event, day, hour)

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
        pass
