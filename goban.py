import enum
from os import lstat
from types import resolve_bases


class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4


class Goban(object):
    def __init__(self, goban):
        self.goban = goban

    def get_status(self, x, y):
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
            not self.goban
            or x < 0
            or y < 0
            or y >= len(self.goban)
            or x >= len(self.goban[0])
        ):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK

    def is_taken(self, x, y):
        start_color = self.get_status(x, y)
        allies = self.check_allies([[x, y]], start_color)
        taken = self.check_liberties(allies)
        
        return taken

    """
        This function will check all existing neighors ally
        
        Return a list of allies
    """
    def check_allies(self, allies, start_color):
        list_allies = allies
        
        while True:
            tmp_allies = []

            for ally in allies:
                pos = self.define_pos(ally[0], ally[1])

                for value in pos:
                    if self.get_status(value[0], value[1]) == start_color:
                        
                        # Important to check if the ally exist or not otherwise we can be stuck in Infinite loop
                        if value not in list_allies:
                            tmp_allies.append(value)
                            list_allies.append(value)

            if len(tmp_allies) == 0:
                break
            else:
                allies = tmp_allies
        
        return list_allies

    """
        Check if Status.EMPTY is available
        For all allies we will check each position defined in defined_pos(x, y)
        then if the coordinate status is EMPTY it means not taken
    """
    def check_liberties(self, allies):
        is_empty = True
        
        for ally in allies:
            pos = self.define_pos(ally[0], ally[1])
            
            for value in pos:
                if self.get_status(value[0], value[1]) == Status.EMPTY:
                    is_empty = False
        
        return is_empty
    
    """
        Define dynamically all position (upper, bottom, right, left) 
        depending on the given paramter (x, y)
    """
    def define_pos(self, x, y):
        pos = [
            [x, y + 1],
            [x, y - 1],
            [x + 1, y],
            [x - 1, y]
        ]
        
        return pos