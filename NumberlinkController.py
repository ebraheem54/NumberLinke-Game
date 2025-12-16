from Board import Board
from Game import Game
from DFS_Solver import DFS_Solver
from BFS_Solver import BFS_Solver
from UCS_Solver import UCS_Solver
from HillClimbing_Solver import HillClimbing_Solver
from AStar_Solver import AStar_Solver
import time

class NumberlinkController:
   
    def __init__(self):
        self.board = None
        self.dfs_solver = None
        self.dfs_time = None
        self.bfs_solver = None
        self.bfs_time = None
        self.ucs_solver = None
        self.ucs_time = None
        self.hill_solver = None
        self.hill_time = None
        self.astar_solver = None
        self.astar_time = None

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
        
        # Set weights for UCS and A*
        self.board.set_weights_manually()
        
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
    
    def run_ucs(self, max_nodes=None):
        game = Game(self.board)
        start = time.time()
        solver = UCS_Solver(game, max_nodes=max_nodes)
        solution = solver.solve()
        elapsed = time.time() - start

        if solution:
            solver.print_solution_path()
            solver.print_solution()
        
        return solver, elapsed
    
    def run_hill_climbing(self, max_nodes=None):
        game = Game(self.board)
        start = time.time()
        solver = HillClimbing_Solver(game, max_nodes=max_nodes)
        solution = solver.solve()
        elapsed = time.time() - start

        # Always print result (even if stuck at local max)
        solver.print_solution()
        
        return solver, elapsed
    
    def run_astar(self, max_nodes=None):
        game = Game(self.board)
        start = time.time()
        solver = AStar_Solver(game, max_nodes=max_nodes)
        solution = solver.solve()
        elapsed = time.time() - start

        if solution:
            solver.print_solution_path()
            solver.print_solution()
        
        return solver, elapsed

    def compare_bfs_astar(self):
        """Compare BFS and A* algorithms (as requested in the task)"""
        if not self.bfs_solver or not self.astar_solver:
            print("\nPlease run both BFS and A* first!")
            return
        
        print("\n" + "="*70)
        print("BFS vs A* COMPARISON")
        print("="*70)
        
        print(f"\n{'Metric':<30} {'BFS':>15} {'A*':>15}")
        print("-"*70)
        
        # States explored
        print(f"{'States Explored':<30} {self.bfs_solver.visited_count:>15,} {self.astar_solver.visited_count:>15,}")
        
        # Time
        def format_time(t):
            if t < 0.01:
                return f"{t*1000:.2f}ms"
            else:
                return f"{t:.3f}s"
        
        print(f"{'Time':<30} {format_time(self.bfs_time):>15} {format_time(self.astar_time):>15}")
        
        # Solution found
        bfs_found = self.bfs_solver.solution_found is not None
        astar_found = self.astar_solver.solution_found is not None
        print(f"{'Solution Found':<30} {str(bfs_found):>15} {str(astar_found):>15}")
        
        if bfs_found and astar_found:
            bfs_moves = sum(len(p) - 1 for p in self.bfs_solver.solution_found.paths.values())
            astar_moves = sum(len(p) - 1 for p in self.astar_solver.solution_found.paths.values())
            print(f"{'Total Moves':<30} {bfs_moves:>15} {astar_moves:>15}")
        
        print("="*70)
        
        # Analysis
        print("\nAnalysis:")
        if astar_found and bfs_found:
            diff = self.bfs_solver.visited_count - self.astar_solver.visited_count
            percent = (diff / self.bfs_solver.visited_count) * 100 if self.bfs_solver.visited_count > 0 else 0
            if diff > 0:
                print(f"- A* explored {diff:,} fewer states than BFS ({percent:.1f}% reduction)")
                print("- A* is more efficient due to its heuristic guidance")
            elif diff < 0:
                print(f"- BFS explored {abs(diff):,} fewer states than A*")
            else:
                print("- Both algorithms explored the same number of states")

    def start(self):
        print("="*70)
        print("NUMBERLINK SOLVER - ALL SEARCH ALGORITHMS")
        print("="*70)
        
        if not self.setup_board():
            return

        while True:
            print("\n=== MENU ===")
            print("1 - DFS Solver")
            print("2 - BFS Solver")
            print("3 - UCS Solver (Minimum Cost)")
            print("4 - Hill Climbing Solver")
            print("5 - A* Solver")
            print("6 - Compare BFS vs A*")
            print("7 - Exit")

            choice = input("\nChoice: ").strip()

            if choice == "1":
                print("\nRunning DFS Solver...")
                self.dfs_solver, self.dfs_time = self.run_dfs()
                
            elif choice == "2":
                print("\nRunning BFS Solver...")
                self.bfs_solver, self.bfs_time = self.run_bfs()
            
            elif choice == "3":
                print("\nRunning UCS Solver...")
                self.ucs_solver, self.ucs_time = self.run_ucs()
            
            elif choice == "4":
                print("\nRunning Hill Climbing Solver...")
                self.hill_solver, self.hill_time = self.run_hill_climbing()
                
            elif choice == "5":
                print("\nRunning A* Solver...")
                self.astar_solver, self.astar_time = self.run_astar()
            
            elif choice == "6":
                self.compare_bfs_astar()
                
            elif choice == "7":
                print("\nGoodbye!")
                break
            
            if choice in ["1", "2", "3", "4", "5"]:
                if input("\nContinue with same board? (y/n): ").lower() != 'y':
                    if input("New board? (y/n): ").lower() == 'y':
                        if not self.setup_board():
                            break
                        # Reset all solvers
                        self.dfs_solver = None
                        self.bfs_solver = None
                        self.ucs_solver = None
                        self.hill_solver = None
                        self.astar_solver = None
                    else:
                        break