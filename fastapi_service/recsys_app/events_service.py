"""Service for simulating new events in online history."""
from fastapi import FastAPI


class EventStore():
    """Class for adding/retrieving online history."""

    def __init__(self, max_events_per_user: int = 10):
        """Initializes a class instance."""
        self.events = {}
        self.max_events_per_user = max_events_per_user

    def put(self, user_id: int, item_id: int):
        """Adds a new event for a user to the online history."""
        user_events = [] if self.events.get(user_id) is None else self.events[user_id]
        self.events[user_id] = [item_id] + user_events[:self.max_events_per_user]

    def get(self, user_id: int, k: int = 5):
        """Retrieves online history."""
        user_events = self.events[user_id][:k] if user_id in self.events else []

        return user_events
    

# Instantiating an object
event_store = EventStore()

# Creating an app
app = FastAPI(title="events")

@app.get("/healthy")
async def healthy():
    """Displays status message."""
    return {
        "status": "healthy"
    }

# Integrating endpoints for the service
@app.post("/put")
async def put(user_id: int, item_id: int):
    """Add an event (item identifier) to the history."""
    event_store.put(user_id, item_id)
    
    return {"result": "OK"}

@app.post("/get")
async def get(user_id: int, k: int):
    """Retrieves user events from the history."""
    events = event_store.get(user_id, k)

    return {"events": events}
