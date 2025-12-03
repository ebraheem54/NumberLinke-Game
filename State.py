class State:
    visited = set()   
    def __init__(self, board, current_color=None, current_position=None, completed_colors=None):
        self.board = board
        self.grid = board.grid.copy()
        self.positions = board.positions
        self.current_color = current_color
        self.current_position = current_position
        self.completed_colors = set(completed_colors) if completed_colors else set()
        self.directions = {"up":(-1,0),"down":(1,0),"left":(0,-1),"right":(0,1)}

  

    def IsFinalState(self):
        return len(self.completed_colors) == len(self.positions)
 

    def IsVisitedState(self):
        return self.GetHashOfState() in State.visited

    def MarkAsVisited(self):
        State.visited.add(self.GetHashOfState())

 