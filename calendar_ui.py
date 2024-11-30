import tkinter as tk
from tkinter import ttk, font
import calendar
from datetime import datetime, timedelta

class CalendarApp:
    def __init__(self, master, event_manager):
        self.master = master
        self.event_manager = event_manager
        self.master.title("Smart Calendar")
        self.master.geometry("1200x800")
        self.master.configure(bg="#f0f4f8")

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.day_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.event_font = font.Font(family="Helvetica", size=10)

        # Color scheme
        self.colors = {
            "bg": "#f0f4f8",
            "fg": "#2c3e50",
            "highlight": "#3498db",
            "button": "#2980b9",
            "button_active": "#1c6ea4"
        }

        # Frame to hold the calendar
        self.calendar_frame = tk.Frame(master, bg=self.colors["bg"])
        self.calendar_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Current date tracking
        self.current_date = datetime.now()
        self.current_week_start = self.get_week_start(self.current_date)

        # Create week view
        self.create_week_view()

        # Navigation buttons
        self.create_navigation_buttons()

    def get_week_start(self, date):
        return date - timedelta(days=date.weekday())

    def create_week_view(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create frames for each day
        self.day_frames = {}
        for i, day_name in enumerate(days):
            day_date = self.current_week_start + timedelta(days=i)
            day_str = day_date.strftime("%Y-%m-%d")

            day_frame = tk.Frame(
                self.calendar_frame,
                bg=self.colors["bg"],
                highlightbackground=self.colors["highlight"],
                highlightthickness=1
            )
            day_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            
            self.calendar_frame.grid_columnconfigure(i, weight=1)
            self.calendar_frame.grid_rowconfigure(0, weight=1)

            # Day header
            day_header = tk.Frame(day_frame, bg=self.colors["highlight"])
            day_header.pack(fill=tk.X)

            tk.Label(
                day_header,
                text=f"{day_name}\n{day_date.strftime('%d %b')}",
                font=self.day_font,
                bg=self.colors["highlight"],
                fg="white",
                pady=5
            ).pack(fill=tk.X)

            # Scrollable canvas for events
            canvas = tk.Canvas(day_frame, bg=self.colors["bg"])
            scrollbar = ttk.Scrollbar(day_frame, orient="vertical", command=canvas.yview)
            event_frame = tk.Frame(canvas, bg=self.colors["bg"])

            canvas.create_window((0, 0), window=event_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            event_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))

            # Store reference
            self.day_frames[day_str] = {
                'frame': event_frame,
                'canvas': canvas
            }

        # Populate events
        self.update_calendar()

    def update_calendar(self):
        for day_date, day_info in self.day_frames.items():
            event_frame = day_info['frame']
            canvas = day_info['canvas']

            # Clear existing events
            for widget in event_frame.winfo_children():
                widget.destroy()

            # Retrieve and display events
            events = self.event_manager.get_events_for_date(day_date)
            if events:
                for event in events:
                    event_label = tk.Label(
                        event_frame,
                        text=f"{event['time']}: {event['description']}",
                        font=self.event_font,
                        bg=self.colors["bg"],
                        fg=self.colors["fg"],
                        wraplength=150,
                        justify="left",
                        pady=5
                    )
                    event_label.pack(fill=tk.X, padx=5)
            else:
                tk.Label(
                    event_frame,
                    text="No events",
                    font=self.event_font,
                    bg=self.colors["bg"],
                    fg=self.colors["fg"]
                ).pack(pady=10)

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self.master, bg=self.colors["bg"])
        nav_frame.pack(pady=10)

        button_style = {
            "font": self.day_font,
            "bg": self.colors["button"],
            "fg": "white",
            "activebackground": self.colors["button_active"],
            "activeforeground": "white",
            "relief": tk.FLAT,
            "padx": 15,
            "pady": 5
        }

        prev_week_btn = tk.Button(nav_frame, text="◀ Previous Week", command=self.prev_week, **button_style)
        prev_week_btn.pack(side=tk.LEFT, padx=5)

        next_week_btn = tk.Button(nav_frame, text="Next Week ▶", command=self.next_week, **button_style)
        next_week_btn.pack(side=tk.LEFT, padx=5)

    def prev_week(self):
        self.current_week_start -= timedelta(days=7)
        self.create_week_view()

    def next_week(self):
        self.current_week_start += timedelta(days=7)
        self.create_week_view()