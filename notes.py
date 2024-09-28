from datetime import datetime
from typing import List


class Note:
    def __init__(self):
        self.pieces: List[Piece] = []
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_timestamp : str = self.timestamp

class Piece:
    def __init__(self, content: str):
        self.text : str = content
        self.timestamp : str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


