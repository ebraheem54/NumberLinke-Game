import numpy   as n
class Board():
    
    def __init__(self,numberOfColums,numberOfRows,numberOfColores):
        self.colunms=numberOfColums
        self.rows=numberOfRows
        self.numberOfColores=numberOfColores
        self.gird=n.zeros((self.rows,self.colunms),dtype=int)

    
    def printGrid(self):
         horizantal='+'+'----+'*self.colunms
         print("\n")
         for i in range(self.rows): 
            print(horizantal)
            row='|'
            for j in range(self.colunms):
                row+=f'  {self.gird[i,j]} |'    
            print(row)

         print(horizantal)

    def ColorsInputs(self,numberOfColors):
     list_of_colors=[]
     if(numberOfColors>max(self.rows,self.colunms)):
        for i in range(1,4):
           if(numberOfColors<=min(self.rows,self.colunms)):
              print("Ok this number accepted lets enter the colors's number")
              break
           print(f" attempts {i} of 3 ,Please enter number less than grid size {max(self.rows,self.colunms)}")
           numberOfColors=int(input())
           if(i==3 and numberOfColors>max(self.rows, self.colunms)):
                  print("please try again")
    
     for i in range(numberOfColors):
          print(f"enter your color number:{i+1} ")
          color= int(input())
          list_of_colors.append(color)

     return list_of_colors  


    def placeForColor(self,list_of_colors):
            positions = {}
 
            for i in range(len(list_of_colors)):
                start_row_x=input(f"enter start Coordinates  row of the number {list_of_colors[i]}:\n")
                start_column_y=input(f"enter start Coordinates column  of the number {list_of_colors[i]}:\n")
                Coordinates_start=[start_row_x,start_column_y]  

                end_row_x=input(f"enter  end Coordinates row of the number {list_of_colors[i]}:\n")
                end_row_y=input(f"enter end column  of the number {list_of_colors[i]}:\n")

                Coordinates_end=[end_row_x,end_row_y]
                dic_coordinates={"start":Coordinates_start,"end":Coordinates_end}  
               
                positions[list_of_colors[i]]=dic_coordinates
 
            print(positions)      


    """
   #private function  
   force the input row stay in less than grid's row
    """
    def __validationForRow(self,x):
        
