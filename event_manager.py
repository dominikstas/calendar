import json
import os
from typing import Dict, List

class EventManager:
    def __init__(self, events_file: str):
        """
        Initialize EventManager with a JSON file to store events
        
        :param events_file: Path to the JSON file storing events
        """
        self.events_file = events_file
        self.events = self.load_events()

    def load_events(self) -> Dict[str, List[Dict]]:
        """
        Load events from the JSON file
        
        :return: Dictionary of events by date
        """
        if os.path.exists(self.events_file):
            try:
                with open(self.events_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_events(self):
        """
        Save events to the JSON file
        """
        try:
            with open(self.events_file, 'w') as f:
                json.dump(self.events, f, indent=4)
        except IOError as e:
            print(f"Error saving events: {e}")

    def add_event(self, date: str, time: str, description: str):
        """
        Add an event to a specific date
        
        :param date: Date of the event (YYYY-MM-DD)
        :param time: Time of the event
        :param description: Event description
        """
        if date not in self.events:
            self.events[date] = []
        
        # Check for duplicate events
        for event in self.events[date]:
            if event['time'] == time and event['description'] == description:
                return  # Avoid duplicate events
        
        self.events[date].append({
            'time': time,
            'description': description
        })
        
        # Sort events by time
        self.events[date] = sorted(
            self.events[date], 
            key=lambda x: x['time']
        )
        
        self.save_events()

    def delete_event(self, date: str, time: str, description: str):
        """
        Delete a specific event
        
        :param date: Date of the event
        :param time: Time of the event
        :param description: Event description
        """
        if date in self.events:
            self.events[date] = [
                event for event in self.events[date]
                if not (
                    event['time'] == time and 
                    event['description'] == description
                )
            ]
            
            # Remove the date key if no events remain
            if not self.events[date]:
                del self.events[date]
            
            self.save_events()

    def get_events_for_date(self, date: str) -> List[Dict]:
        """
        Get events for a specific date
        
        :param date: Date to retrieve events for
        :return: List of events for the date
        """
        return self.events.get(date, [])

    def list_all_events(self):
        """
        List all events across all dates
        
        :return: Dictionary of all events
        """
        return self.events