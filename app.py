"""
Flask application for managing events through a RESTful API.

This application demonstrates basic CRUD-style operations using
in-memory Python objects. It supports creating, updating, and deleting
events through POST, PATCH, and DELETE requests.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

class Event:
    """
    Represent an event with an ID and title.

    Attributes:
        id (int): Unique identifier for the event.
        title (str): Name of the event.
    """

    def __init__(self, id, title):
        """
        Initialize a new Event instance.

        Args:
            id (int): Unique identifier for the event.
            title (str): Name of the event.
        """
        self.id = id
        self.title = title

    def to_dict(self):
        """
        Convert the Event object into a dictionary.

        Returns:
            dict: Dictionary containing the event ID and title.
        """
        return {"id": self.id, "title": self.title}

# In-memory "database" (used to simulate a database)
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["POST"])
def create_event():
    """
    Create a new event from JSON request data.

    The request must include a "title" field. A new unique event ID
    is generated based on the highest existing event ID.

    Returns:
        Response: JSON representation of the new event with status 201.
        Response: JSON error message with status 400 if title is missing.
    """
    data = request.get_json()

    # Validate that the request includes a title
    if not "title" in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate the next available event ID
    new_id = max((e.id for e in events), default=0) + 1

    # Create and store the new event
    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """
    Update the title of an existing event.

    Args:
        event_id (int): ID of the event to update.

    Returns:
        Response: JSON representation of the updated event.
        Response: JSON error message with status 404 if event is not found.
        Response: JSON error message with status 400 if title is missing.
    """
    data = request.get_json()

    # Search for the requested event
    event = next((e for e in events if e.id == event_id), None)

    # Return an error if the event does not exist
    if not event:
        return  jsonify({"error": "event not found"}), 404

    # Validate that a title was provided
    if "title" not in data:
        return jsonify({"error": "Title not found"}), 400

    # Update the event title
    event.title = data["title"]

    return jsonify(event.to_dict())

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Delete an existing event.

    Args:
        event_id (int): ID of the event to delete.

    Returns:
        Response: Empty response with status 204 when deletion succeeds.
        Response: JSON error message with status 404 if event is not found.
    """
    global events

    # Search for the requested event
    event = next((e for e in events if e.id == event_id), None)

    # Return an error if the event does not exist
    if not event:
        return  jsonify({"error": "event not found"}), 404

    # Remove the matching event from the in-memory list
    events = [e for e in events if e.id != event_id]

    return jsonify(), 204

if __name__ == "__main__":
    app.run(debug=True)
