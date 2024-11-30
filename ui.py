# ui.py
from tkinter import ttk, messagebox
from functions import TaskManager
import tkinter as tk


class ModernAppDesign(TaskManager):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Smart Schedule")
        self.root.geometry("1024x768")
        self.root.config(bg="#ffffff")

        self.colors = {
            'primary': '#7c3aed',
            'secondary': '#a78bfa',
            'success': '#6d28d9',
            'background': '#ffffff',
            'surface': '#f5f3ff',
            'text': '#4c1d95',
            'border': '#ddd6fe'
        }

        self.configure_styles()
        self.create_ui()
        self.bind_shortcuts()

    def configure_styles(self):
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
        main_container = ttk.Frame(self.root, style="Card.TFrame", padding="20")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

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

        days_frame = ttk.Frame(main_container, style="Card.TFrame")
        days_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1, uniform="column")
        days_frame.grid_rowconfigure(0, weight=1)

        for i, day in enumerate(self.days):
            day_frame = tk.Frame(
                days_frame,
                bg=self.colors['background'],
                highlightthickness=1,
                highlightbackground=self.colors['border']
            )
            day_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

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
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['success']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['primary']))

    def bind_shortcuts(self):
        self.root.bind("<F1>", lambda event: self.open_terminal())
        self.root.bind("<F2>", lambda event: self.print_all_events())
