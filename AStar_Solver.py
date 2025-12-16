from Game import Game
from BaseSolver import BaseSolver
from typing import Optional
import heapq

class AStar_Solver(BaseSolver):
    
    def __init__(self, initial_game: Game, max_nodes=None):
        super().__init__(initial_game, max_nodes)
        self.max_queue_size = 0
    
    def solve(self) -> Optional[Game]:
        print("\nStarting A* Search...")
        print(f"Board: {self.initial_game.board.rows}x{self.initial_game.board.cols}, Colors: {len(self.initial_game.board.positions)}")
        
        self.visited_count = 0
        self.max_queue_size = 0
        self.solution_found = None
        self.solution_path = []
        self.parent_map = {}
        
        self.initial_game.visited_states.clear()
        result = self._astar_search()
        
        print(f"\nA* Complete: {self.visited_count:,} states visited, max queue: {self.max_queue_size:,}")
        
        if result:
            print("Solution found!")
            return result
        else:
            print("No solution found")
            return None
    
    def _astar_search(self) -> Optional[Game]:
        priority_queue = []
        counter = 0
        
        # F(n) = G(n) + H(n)
        g_cost = self.initial_game.get_total_cost()  # G(n) = actual cost from start
        h_cost = self._calculate_heuristic(self.initial_game)  # H(n) = estimated cost to goal
        f_cost = g_cost + h_cost  # F(n) = total estimated cost
        
        heapq.heappush(priority_queue, (f_cost, counter, self.initial_game))
        counter += 1
        
        self.initial_game.MarkAsVisited()
        state_hash = self._hash_state(self.initial_game)
        self.parent_map[state_hash] = None
        
        # Track best f_cost for each state
        best_f_cost = {state_hash: f_cost}
        
        while priority_queue:
            if self.visited_count >= self.max_nodes:
                return None
            
            if len(priority_queue) > self.max_queue_size:
                self.max_queue_size = len(priority_queue)
            
            current_f_cost, _, current_state = heapq.heappop(priority_queue)
            self.visited_count += 1
            
            # Check if reached goal
            if current_state.IsFinalState():
                self.solution_found = current_state
                self._reconstruct_path(current_state)
                return current_state
            
            current_hash = self._hash_state(current_state)
            
            # Skip if we found better path to this state already
            if current_f_cost > best_f_cost.get(current_hash, float('inf')):
                continue
            
            # Get all possible next states
            next_states = current_state.GetPossibleMoves()
            
            for next_state in next_states:
                next_hash = self._hash_state(next_state)
                
                # Calculate costs for next state
                g_next = next_state.get_total_cost()  # G(n) = actual cost from start
                h_next = self._calculate_heuristic(next_state)  # H(n) = estimated cost to goal
                f_next = g_next + h_next  # F(n) = total estimated cost
                
                # Only add if this is better path to this state
                if f_next < best_f_cost.get(next_hash, float('inf')):
                    best_f_cost[next_hash] = f_next
                    next_state.MarkAsVisited()
                    heapq.heappush(priority_queue, (f_next, counter, next_state))
                    counter += 1
                    
                    self.parent_map[next_hash] = current_state
        
        return None
    
    def _calculate_heuristic(self, state: Game) -> float:
        """
        H(n) = Heuristic estimate of cost from current state to goal.
        Uses Manhattan distance for all incomplete colors.
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
        
        return float(total_distance)
    
    def _get_manhattan_distance(self, pos1: tuple, pos2: tuple) -> int:
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def print_solution(self):
        """Print the final solution"""
        if self.solution_found is None:
            print("No solution found")
            return
        
        print("\nFINAL SOLUTION")
        print("="*60)
        
        self.solution_found.board.printGrid()
        
        print("\nPaths:")
        for color, path in self.solution_found.paths.items():
            cost = self.solution_found.path_costs[color]
            print(f"  Color {color}: {len(path)} moves, cost: {cost:.2f} -> {path}")
        
        # Show costs breakdown
        g_cost = self.solution_found.get_total_cost()
        h_cost = self._calculate_heuristic(self.solution_found)
        f_cost = g_cost + h_cost
        
        print(f"\nG(n) - Actual cost from start: {g_cost:.2f}")
        print(f"H(n) - Heuristic to goal: {h_cost:.2f}")
        print(f"F(n) - Total estimated cost: {f_cost:.2f}")
        
        print(f"\nStates explored: {self.visited_count:,}")
        print(f"Max queue size: {self.max_queue_size:,}")
        print("="*60)