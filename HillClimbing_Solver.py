from Game import Game
from BaseSolver import BaseSolver
from typing import Optional

class HillClimbing_Solver(BaseSolver):
    
    def __init__(self, initial_game: Game, max_nodes=None):
        super().__init__(initial_game, max_nodes)
        self.stuck_at_local_max = False
        self.final_reached_state = None
    
    def solve(self) -> Optional[Game]:
        print("\nStarting Hill Climbing Search...")
        print(f"Board: {self.initial_game.board.rows}x{self.initial_game.board.cols}, Colors: {len(self.initial_game.board.positions)}")
        
        self.visited_count = 0
        self.solution_found = None
        self.solution_path = []
        self.parent_map = {}
        self.stuck_at_local_max = False
        self.final_reached_state = None
        
        self.initial_game.visited_states.clear()
        result = self._hill_climbing_search()
        
        print(f"\nHill Climbing Complete: {self.visited_count:,} states visited")
        
        if result:
            print("Solution found!")
            return result
        else:
            if self.stuck_at_local_max:
                print("Stuck at local maximum - no solution found")
                print("Algorithm stopped because all neighbors have worse evaluation")
            else:
                print("No solution found")
            return None
    
    def _hill_climbing_search(self) -> Optional[Game]:
        current_state = self.initial_game
        current_state.MarkAsVisited()
        
        state_hash = self._hash_state(current_state)
        self.parent_map[state_hash] = None
        
        while True:
            if self.visited_count >= self.max_nodes:
                self.final_reached_state = current_state
                return None
            
            self.visited_count += 1
            
            # Check if we reached the goal
            if current_state.IsFinalState():
                self.solution_found = current_state
                self._reconstruct_path(current_state)
                self.final_reached_state = current_state
                return current_state
            
            # Get current evaluation
            current_eval = self._evaluate(current_state)
            
            # Get all possible next states
            next_states = current_state.GetPossibleMoves()
            
            if not next_states:
                # No moves available - stuck
                self.stuck_at_local_max = True
                self.final_reached_state = current_state
                return None
            
            # Find the best neighbor (lowest evaluation = closer to goal)
            best_state = None
            best_eval = float('inf')
            
            for next_state in next_states:
                next_eval = self._evaluate(next_state)
                if next_eval < best_eval:
                    best_eval = next_eval
                    best_state = next_state
            
            # Check if best neighbor is better than current
            if best_eval >= current_eval:
                # Stuck at local maximum
                self.stuck_at_local_max = True
                self.final_reached_state = current_state
                return None
            
            # Move to best neighbor
            current_hash = self._hash_state(current_state)
            best_state.MarkAsVisited()
            
            best_hash = self._hash_state(best_state)
            self.parent_map[best_hash] = current_state
            
            current_state = best_state
        
        return None
    
    def _evaluate(self, state: Game) -> float:
        """
        Calculate sum of Manhattan distances for all incomplete colors.
        Lower value = closer to goal = better state.
        """
        total_distance = 0
        
        for color, path in state.paths.items():
            # Skip completed colors
            if color in state.completed_colors:
                continue
            
            # Get current position and end position
            current_pos = path[-1]
            end_pos = tuple(state.board.positions[color]["end"])
            
            # Calculate Manhattan distance
            manhattan = self._get_manhattan_distance(current_pos, end_pos)
            total_distance += manhattan
        
        return total_distance
    
    def _get_manhattan_distance(self, pos1: tuple, pos2: tuple) -> int:
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def print_solution(self):
        """Print the final solution or last reached state"""
        if self.solution_found is None:
            print("\n" + "="*60)
            print("HILL CLIMBING - NO SOLUTION FOUND")
            print("="*60)
            
            if self.final_reached_state:
                print("\nLAST REACHED STATE (stuck at local maximum):")
                self.final_reached_state.board.printGrid()
                
                print("\nPaths:")
                for color, path in self.final_reached_state.paths.items():
                    status = "COMPLETE" if color in self.final_reached_state.completed_colors else "INCOMPLETE"
                    print(f"  Color {color}: {len(path)} moves [{status}] -> {path}")
                
                print(f"\nCompletion: {self.final_reached_state.GetCompletionPercentage():.2f}%")
                print(f"Final evaluation (Manhattan): {self._evaluate(self.final_reached_state)}")
                print(f"States explored: {self.visited_count:,}")
            
            print("="*60)
            return
        
        # If solution was found, print it
        print("\nFINAL SOLUTION")
        print("="*60)
        
        self.solution_found.board.printGrid()
        
        print("\nPaths:")
        for color, path in self.solution_found.paths.items():
            print(f"  Color {color}: {len(path)} moves -> {path}")
        
        print(f"\nStates explored: {self.visited_count:,}")
        print("="*60)