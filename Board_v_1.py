# import numpy as np

# class Board:
    
#     def __init__(self, num_cols, num_rows, num_colors):
#         self.cols = num_cols
#         self.rows = num_rows
#         self.num_colors = num_colors
#         self.grid = np.zeros(self.rows *self.cols, dtype=np.uint8)
#         self.positions = {}  

    
#     def printGrid(self):
#         horiz = '+' + '----+' * self.cols
#         print("\n")
#         for i in range(self.rows):
#             print(horiz)
#             row = '|'
#             for j in range(self.cols):
#                 cell_val = self.grid[i, j]
#                 # Display empty cells as spaces
#                 display = ' ' if cell_val == 0 else str(cell_val)
#                 row += f'  {display} |'
#             print(row)
#         print(horiz)

  
#     def ColorsInputs(self, numberOfColors):
#         colors = []
#         if numberOfColors > max(self.rows, self.cols):
#             for i in range(1, 4):
#                 if numberOfColors <= max(self.rows, self.cols):
#                     print("Number accepted.")
#                     break
#                 print(f"Attempt {i} of 3. Enter ≤ {max(self.rows, self.cols)}:")
#                 numberOfColors = int(input())
#                 if i == 3 and numberOfColors > max(self.rows, self.cols):
#                     print("Try again later.")
#                     return []

#         for i in range(numberOfColors):
#             while True:
#                 color = int(input(f"Enter color number {i+1}: "))
#                 if color == 0:
#                     print("Color cannot be 0.")
#                     continue
#                 if color in colors:
#                     print("Color already used!")
#                     continue
#                 colors.append(color)
#                 break
#         return colors

   
#     def placeForColor(self, list_of_colors):
#         positions = {}
#         for color in list_of_colors:
#             start_r, start_c = None, None
#             while start_r is None or start_c is None:
#                 row = self.__validateRange(int(input(f"Start row for {color}: ")), self.rows, "row")
#                 col = self.__validateRange(int(input(f"Start column for {color}: ")), self.cols, "column")
#                 if row is not None and col is not None:
#                     if not self.__isOccupied(row, col, positions):
#                         start_r, start_c = row, col
#                     else:
#                         print("Cell occupied.")

#             end_r, end_c = None, None
#             while end_r is None or end_c is None:
#                 row = self.__validateRange(int(input(f"End row for {color}: ")), self.rows, "row")
#                 col = self.__validateRange(int(input(f"End column for {color}: ")), self.cols, "column")
#                 if row is not None and col is not None:
#                     if [row, col] == [start_r, start_c]:
#                         print("Cannot be same as start.")
#                         continue
#                     if not self.__isOccupied(row, col, positions):
#                         end_r, end_c = row, col
#                     else:
#                         print("Cell occupied.")

#             positions[color] = {"start": [start_r, start_c], "end": [end_r, end_c]}

#         self.__AddNumbersTOGrid(positions)
#         self.positions = positions
#         return positions
 
#     def __AddNumbersTOGrid(self, positions):
#         for color, coord in positions.items():
#             s = coord["start"]
#             e = coord["end"]
#             # Removed unnecessary validation - constructor ensures valid positions
#             self.grid[s[0], s[1]] = color
#             self.grid[e[0], e[1]] = color

    
#     # OPTIMIZED: Inline simple check (no function call overhead)
#     def isValidPosition(self, row, col):
#         return 0 <= row < self.rows and 0 <= col < self.cols

#     def __isOccupied(self, row, col, positions):
#         for coord in positions.values():
#             if coord["start"] == [row, col] or coord["end"] == [row, col]:
#                 return True
#         return False

#     def __validateRange(self, value, limit, name):
#         if 0 <= value < limit:
#             return value
#         print(f"Invalid {name}, must be 0-{limit-1}")
#         return None

 
#     # OPTIMIZED: Direct array access (removed unnecessary validation)
#     def getCell(self, row, col):
#         return self.grid[row, col]

#     # OPTIMIZED: Direct array access
#     def setCell(self, row, col, value):
#         self.grid[row, col] = value
#         return True

    
#     def resetGrid(self):
#         # OPTIMIZED: Use fill instead of recreating array
#         self.grid.fill(0)
#         for color, coord in self.positions.items():
#             s = coord["start"]
#             e = coord["end"]
#             self.grid[s[0], s[1]] = color
#             self.grid[e[0], e[1]] = color
#         print("Grid has been reset successfully.")

 
#     def chooseStartEnd(self, color):
#         while True:
#             choice = input(f"Start or End for color {color}? (s/e): ").lower()
#             if choice == "s":
#                 return self.positions[color]["start"].copy()
#             elif choice == "e":
#                 return self.positions[color]["end"].copy()
#             else:
#                 print("Invalid choice, enter 's' or 'e'.")