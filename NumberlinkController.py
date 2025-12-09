from Board import Board
from Game import Game
from DFS_Solver import DFS_Solver
from BFS_Solver import BFS_Solver
from UCS_Solver import UCS_Solver
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
        
        # Set weights for UCS
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

    def compare_solvers(self):
        solvers_run = []
        if self.dfs_solver:
            solvers_run.append(('DFS', self.dfs_solver, self.dfs_time))
        if self.bfs_solver:
            solvers_run.append(('BFS', self.bfs_solver, self.bfs_time))
        if self.ucs_solver:
            solvers_run.append(('UCS', self.ucs_solver, self.ucs_time))
        
        if len(solvers_run) < 2:
            print("Run at least 2 algorithms first")
            return
        
        print("\n" + "="*70)
        print("ALGORITHM COMPARISON")
        print("="*70)
        
        def format_time(t):
            if t < 0.01:
                return f"{t*1000:.2f}ms"
            else:
                return f"{t:.3f}s"
        
        # Header
        header = f"\n{'Metric':<30}"
        for name, _, _ in solvers_run:
            header += f" {name:>12}"
        print(header)
        print("-"*70)
        
        # Solution found
        row = f"{'Solution Found':<30}"
        for _, solver, _ in solvers_run:
            found = solver.solution_found is not None
            row += f" {str(found):>12}"
        print(row)
        
        # States explored
        row = f"{'States Explored':<30}"
        for _, solver, _ in solvers_run:
            row += f" {solver.visited_count:>12,}"
        print(row)
        
        # Time
        row = f"{'Time':<30}"
        for _, _, time_taken in solvers_run:
            row += f" {format_time(time_taken):>12}"
        print(row)
        
        # Path length (for solvers that found solution)
        all_found_solution = all(solver.solution_found for _, solver, _ in solvers_run)
        if all_found_solution:
            row = f"{'Path Length (states)':<30}"
            for _, solver, _ in solvers_run:
                path_len = len(solver.solution_path)
                row += f" {path_len:>12}"
            print(row)
            
            row = f"{'Total Moves':<30}"
            for _, solver, _ in solvers_run:
                moves = sum(len(p) - 1 for p in solver.solution_found.paths.values())
                row += f" {moves:>12}"
            print(row)
            
            # Path cost (for UCS)
            row = f"{'Total Path Cost':<30}"
            for _, solver, _ in solvers_run:
                if hasattr(solver.solution_found, 'get_total_cost'):
                    cost = solver.solution_found.get_total_cost()
                    row += f" {cost:>12.2f}"
                else:
                    row += f" {'N/A':>12}"
            print(row)
        
        # Max depth/queue
        row = f"{'Max Depth/Queue':<30}"
        for _, solver, _ in solvers_run:
            if hasattr(solver, 'max_depth'):
                row += f" {solver.max_depth:>12}"
            elif hasattr(solver, 'max_queue_size'):
                row += f" {solver.max_queue_size:>12,}"
        print(row)
        
        print("="*70)
        
        # Analysis
        if all_found_solution:
            print("\nAnalysis:")
            
            # Find minimum cost solution
            if self.ucs_solver and self.ucs_solver.solution_found:
                ucs_cost = self.ucs_solver.solution_found.get_total_cost()
                print(f"- UCS found minimum cost solution: {ucs_cost:.2f}")
                print("- UCS guarantees optimal cost (lowest total weight)")
            
            # Compare states explored
            min_states = min(solver.visited_count for _, solver, _ in solvers_run)
            for name, solver, _ in solvers_run:
                if solver.visited_count == min_states:
                    print(f"- {name} explored fewest states: {min_states:,}")
                    break

    def start(self):
        print("="*70)
        print("NUMBERLINK SOLVER - DFS vs BFS vs UCS")
        print("="*70)
        
        if not self.setup_board():
            return

        while True:
            print("\n=== MENU ===")
            print("1 - DFS Solver")
            print("2 - BFS Solver")
            print("3 - UCS Solver (Minimum Cost)")
            print("4 - Compare Results")
            print("5 - Exit")

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
                self.compare_solvers()
                
            elif choice == "5":
                print("\nGoodbye!")
                break
            
            if choice in ["1", "2", "3"]:
                if input("\nContinue with same board? (y/n): ").lower() != 'y':
                    if input("New board? (y/n): ").lower() == 'y':
                        if not self.setup_board():
                            break
                        self.dfs_solver = None
                        self.bfs_solver = None
                        self.ucs_solver = None
                    else:
                        break