import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class ModernAppDesign:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Schedule")
        self.root.geometry("1024x768")
        self.root.config(bg="#ffffff")

        # Custom colors
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#6b7280',    # Gray
            'success': '#059669',      # Green
            'background': '#ffffff',   # White
            'surface': '#f3f4f6',     # Light gray
            'text': '#1f2937',        # Dark gray
            'border': '#e5e7eb'       # Light border
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
            ("Add Event (F1)", self.open_terminal),
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
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#1d4ed8"))
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
        action, event, day, hour = parts[0], parts[1], parts[2].capitalize(), parts[3]
        if action == "add":
            self.add_task(event, day, hour)
        elif action == "delete":
            self.delete_task(event, day, hour)
        else:
            messagebox.showerror("Error", "Invalid action. Use 'add' or 'delete'.")

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

        # Center the window
        events_window.geometry("+%d+%d" % (
            self.root.winfo_x() + (self.root.winfo_width() - 600) // 2,
            self.root.winfo_y() + (self.root.winfo_height() - 400) // 2
        ))

        header = tk.Label(
            events_window,
            text="All Scheduled Events",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        header.pack(pady=20)

        # Create text widget with custom styling
        events_text = tk.Text(
            events_window,
            wrap="word",
            height=15,
            width=50,
            font=("Helvetica", 11),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            relief="flat",
            padx=15,
            pady=15
        )
        events_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        # Populate events
        all_events = []
        for day in self.days:
            if self.tasks[day]:
                all_events.append(f"\n{day}:")
                for task in sorted(self.tasks[day]):
                    all_events.append(f"  • {task}")

        events_text.insert("1.0", "No events scheduled." if not all_events else "\n".join(all_events))
        events_text.config(state="disabled")

        # Copy button with hover effect
        copy_btn = tk.Button(
            events_window,
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
        copy_btn.pack(pady=20)

        copy_btn.bind("<Enter>", lambda e: copy_btn.configure(bg="#1d4ed8"))
        copy_btn.bind("<Leave>", lambda e: copy_btn.configure(bg=self.colors['primary']))

    def copy_events(self, events_text):
        self.root.clipboard_clear()
        self.root.clipboard_append(events_text)
        self.root.update()
        messagebox.showinfo("Success", "Events copied to clipboard!")

    def bind_shortcuts(self):
        self.root.bind("<F1>", lambda event: self.open_terminal())
        self.root.bind("<F2>", lambda event: self.print_all_events())

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAppDesign(root)
    root.mainloop()