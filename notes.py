from datetime import datetime

class Note:
    def __init__(self):
        self.pieces = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_timestamp = self.timestamp

class Piece:
    def __init__(self, content: str):
        self.text = content
        self.timestamp = datetime.now().strftime


