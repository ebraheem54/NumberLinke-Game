from Game import Game
from BaseSolver import BaseSolver
from typing import Optional
import heapq

class UCS_Solver(BaseSolver):
    
    def __init__(self, initial_game: Game, max_nodes=None):
        super().__init__(initial_game, max_nodes)
        self.max_queue_size = 0
    
    def solve(self) -> Optional[Game]:
        print("\nStarting UCS Search...")
        print(f"Board: {self.initial_game.board.rows}x{self.initial_game.board.cols}, Colors: {len(self.initial_game.board.positions)}")
        
        self.visited_count = 0
        self.max_queue_size = 0
        self.solution_found = None
        self.solution_path = []
        self.parent_map = {}
        
        self.initial_game.visited_states.clear()
        result = self._ucs_iterative()
        
        print(f"\nUCS Complete: {self.visited_count:,} states visited, max queue: {self.max_queue_size:,}")
        
        if result:
            print("Solution found!")
            print(f"Best cost: {result.get_total_cost():.2f}")
            return result
        else:
            print("No solution found")
            return None
    
    def _ucs_iterative(self) -> Optional[Game]:
        priority_queue = []
        counter = 0
        
        initial_cost = self.initial_game.get_total_cost()
        heapq.heappush(priority_queue, (initial_cost, counter, self.initial_game))
        counter += 1
        
        self.initial_game.MarkAsVisited()
        state_hash = self._hash_state(self.initial_game)
        self.parent_map[state_hash] = None
        
        best_cost = {state_hash: initial_cost}
        
        while priority_queue:
            if self.visited_count >= self.max_nodes:
                return None
            
            if len(priority_queue) > self.max_queue_size:
                self.max_queue_size = len(priority_queue)
            
            current_cost, _, current_state = heapq.heappop(priority_queue)
            self.visited_count += 1
            
            if current_state.IsFinalState():
                self.solution_found = current_state
                self._reconstruct_path(current_state)
                return current_state
            
            current_hash = self._hash_state(current_state)
            
            if current_cost > best_cost.get(current_hash, float('inf')):
                continue
            
            next_states = current_state.GetPossibleMoves()
            
            for next_state in next_states:
                next_hash = self._hash_state(next_state)
                next_cost = next_state.get_total_cost()
                
                if next_cost < best_cost.get(next_hash, float('inf')):
                    best_cost[next_hash] = next_cost
                    next_state.MarkAsVisited()
                    heapq.heappush(priority_queue, (next_cost, counter, next_state))
                    counter += 1
                    
                    self.parent_map[next_hash] = current_state
        
        return None