import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime
import json
import os

from calendar_ui import CalendarApp
from schedule_generator import generate_ai_schedule
from event_manager import EventManager

class CalendarApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("AI-Powered Calendar App")
        self.master.geometry("800x600")

        # Event storage file
        self.events_file = "calendar_events.json"

        # Initialize event manager
        self.event_manager = EventManager(self.events_file)

        # Create calendar UI
        self.calendar_ui = CalendarApp(master, self.event_manager)

        # Create schedule generation button
        self.create_schedule_button = tk.Button(
            master, 
            text="Create AI Schedule", 
            command=self.open_schedule_dialog
        )
        self.create_schedule_button.pack(pady=10)

    def open_schedule_dialog(self):
        # Open a dialog to choose a date and add tasks
        date_dialog = tk.Toplevel(self.master)
        date_dialog.title("Create AI Schedule")
        date_dialog.geometry("400x300")

        # Date selection
        date_label = tk.Label(date_dialog, text="Select Date:")
        date_label.pack(pady=5)

        # Use a StringVar to store the selected date
        self.selected_date = tk.StringVar()
        date_entry = tk.Entry(date_dialog, textvariable=self.selected_date)
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        # Tasks input
        tasks_label = tk.Label(date_dialog, text="Enter Tasks (comma-separated):")
        tasks_label.pack(pady=5)
        tasks_text = tk.Text(date_dialog, height=5, width=50)
        tasks_text.pack(pady=5)

        # Generate Schedule Button
        generate_button = tk.Button(
            date_dialog, 
            text="Generate AI Schedule", 
            command=lambda: self.generate_and_save_schedule(
                date_entry.get(), 
                tasks_text.get("1.0", tk.END).strip()
            )
        )
        generate_button.pack(pady=10)

    def generate_and_save_schedule(self, date, tasks):
        # Split tasks
        task_list = [task.strip() for task in tasks.split(',') if task.strip()]
        
        try:
            # Generate AI schedule
            ai_schedule = generate_ai_schedule(task_list)
            
            # Save events for the selected date
            for time, task in ai_schedule.items():
                self.event_manager.add_event(
                    date, 
                    time, 
                    task
                )
            
            # Refresh calendar view
            self.calendar_ui.update_calendar()
            
            messagebox.showinfo("Success", f"AI Schedule generated for {date}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate schedule: {str(e)}")

def main():
    root = tk.Tk()
    app = CalendarApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()