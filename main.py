import Board as b

print("             ++++____",'WELCOME  TO NUMBERLINK Game',"____++++",sep=' ')

numbserOfRowsGrid=int(input("Please enter Your Grid Size here row:"))
numbserOfColumnsGrid=int(input("Please enter Your Grid Size here Column:"))
print("Please enter How Many number of Colors :")
numberOfColores=int(input())

board=b.Board(numbserOfColumnsGrid,numbserOfRowsGrid,numberOfColores)
board.printGrid()
list_of_colors=board.ColorsInputs(numberOfColores)
board.placeForColor(list_of_colors)
 