from datetime import datetime


class PositionWithTime:
    """
    Object position with timestamp needed to store information for final result's position.
    """
    def __init__(self, x: float, y: float, timestamp: datetime):
        self.last_position_x = x
        self.last_position_y = y
        self.last_position_timestamp = timestamp.isoformat(sep=' ', timespec='milliseconds')
