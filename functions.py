import tkinter as tk
from tkinter import messagebox, ttk
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class TaskManager:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.root.geometry("800x600")

        # Days of the week
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Tasks dictionary
        self.tasks = {day: [] for day in self.days}
        
        # Task entries dictionary
        self.task_entries = {}

        # Create frames for each day
        self.create_day_frames()

        # Create buttons
        self.create_buttons()

        # Load Hugging Face GPT-2 Model
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def create_day_frames(self):
        # Create a frame to hold day frames
        days_frame = tk.Frame(self.root)
        days_frame.pack(expand=True, fill=tk.BOTH)

        # Create a frame for each day
        for day in self.days:
            day_frame = tk.LabelFrame(days_frame, text=day, padx=10, pady=10)
            day_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

            # Create a listbox for tasks
            task_listbox = tk.Listbox(day_frame, width=30, height=10)
            task_listbox.pack(padx=5, pady=5)

            # Store the listbox for each day
            self.task_entries[day] = task_listbox

    def create_buttons(self):
        # Create a frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Add Event Button
        add_event_btn = tk.Button(button_frame, text="Add Event", command=self.open_terminal)
        add_event_btn.pack(side=tk.LEFT, padx=5)

        # Print All Events Button
        print_events_btn = tk.Button(button_frame, text="Print All Events", command=self.print_all_events)
        print_events_btn.pack(side=tk.LEFT, padx=5)

        # Generate Schedule Button
        generate_schedule_btn = tk.Button(button_frame, text="Generate Schedule", command=self.open_schedule_terminal)
        generate_schedule_btn.pack(side=tk.LEFT, padx=5)

    def open_terminal(self):
        terminal = tk.Toplevel(self.root)
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
        all_events = tk.Toplevel(self.root)
        all_events.title("All Scheduled Events")
        all_events.geometry("500x400")

        for day, tasks in self.tasks.items():
            tk.Label(all_events, text=day, font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
            for task in tasks:
                tk.Label(all_events, text=f"  - {task}", font=("Helvetica", 10)).pack(anchor="w")

    def open_schedule_terminal(self):
        schedule_terminal = tk.Toplevel(self.root)
        schedule_terminal.title("Generate Daily Schedule")
        schedule_terminal.geometry("500x400")

        # Tasks input
        tk.Label(schedule_terminal, text="Enter tasks for the day (comma-separated):").pack(pady=5)
        task_entry = tk.Entry(schedule_terminal, width=50)
        task_entry.pack(pady=5)

        # Day selection
        tk.Label(schedule_terminal, text="Select Day:").pack(pady=5)
        day_dropdown = ttk.Combobox(schedule_terminal, values=self.days, state="readonly")
        day_dropdown.pack(pady=5)
        day_dropdown.set(self.days[0])  # Default to first day

        # Schedule output text area
        tk.Label(schedule_terminal, text="Generated Schedule:").pack(pady=5)
        schedule_output = tk.Text(schedule_terminal, height=10, width=50, wrap=tk.WORD)
        schedule_output.pack(pady=5)

        def generate_schedule():
            # Clear previous output
            schedule_output.delete(1.0, tk.END)

            # Validate inputs
            tasks_input = task_entry.get().strip()
            selected_day = day_dropdown.get()

            if not tasks_input:
                messagebox.showerror("Error", "Please enter tasks!")
                return

            # Prepare input for schedule generation
            prompt = f"Create a detailed schedule for {selected_day} with these tasks: {tasks_input}. Break down the tasks into a time-organized schedule:"

            try:
                # Tokenize and generate schedule
                inputs = self.tokenizer.encode(prompt, return_tensors="pt")
                
                # Use more controlled generation
                outputs = self.model.generate(
                    inputs, 
                    max_length=250,  # Adjust length as needed
                    num_return_sequences=1,
                    no_repeat_ngram_size=2,
                    temperature=0.7,  # Add some creativity
                    top_k=50,
                    top_p=0.95
                )

                # Decode the generated text
                generated_schedule = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Clean up the generated schedule
                cleaned_schedule = generated_schedule[len(prompt):].strip()

                # Insert the cleaned schedule into the text area
                schedule_output.insert(tk.END, cleaned_schedule)

                # Optionally, add the generated schedule to the selected day's task list
                task_list = self.task_entries.get(selected_day)
                if task_list:
                    # Split generated schedule into lines and add as tasks
                    for line in cleaned_schedule.split('\n'):
                        if line.strip():
                            task_list.insert(tk.END, line.strip())

            except Exception as e:
                messagebox.showerror("Generation Error", str(e))

        # Generate button
        generate_btn = tk.Button(schedule_terminal, text="Generate Schedule", command=generate_schedule)
        generate_btn.pack(pady=10)

# Create and run the application
if __name__ == "__main__":
    app = TaskManager()
    app.run()