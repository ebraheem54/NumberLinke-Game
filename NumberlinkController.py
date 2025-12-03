from Board import Board
from Game import Game
from DFS_Solver import DFS_Solver
from BFS_Solver import BFS_Solver
from ManualPlayer import ManualPlayer
import time

class NumberlinkController:
   
    def __init__(self):
        self.board = None
        self.dfs_solver = None
        self.dfs_time = None
        self.bfs_solver = None
        self.bfs_time = None

    def setup_board(self):
        print("\n=== BOARD SETUP ===")
        try:
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            num_colors = int(input("Enter number of colors: "))
        except ValueError:
            print("Invalid input")
            return False

        if rows < 2 or cols < 2 or num_colors < 1:
            print("Invalid dimensions")
            return False

        self.board = Board(cols, rows, num_colors)
        color_list = self.board.ColorsInputs(num_colors)
        if not color_list:
            return False

        print("\nEmpty board:")
        self.board.printGrid()
        
        positions = self.board.placeForColor(color_list)
        if not positions:
            return False
        
        print("\nInitial board:")
        self.board.printGrid()
        return True

    def run_dfs(self, max_nodes=None):
        game = Game(self.board)
        start = time.time()
        solver = DFS_Solver(game, max_nodes=max_nodes)
        solution = solver.solve()
        elapsed = time.time() - start

        if solution:
            solver.print_solution_path()
            solver.print_solution()
        
        return solver, elapsed

    def run_bfs(self, max_nodes=None):
        game = Game(self.board)
        start = time.time()
        solver = BFS_Solver(game, max_nodes=max_nodes)
        solution = solver.solve()
        elapsed = time.time() - start

        if solution:
            solver.print_solution_path()
            solver.print_solution()
        
        return solver, elapsed

    def compare_solvers(self):
        if not (self.dfs_solver and self.bfs_solver):
            print("Run both DFS and BFS first")
            return
        
        print("\n" + "="*60)
        print("ALGORITHM COMPARISON")
        print("="*60)
        
        dfs_found = self.dfs_solver.solution_found is not None
        bfs_found = self.bfs_solver.solution_found is not None
        
        # Format time display (show milliseconds if under 0.01s)
        def format_time(t):
            if t < 0.01:
                return f"{t*1000:.2f}ms"
            else:
                return f"{t:.3f}s"
        
        print(f"\n{'Metric':<30} {'DFS':>12} {'BFS':>12}")
        print("-"*60)
        print(f"{'Solution Found':<30} {str(dfs_found):>12} {str(bfs_found):>12}")
        print(f"{'States Explored':<30} {self.dfs_solver.visited_count:>12,} {self.bfs_solver.visited_count:>12,}")
        print(f"{'Time':<30} {format_time(self.dfs_time):>12} {format_time(self.bfs_time):>12}")
        
        if dfs_found and bfs_found:
            dfs_len = len(self.dfs_solver.solution_path)
            bfs_len = len(self.bfs_solver.solution_path)
            print(f"{'Path Length':<30} {dfs_len:>12} {bfs_len:>12}")
            
            dfs_moves = sum(len(p) - 1 for p in self.dfs_solver.solution_found.paths.values())
            bfs_moves = sum(len(p) - 1 for p in self.bfs_solver.solution_found.paths.values())
            print(f"{'Total Moves':<30} {dfs_moves:>12} {bfs_moves:>12}")
        
        print(f"{'Max Depth/Queue':<30} {self.dfs_solver.max_depth:>12} {self.bfs_solver.max_queue_size:>12,}")
        print("="*60)

    def start(self):
        print("="*60)
        print("NUMBERLINK GAME")
        print("="*60)
        
        if not self.setup_board():
            return

        while True:
            print("\n=== MENU ===")
            print("1 - Manual Play")
            print("2 - DFS Solver")
            print("3 - BFS Solver")
            if self.dfs_solver and self.bfs_solver:
                print("4 - Compare Results")
            print("5 - Exit")

            choice = input("\nChoice: ").strip()

            if choice == "1":
                ManualPlayer(Game(self.board)).start()
                
            elif choice == "2":   
                print("\nRunning DFS Solver...")
                self.dfs_solver, self.dfs_time = self.run_dfs()
                
                if self.dfs_solver.solution_found:
                    if input("\nRun BFS for comparison? (y/n): ").lower() == 'y':
                        self.bfs_solver, self.bfs_time = self.run_bfs()
                        if self.bfs_solver.solution_found:
                            self.compare_solvers()
                
            elif choice == "3":
                print("\nRunning BFS Solver...")
                self.bfs_solver, self.bfs_time = self.run_bfs()
                
                if self.bfs_solver.solution_found:
                    if input("\nRun DFS for comparison? (y/n): ").lower() == 'y':
                        self.dfs_solver, self.dfs_time = self.run_dfs()
                        if self.dfs_solver.solution_found:
                            self.compare_solvers()
                
            elif choice == "4":
                self.compare_solvers()
                
            elif choice == "5":
                print("\nGoodbye!")
                break
            
            if input("\nContinue with same board? (y/n): ").lower() != 'y':
                if input("New board? (y/n): ").lower() == 'y':
                    if not self.setup_board():
                        break
                    self.dfs_solver = None
                    self.bfs_solver = None
                else:
                    break