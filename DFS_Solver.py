from Game import Game
from typing import Optional

class DFS_Solver:
    
    def __init__(self, initial_game: Game, max_nodes=None):
        self.initial_game = initial_game
        self.solution_found = None
        self.visited_count = 0
        self.max_depth = 0
        self.max_nodes = max_nodes if max_nodes else float('inf')
        self.solution_path = []
        self.parent_map = {}
    
    def solve(self) -> Optional[Game]:
        print("\nStarting DFS Search...")
        print(f"Board: {self.initial_game.board.rows}x{self.initial_game.board.cols}, Colors: {len(self.initial_game.board.positions)}")
        
        self.visited_count = 0
        self.max_depth = 0
        self.solution_found = None
        self.solution_path = []
        self.parent_map = {}
        
        self.initial_game.visited_states.clear()
        
        result = self._dfs_iterative()
        
        print(f"\nDFS Complete: {self.visited_count:,} states visited, max depth: {self.max_depth}")
        
        if result:
            print("Solution found!")
            return result
        else:
            print("No solution found")
            return None
    
    def _dfs_iterative(self) -> Optional[Game]:
        """
        Iterative DFS using explicit stack (LIFO)
        Stack stores tuples of (state, depth)
        """
        
        # Initialize stack with initial state
        stack = [(self.initial_game, 0)]
        self.initial_game.MarkAsVisited()
        
        # Track parent relationships for path reconstruction
        state_hash = self._hash_state(self.initial_game)
        self.parent_map[state_hash] = None
        
        # Process stack until empty
        while stack:
            # Check node limit
            if self.visited_count >= self.max_nodes:
                return None
            
            # Pop from stack (LIFO - Last In First Out)
            current_state, depth = stack.pop()
            self.visited_count += 1
            
            # Update max depth
            if depth > self.max_depth:
                self.max_depth = depth
            
            # Check if this is the final state
            if current_state.IsFinalState():
                self.solution_found = current_state
                self._reconstruct_path(current_state)
                return current_state
            
            # Check for dead ends (pruning optimization)
            if current_state.IsDeadEnd():
                continue
            
            # Get current state hash for parent tracking
            current_hash = self._hash_state(current_state)
            
            # Get all unvisited next states
            next_states = current_state.GetPossibleMovesUnvisited()
            
            # Sort moves by heuristic (best moves first)
            next_states = self._sort_moves(current_state, next_states)
            
            # Add unvisited states to stack in REVERSE order
            # (so best move is processed first when we pop)
            for next_state in reversed(next_states):
                next_state.MarkAsVisited()
                stack.append((next_state, depth + 1))
                
                # Track parent relationship
                next_hash = self._hash_state(next_state)
                self.parent_map[next_hash] = current_state
        
        # Stack is empty, no solution found
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
    
    def _sort_moves(self, current_state: Game, moves: list) -> list:
        
        def score(next_state: Game) -> tuple:
            completes = 0
            for color in next_state.completed_colors:
                if color not in current_state.completed_colors:
                    completes = 1
                    break
            
            total_dist = 0
            for color, path in next_state.paths.items():
                if color in next_state.completed_colors:
                    continue
                if color not in next_state.board.positions:
                    continue
                
                pos = path[-1]
                end = tuple(next_state.board.positions[color]["end"])
                dist = abs(pos[0] - end[0]) + abs(pos[1] - end[1])
                total_dist += dist
            
            path_len = sum(len(p) for p in next_state.paths.values())
            
            return (completes, -total_dist, -path_len)
        
        return sorted(moves, key=score, reverse=True)
    
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
        print(f"Max depth: {self.max_depth}")
        print(f"{'='*60}")