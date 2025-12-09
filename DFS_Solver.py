from Game import Game
from BaseSolver import BaseSolver
from typing import Optional

class DFS_Solver(BaseSolver):
    
    def __init__(self, initial_game: Game, max_nodes=None):
        super().__init__(initial_game, max_nodes)
        self.max_depth = 0
    
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
        stack = [(self.initial_game, 0)]
        self.initial_game.MarkAsVisited()
        
        state_hash = self._hash_state(self.initial_game)
        self.parent_map[state_hash] = None
        
        while stack:
            if self.visited_count >= self.max_nodes:
                return None
            
            current_state, depth = stack.pop()
            self.visited_count += 1
            
            if depth > self.max_depth:
                self.max_depth = depth
            
            if current_state.IsFinalState():
                self.solution_found = current_state
                self._reconstruct_path(current_state)
                return current_state
            
            if current_state.IsDeadEnd():
                continue
            
            current_hash = self._hash_state(current_state)
            next_states = current_state.GetPossibleMoves()
            next_states = self._sort_moves(current_state, next_states)
            
            for next_state in reversed(next_states):
                next_state.MarkAsVisited()
                stack.append((next_state, depth + 1))
                
                next_hash = self._hash_state(next_state)
                self.parent_map[next_hash] = current_state
        
        return None
    
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