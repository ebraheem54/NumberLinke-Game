from Game import Game
from typing import Optional
from collections import deque

class BFS_Solver:
    
    def __init__(self, initial_game: Game, max_nodes=None):
        self.initial_game = initial_game
        self.solution_found = None
        self.visited_count = 0
        self.max_queue_size = 0
        self.max_nodes = max_nodes if max_nodes else float('inf')
        self.solution_path = []
        self.parent_map = {}
    
    def solve(self) -> Optional[Game]:
        print("\nStarting BFS Search...")
        print(f"Board: {self.initial_game.board.rows}x{self.initial_game.board.cols}, Colors: {len(self.initial_game.board.positions)}")
        
        self.visited_count = 0
        self.max_queue_size = 0
        self.solution_found = None
        self.solution_path = []
        self.parent_map = {}
        
        self.initial_game.visited_states.clear()
        result = self._bfs_iterative()
        
        print(f"\nBFS Complete: {self.visited_count:,} states visited, max queue: {self.max_queue_size:,}")
        
        if result:
            print("Solution found!")
            return result
        else:
            print("No solution found")
            return None
    
    def _bfs_iterative(self) -> Optional[Game]:
        # Initialize queue
        queue = deque()
        queue.append(self.initial_game)
        self.initial_game.MarkAsVisited()
        
        state_hash = self._hash_state(self.initial_game)
        self.parent_map[state_hash] = None
        
        while queue:
            if self.visited_count >= self.max_nodes:
                return None
            
            if len(queue) > self.max_queue_size:
                self.max_queue_size = len(queue)
            
            # Dequeue (FIFO)
            current_state = queue.popleft()
            self.visited_count += 1
            
            if current_state.IsFinalState():
                self.solution_found = current_state
                self._reconstruct_path(current_state)
                return current_state
            
            current_hash = self._hash_state(current_state)
            next_states = current_state.GetPossibleMovesUnvisited()
            
            for next_state in next_states:
                next_state.MarkAsVisited()
                queue.append(next_state)
                
                next_hash = self._hash_state(next_state)
                self.parent_map[next_hash] = current_state
        
        return None
    
    def _hash_state(self, state: Game) -> str:
        return str(state.board.grid.tobytes()) + str(state.paths)
    
    def _reconstruct_path(self, final_state: Game):
        path = []
        current = final_state
        current_hash = self._hash_state(current)
        
        while current_hash in self.parent_map:
            path.append(current)
            parent = self.parent_map[current_hash]
            if parent is None:
                break
            current = parent
            current_hash = self._hash_state(current)
        
        path.reverse()
        self.solution_path = path
    
    def print_solution_path(self):
        if not self.solution_path:
            print("No solution to print")
            return
        
        print(f"\n{'='*60}")
        print(f"SOLUTION PATH ({len(self.solution_path)} states)")
        print(f"{'='*60}\n")
        
        for i, state in enumerate(self.solution_path):
            print(f"Step {i}:")
            state.board.printGrid()
            print()
        
        print(f"{'='*60}")
    
    def print_solution(self):
        if self.solution_found is None:
            print("No solution found")
            return
        
        print("FINAL SOLUTION")
        print(f"{'='*60}")
        self.solution_found.board.printGrid()
    
        print("\nPaths:")
        for color, path in self.solution_found.paths.items():
            print(f"  Color {color}: {len(path)} moves -> {path}")
        
        print(f"\nStates explored: {self.visited_count:,}")
        print(f"Max queue size: {self.max_queue_size:,}")
        print(f"{'='*60}")