import numpy as np

class Board:
    
    def __init__(self, num_cols, num_rows, num_colors):
        self.cols = num_cols
        self.rows = num_rows
        self.num_colors = num_colors
        self.grid = np.zeros(self.rows * self.cols, dtype=np.uint8)
        self.weights = np.ones(self.rows * self.cols, dtype=int)   
        self.positions = {}
    
    def _index(self, row, col):
        return row * self.cols + col
    
    def set_weights_manually(self):
        print("Default weight for all cells is 1.0")
        choice = input("enter new weights (or default all ones)? (y/n): ").lower()
        
        if choice == 'y':
            print("\nEnter weights for each cell (row by row)")
            for i in range(self.rows):
                for j in range(self.cols):
                    while True:
                        try:
                            weight = float(input(f"Weight for cell ({i},{j}): "))
                            if weight >= 0:
                                self.weights[self._index(i, j)] = weight
                                break
                            else:
                                print("Weight must be positive")
                        except ValueError:
                            print("Invalid input")
            
            print("\nWeights set successfully!")
            self.print_weights()
    
    def print_weights(self):
        """Display the weight grid"""
        print("\n=== WEIGHT GRID ===")
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                weight = self.weights[self._index(i, j)]
                row += f"{weight:5.1f} "
            print(row)
        print()
    
    def get_weight(self, row, col):
        """Get weight of a specific cell"""
        return self.weights[self._index(row, col)]
    
    def printGrid(self):
        horiz = '+' + '----+' * self.cols
        print("\n")
        for i in range(self.rows):
            print(horiz)
            row = '|'
            for j in range(self.cols):
                cell_val = self.grid[self._index(i, j)]
                display = ' ' if cell_val == 0 else str(cell_val)
                row += f'  {display} |'
            print(row)
        print(horiz)
    
    def ColorsInputs(self, numberOfColors):
        colors = []
        if numberOfColors > max(self.rows, self.cols):
            for i in range(1, 4):
                if numberOfColors <= max(self.rows, self.cols):
                    print("Number accepted.")
                    break
                print(f"Attempt {i} of 3. Enter ≤ {max(self.rows, self.cols)}:")
                numberOfColors = int(input())
                if i == 3 and numberOfColors > max(self.rows, self.cols):
                    print("Try again later.")
                    return []

        for i in range(numberOfColors):
            while True:
                color = int(input(f"Enter color number {i+1}: "))
                if color in colors:
                    print("Color already used!")
                    continue
                colors.append(color)
                break
        return colors
    
    def placeForColor(self, list_of_colors):
        positions = {}
        for color in list_of_colors:
            start_r, start_c = None, None
            while start_r is None or start_c is None:
                row = self._validateRange(int(input(f"Start row for {color}: ")), self.rows, "row")
                col = self._validateRange(int(input(f"Start column for {color}: ")), self.cols, "column")
                if row is not None and col is not None:
                    if not self._isOccupied(row, col, positions):
                        start_r, start_c = row, col
                    else:
                        print("Cell occupied.")

            end_r, end_c = None, None
            while end_r is None or end_c is None:
                row = self._validateRange(int(input(f"End row for {color}: ")), self.rows, "row")
                col = self._validateRange(int(input(f"End column for {color}: ")), self.cols, "column")
                if row is not None and col is not None:
                    if [row, col] == [start_r, start_c]:
                        print("Cannot be same as start.")
                        continue
                    if not self._isOccupied(row, col, positions):
                        end_r, end_c = row, col
                    else:
                        print("Cell occupied.")

            positions[color] = {"start": [start_r, start_c], "end": [end_r, end_c]}

        self._addNumbersToGrid(positions)
        self.positions = positions
        return positions
    
    def _addNumbersToGrid(self, positions):
        for color, coord in positions.items():
            s = coord["start"]
            e = coord["end"]
            self.grid[self._index(s[0], s[1])] = color
            self.grid[self._index(e[0], e[1])] = color
    
    def isValidPosition(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def _isOccupied(self, row, col, positions):
        for coord in positions.values():
            if coord["start"] == [row, col] or coord["end"] == [row, col]:
                return True
        return False
    
    def _validateRange(self, value, limit, name):
        if 0 <= value < limit:
            return value
        print(f"Invalid {name}, must be 0-{limit-1}")
        return None
    
    def getCell(self, row, col):
        return self.grid[self._index(row, col)]
    
    def setCell(self, row, col, value):
        self.grid[self._index(row, col)] = value
        return True
    
    def resetGrid(self):
        self.grid.fill(0)
        for color, coord in self.positions.items():
            s = coord["start"]
            e = coord["end"]
            self.grid[self._index(s[0], s[1])] = color
            self.grid[self._index(e[0], e[1])] = color
    
    def chooseStartEnd(self, color):
        while True:
            choice = input(f"Start or End for color {color}? (s/e): ").lower()
            if choice == "s":
                return self.positions[color]["start"].copy()
            elif choice == "e":
                return self.positions[color]["end"].copy()
            else:
                print("Invalid choice, enter 's' or 'e'.")