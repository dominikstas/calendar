import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class ModernAppDesign:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Schedule")
        self.root.geometry("1024x768")
        self.root.config(bg="#ffffff")

        # Custom colors - changed to violet/purple theme
        self.colors = {
            'primary': '#7c3aed',      # Violet-600
            'secondary': '#a78bfa',    # Violet-400
            'success': '#6d28d9',      # Violet-700
            'background': '#ffffff',   # White
            'surface': '#f5f3ff',     # Violet-50
            'text': '#4c1d95',        # Violet-900
            'border': '#ddd6fe'       # Violet-200
        }

        # Task storage
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.tasks = {day: [] for day in self.days}
        self.task_entries = {}

        # Configure styles
        self.configure_styles()
        self.create_ui()
        self.bind_shortcuts()

    def configure_styles(self):
        # Configure TTK styles
        style = ttk.Style()
        style.configure(
            "Modern.TButton",
            padding=10,
            background=self.colors['primary'],
            foreground="white",
            font=("Helvetica", 10),
            borderwidth=0
        )
        
        style.configure(
            "Card.TFrame",
            background=self.colors['surface'],
            relief="flat",
            borderwidth=1
        )

    def create_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, style="Card.TFrame", padding="20")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with gradient effect
        header_frame = tk.Frame(main_container, bg=self.colors['background'])
        header_frame.pack(fill="x", pady=(0, 20))

        header = tk.Label(
            header_frame,
            text="Smart Weekly Planner",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        header.pack(pady=10)

        subtitle = tk.Label(
            header_frame,
            text="Organize your week efficiently",
            font=("Helvetica", 12),
            bg=self.colors['background'],
            fg=self.colors['secondary']
        )
        subtitle.pack()

        # Days grid container
        days_frame = ttk.Frame(main_container, style="Card.TFrame")
        days_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure grid weights
        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1, uniform="column")
        days_frame.grid_rowconfigure(0, weight=1)

        # Create frames for each day
        for i, day in enumerate(self.days):
            day_frame = tk.Frame(
                days_frame,
                bg=self.colors['background'],
                highlightthickness=1,
                highlightbackground=self.colors['border']
            )
            day_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

            # Day header with custom styling
            day_header = tk.Frame(day_frame, bg=self.colors['primary'], height=40)
            day_header.pack(fill="x")
            day_header.pack_propagate(False)

            day_label = tk.Label(
                day_header,
                text=day,
                font=("Helvetica", 11, "bold"),
                bg=self.colors['primary'],
                fg="white"
            )
            day_label.pack(pady=10)

            # Task listbox with custom styling
            task_frame = tk.Frame(day_frame, bg=self.colors['background'])
            task_frame.pack(fill="both", expand=True)

            task_listbox = tk.Listbox(
                task_frame,
                bg=self.colors['background'],
                fg=self.colors['text'],
                font=("Helvetica", 10),
                selectmode="extended",
                borderwidth=0,
                highlightthickness=0,
                selectbackground=self.colors['primary'],
                selectforeground="white"
            )
            task_listbox.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(task_frame, orient="vertical", command=task_listbox.yview)
            scrollbar.pack(side="right", fill="y")
            task_listbox.config(yscrollcommand=scrollbar.set)

            self.task_entries[day] = task_listbox

        # Footer with action buttons
        footer = tk.Frame(main_container, bg=self.colors['background'])
        footer.pack(pady=20, fill="x")

        btn_frame = tk.Frame(footer, bg=self.colors['background'])
        btn_frame.pack()

        buttons = [
            ("Open Terminal (F1)", self.open_terminal),
            ("View All (F2)", self.print_all_events)
        ]

        for text, command in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                font=("Helvetica", 10),
                bg=self.colors['primary'],
                fg="white",
                padx=20,
                pady=10,
                bd=0,
                cursor="hand2"
            )
            btn.pack(side="left", padx=10)
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['success']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['primary']))

    def open_terminal(self):
        terminal = tk.Toplevel(self.root)
        terminal.title("Add Event")
        terminal.geometry("500x300")
        terminal.configure(bg=self.colors['background'])

        # Center the terminal window
        terminal.geometry("+%d+%d" % (
            self.root.winfo_x() + (self.root.winfo_width() - 500) // 2,
            self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        ))

        header = tk.Label(
            terminal,
            text="Add New Event",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        header.pack(pady=20)

        # Form container
        form_frame = tk.Frame(terminal, bg=self.colors['background'])
        form_frame.pack(fill="both", expand=True, padx=40)

        # Command entry with modern styling
        entry_frame = tk.Frame(form_frame, bg=self.colors['background'])
        entry_frame.pack(fill="x", pady=10)

        command_entry = tk.Entry(
            entry_frame,
            font=("Helvetica", 12),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief="flat",
            width=40
        )
        command_entry.pack(fill="x", ipady=8)

        # Add subtle border
        entry_border = tk.Frame(entry_frame, height=2, bg=self.colors['border'])
        entry_border.pack(fill="x")

        def on_enter(event=None):
            command = command_entry.get()
            self.process_command(command)
            command_entry.delete(0, tk.END)

        command_entry.bind("<Return>", on_enter)

        # Help text
        help_frame = tk.Frame(form_frame, bg=self.colors['background'])
        help_frame.pack(fill="x", pady=20)

        help_title = tk.Label(
            help_frame,
            text="Command Format:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['background'],
            fg=self.colors['secondary']
        )
        help_title.pack(anchor="w")

        examples = [
            "add <event> <day> <hour>",
            "delete <event> <day> <hour>",
            "Example: add Meeting Monday 14:00"
        ]

        for example in examples:
            tk.Label(
                help_frame,
                text=example,
                font=("Helvetica", 10),
                bg=self.colors['background'],
                fg=self.colors['secondary']
            ).pack(anchor="w", pady=2)

def process_command(self, command):
    parts = command.split()
    if len(parts) < 4:
        messagebox.showerror("Error", "Invalid command format.")
        return

    action = parts[0]
    if action == "add":
        if len(parts) != 4:
            messagebox.showerror("Error", "Invalid format for 'add'.")
            return
        event, day, hour = parts[1], parts[2].capitalize(), parts[3]
        self.add_task(event, day, hour)
    elif action == "delete":
        if len(parts) != 4:
            messagebox.showerror("Error", "Invalid format for 'delete'.")
            return
        event, day, hour = parts[1], parts[2].capitalize(), parts[3]
        self.delete_task(event, day, hour)
    elif action == "edit":
        if len(parts) < 5:
            messagebox.showerror("Error", "Invalid format for 'edit'.")
            return
        sub_action = parts[1]
        if sub_action == "hour":
            old_name, new_hour = parts[2], parts[3]
            self.edit_task_hour(old_name, new_hour)
        elif sub_action == "name":
            old_name, new_name = parts[2], parts[3]
            self.edit_task_name(old_name, new_name)
        else:
            messagebox.showerror("Error", "Invalid sub-action for 'edit'. Use 'hour' or 'name'.")
    else:
        messagebox.showerror("Error", "Invalid action. Use 'add', 'delete', or 'edit'.")

    def add_task(self, event, day, hour):
        if day not in self.days:
            messagebox.showerror("Error", f"Invalid day: {day}")
            return
        task = f"{hour}: {event}"
        self.tasks[day].append(task)
        self.task_entries[day].insert(tk.END, task)
        # Sort tasks by time
        self.sort_tasks(day)

    def sort_tasks(self, day):
        tasks = list(self.task_entries[day].get(0, tk.END))
        tasks.sort(key=lambda x: x.split(":")[0])  # Sort by hour
        self.task_entries[day].delete(0, tk.END)
        for task in tasks:
            self.task_entries[day].insert(tk.END, task)

    def delete_task(self, event, day, hour):
        if day not in self.days:
            messagebox.showerror("Error", f"Invalid day: {day}")
            return
        task = f"{hour}: {event}"
        if task in self.tasks[day]:
            self.tasks[day].remove(task)
            index = self.task_entries[day].get(0, tk.END).index(task)
            self.task_entries[day].delete(index)
        else:
            messagebox.showinfo("Info", f"Task '{task}' not found for {day}.")

    def print_all_events(self):
        events_window = tk.Toplevel(self.root)
        events_window.title("All Events")
        events_window.geometry("600x400")
        events_window.configure(bg=self.colors['background'])
        events_window.minsize(600, 400)  # Force minimum size

        # Create container frame with grid layout
        container = tk.Frame(events_window, bg=self.colors['background'])
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_rowconfigure(1, weight=1)  # Make text area expandable
        container.grid_columnconfigure(0, weight=1)

        # Header - row 0
        header = tk.Label(
            container,
            text="All Scheduled Events",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        header.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        # Text widget - row 1
        events_text = tk.Text(
            container,
            wrap="word",
            font=("Helvetica", 11),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            relief="flat",
            padx=15,
            pady=15
        )
        events_text.grid(row=1, column=0, sticky="nsew")

        # Button frame - row 2
        button_frame = tk.Frame(container, bg=self.colors['background'])
        button_frame.grid(row=2, column=0, pady=(20, 0), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)  # Center the button

        # Copy button
        copy_btn = tk.Button(
            button_frame,
            text="Copy to Clipboard",
            font=("Helvetica", 10),
            bg=self.colors['primary'],
            fg="white",
            padx=20,
            pady=10,
            bd=0,
            cursor="hand2",
            command=lambda: self.copy_events(events_text.get("1.0", tk.END))
        )
        copy_btn.grid(row=0, column=0)

        copy_btn.bind("<Enter>", lambda e: copy_btn.configure(bg=self.colors['success']))
        copy_btn.bind("<Leave>", lambda e: copy_btn.configure(bg=self.colors['primary']))

        # Populate events
        all_events = []
        for day in self.days:
            if self.tasks[day]:
                all_events.append(f"\n{day}:")
                for task in sorted(self.tasks[day]):
                    all_events.append(f"  • {task}")

        events_text.insert("1.0", "No events scheduled." if not all_events else "\n".join(all_events))
        events_text.config(state="disabled")
        
    def copy_events(self, events_text):
        self.root.clipboard_clear()
        self.root.clipboard_append(events_text)
        self.root.update()
        messagebox.showinfo("Success", "Events copied to clipboard!")

    def bind_shortcuts(self):
        self.root.bind("<F1>", lambda event: self.open_terminal())
        self.root.bind("<F2>", lambda event: self.print_all_events())

def edit_task_hour(self, task_name, new_hour):
    for day in self.days:
        for task in self.tasks[day]:
            if task.split(": ", 1)[1] == task_name:
                old_task = task
                new_task = f"{new_hour}: {task_name}"
                self.tasks[day].remove(old_task)
                self.tasks[day].append(new_task)
                self.sort_tasks(day)
                messagebox.showinfo("Success", f"Updated hour for '{task_name}' to {new_hour}.")
                return
    messagebox.showerror("Error", f"Task '{task_name}' not found.")

def edit_task_name(self, old_name, new_name):
    for day in self.days:
        for task in self.tasks[day]:
            if task.split(": ", 1)[1] == old_name:
                hour = task.split(": ")[0]
                old_task = task
                new_task = f"{hour}: {new_name}"
                self.tasks[day].remove(old_task)
                self.tasks[day].append(new_task)
                self.sort_tasks(day)
                messagebox.showinfo("Success", f"Updated task name from '{old_name}' to '{new_name}'.")
                return
    messagebox.showerror("Error", f"Task '{old_name}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAppDesign(root)
    root.mainloop()