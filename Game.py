from typing import List, Optional
from Board import Board

class Game:
    def __init__(self, board: Board):
        self.board = board
        self.paths = {}
        self.path_costs = {}  # NEW: For UCS
        self.visited_states = set()
        self.current_color: Optional[int] = None
        self.completed_colors = set()

        for color, pos in self.board.positions.items():
            self.paths[color] = [tuple(pos["start"])]
            self.path_costs[color] = 0.0  # NEW: For UCS
    
    def _idx(self, row, col):
        return row * self.board.cols + col
    
    # NEW: For UCS
    def get_total_cost(self) -> float:
        return sum(self.path_costs.values())
    
    def GetPossibleMoves(self) -> List['Game']:
        next_states = []
        
        for color, path in self.paths.items():
            if color in self.completed_colors:
                continue
            
            cur = path[-1]
            end = tuple(self.board.positions[color]["end"])
            
            if cur == end:
                continue
            
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = cur[0] + dr, cur[1] + dc
                
                if not (0 <= nr < self.board.rows and 0 <= nc < self.board.cols):
                    continue
                
                cell = self.board.grid[self._idx(nr, nc)]
                
                if cell == 0 or ((nr, nc) == end and cell == color):
                    if (nr, nc) not in path:
                        # NEW: Get weight for UCS
                        move_cost = self.board.get_weight(nr, nc) if hasattr(self.board, 'get_weight') else 1.0
                        
                        self.ApplyMove(color, (nr, nc), move_cost)
                        
                        if not self.IsVisitedState():
                            self.UndoMove(color, move_cost)
                            new_state = self.CopyState()
                            new_state.ApplyMove(color, (nr, nc), move_cost)
                            next_states.append(new_state)
                        else:
                            self.UndoMove(color, move_cost)
        
        return next_states
    
    def IsFinalState(self) -> bool:
        return len(self.completed_colors) == len(self.board.positions)
    
    def GetHashOfState(self):
        grid_bytes = self.board.grid.tobytes()
        paths_data = tuple((color, path[-1]) for color, path in sorted(self.paths.items()))
        return (grid_bytes, paths_data)
    
    def IsVisitedState(self) -> bool:
        return self.GetHashOfState() in self.visited_states
    
    def MarkAsVisited(self):
        self.visited_states.add(self.GetHashOfState())
    
    def CopyState(self) -> 'Game':
        new_board = Board(self.board.cols, self.board.rows, self.board.num_colors)
        new_board.grid = self.board.grid.copy()
        new_board.positions = self.board.positions
        
        # NEW: Copy weights if they exist (for UCS)
        if hasattr(self.board, 'weights'):
            new_board.weights = self.board.weights.copy()
        
        new_game = Game.__new__(Game)
        new_game.board = new_board
        new_game.paths = {color: path.copy() for color, path in self.paths.items()}
        new_game.path_costs = self.path_costs.copy()  # NEW: For UCS
        new_game.completed_colors = self.completed_colors.copy()
        new_game.visited_states = self.visited_states
        new_game.current_color = self.current_color
        
        return new_game
    
    def ApplyMove(self, color: int, pos: tuple, cost: float = 1.0):  # NEW: cost parameter
        end = tuple(self.board.positions[color]["end"])
        self.paths[color].append(pos)
        self.path_costs[color] += cost  # NEW: Track cost
        
        if pos != end:
            self.board.grid[self._idx(pos[0], pos[1])] = color
        else:
            self.completed_colors.add(color)
    
    def UndoMove(self, color: int, cost: float = 1.0):  # NEW: cost parameter
        if not self.paths[color]:
            return
        
        last = self.paths[color].pop()
        self.path_costs[color] -= cost  # NEW: Undo cost
        end = tuple(self.board.positions[color]["end"])
        
        if last != end:
            self.board.grid[self._idx(last[0], last[1])] = 0
        else:
            self.completed_colors.discard(color)
    
    def IsDeadEnd(self) -> bool:
        for color, path in self.paths.items():
            if color in self.completed_colors:
                continue
            
            end = tuple(self.board.positions[color]["end"])
            current = path[-1]
            
            if current != end:
                er, ec = end
                end_cell = self.board.grid[self._idx(er, ec)]
                
                if end_cell != color and end_cell != 0:
                    return True
                
                free_neighbors = 0
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = er + dr, ec + dc
                    if 0 <= nr < self.board.rows and 0 <= nc < self.board.cols:
                        cell = self.board.grid[self._idx(nr, nc)]
                        if cell == 0 or cell == color:
                            free_neighbors += 1
                
                if free_neighbors == 0:
                    if abs(current[0] - er) + abs(current[1] - ec) > 1:
                        return True
        
        return False
    
    def isGameCompleted(self):
        return self.IsFinalState()
    
    def GetCompletionPercentage(self):
        total = len(self.board.positions)
        done = len(self.completed_colors)
        return (done / total) * 100 if total > 0 else 0.0
    
    def resetGame(self):
        self.board.resetGrid()
        self.paths = {}
        self.path_costs = {}  # NEW: Reset costs
        self.completed_colors = set()
        for color, pos in self.board.positions.items():
            self.paths[color] = [tuple(pos["start"])]
            self.path_costs[color] = 0.0  # NEW: Initialize cost
        self.visited_states.clear()
        self.current_color = None
    
    def choose_color_to_play(self) -> bool:
        available = [c for c in self.paths if c not in self.completed_colors]
        if not available:
            print("No colors remaining.")
            return False

        print("Available colors to play:", available)
        try:
            choice = int(input("Choose a color number to play (or -1 to cancel): "))
        except:
            return False

        if choice == -1 or choice not in available:
            return False

        self.current_color = choice
        return True
    
    def getMovesAsDirections(self, color):
        if color not in self.paths or color in self.completed_colors:
            return []
        
        dirs = []
        cur = self.paths[color][-1]
        end = tuple(self.board.positions[color]["end"])
        
        for direction, (dr, dc) in [("UP", (-1, 0)), ("DOWN", (1, 0)), 
                                      ("LEFT", (0, -1)), ("RIGHT", (0, 1))]:
            nr, nc = cur[0] + dr, cur[1] + dc
            
            if not (0 <= nr < self.board.rows and 0 <= nc < self.board.cols):
                continue
            
            cell = self.board.grid[self._idx(nr, nc)]
            
            if cell == 0 or ((nr, nc) == end and cell == color):
                if (nr, nc) not in self.paths[color]:
                    dirs.append(direction)
        
        return dirs
    
    def printGameStatus(self):
        print("\n=== CURRENT GAME STATE ======")
        self.board.printGrid()
        print(f"\nSelected color: {self.current_color}")
        print("\nPaths:")
        for color, path in self.paths.items():
            end = tuple(self.board.positions[color]["end"])
            status = "COMPLETE" if path[-1] == end else "INCOMPLETE"
            print(f"  Color {color}: Path={path} [{status}]")
        print(f"\nCompletion: {self.GetCompletionPercentage():.2f}%")
        print("========================================================\n")
    
    def move(self, direction: str):
        if self.current_color is None:
            return None

        deltas = {
            "up": (-1, 0), "down": (1, 0),
            "left": (0, -1), "right": (0, 1)
        }

        if direction not in deltas:
            return None

        dr, dc = deltas[direction]
        cur = self.paths[self.current_color][-1]
        nr, nc = cur[0] + dr, cur[1] + dc

        if not self.board.isValidPosition(nr, nc):
            return None

        cell = self.board.getCell(nr, nc)
        end = tuple(self.board.positions[self.current_color]["end"])

        if cell == 0 or ((nr, nc) == end and cell == self.current_color):
            if (nr, nc) in self.paths[self.current_color]:
                return None

            self.ApplyMove(self.current_color, (nr, nc))

            if (nr, nc) == end:
                self.current_color = None
                return "completed"

            return None

        return None