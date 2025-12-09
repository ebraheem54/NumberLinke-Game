from Game import Game
from typing import Optional

class BaseSolver:
   
    
    def __init__(self, initial_game: Game, max_nodes=None):
        self.initial_game = initial_game
        self.solution_found = None
        self.visited_count = 0
        self.max_nodes = max_nodes if max_nodes else float('inf')
        self.solution_path = []
        self.parent_map = {}
    
    def _hash_state(self, state: Game) -> str:
        """Create unique hash for a state"""
        return str(state.board.grid.tobytes()) + str(state.paths)
    
    def _reconstruct_path(self, final_state: Game):
        """Reconstruct solution path from parent map"""
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
        """Print the solution path step by step"""
        if not self.solution_path:
            print("No solution to print")
            return
        
        print(f"\n{'='*60}")
        print(f"SOLUTION PATH ({len(self.solution_path)} states)")
        
        # Show cost if available (for UCS)
        if self.solution_path and hasattr(self.solution_path[-1], 'get_total_cost'):
            cost = self.solution_path[-1].get_total_cost()
            print(f"Total cost: {cost:.2f}")
        
        print(f"{'='*60}\n")
        
        for i, state in enumerate(self.solution_path):
            print(f"Step {i}:")
            state.board.printGrid()
            print()
        
        print(f"{'='*60}")
    
    def print_solution(self):
        """Print the final solution"""
        if self.solution_found is None:
            print("No solution found")
            return
        
        print("FINAL SOLUTION")
        print(f"{'='*60}")
        
        self.solution_found.board.printGrid()
        
        print("\nPaths:")
        for color, path in self.solution_found.paths.items():
            # Show cost if available (for UCS)
            if hasattr(self.solution_found, 'path_costs'):
                cost = self.solution_found.path_costs[color]
                print(f"  Color {color}: {len(path)} moves, cost: {cost:.2f} -> {path}")
            else:
                print(f"  Color {color}: {len(path)} moves -> {path}")
        
        # Show total cost if available (for UCS)
        if hasattr(self.solution_found, 'get_total_cost'):
            print(f"\nBest total cost: {self.solution_found.get_total_cost():.2f}")
        
        print(f"\nStates explored: {self.visited_count:,}")
        
        # Show algorithm-specific metrics
        if hasattr(self, 'max_depth'):
            print(f"Max depth: {self.max_depth}")
        if hasattr(self, 'max_queue_size'):
            print(f"Max queue size: {self.max_queue_size:,}")
        
        print(f"{'='*60}")