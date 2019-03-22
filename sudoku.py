from cell import Cell
import grid_utils


class Sudoku:

   def __init__(self):
      self.cells = [None]*81
   
   def load_from_file(self, filename):
      with open(filename, "r") as f:
         data = f.read().replace("\n", "").replace("\r", "")
         if len(data) == 81:
            values = []
            for char in data:
               value = 0
               try:
                  value = int(char)
               except ValueError:
                  value = 0
               if value < 1 or value > 9:
                  value = 0
               values.append(value)
            self.set_values(values)
   
   def display(self):
      disp = ""
      for y in range(0, 9):
         if y == 3 or y == 6:
            disp += " ------+-------+------\n"
         for x in range(0, 9):
            if x == 3 or x == 6:
               disp += " |"
            val = self.cells[y*9 + x].value
            if val == 0:
               disp += " ."
            else:
               disp += " " + str(val)
         disp += "\n"
      print(disp)

   def display_full(self):
      disp = "\n"
      for y in range(0, 27):
         if y in [3, 6, 9, 12, 15, 18, 21, 24, 27]:
            disp += "                      |                       |                     \n"
         if y in [9, 18]:
            disp += " ---------------------+-----------------------+---------------------\n"
            disp += "                      |                       |                     \n"
         for x in range(0, 27):
            if x in [3, 6, 9, 12, 15, 18, 21, 24, 27]:
               disp += " "
            if x in [9, 18]:
               disp += " | "
            cell = self.cells[(y/3)*9 + (x/3)]
            poss_index = (y%3)*3 + (x%3)
            if cell.value == 0:
               if cell.possible[poss_index]:
                  disp += " " + str(poss_index+1)
               else:
                  disp += " ."
            else:
               if poss_index == 4:
                  disp += " "+str(cell.value)
               else:
                  disp += "  "
         disp += "\n"
      print(disp)
   
   def set_values(self, values):
      if len(values) == 81:
         for i in range(0, 81):
            if self.cells[i] is None:
               self.cells[i] = Cell(values[i])

   def update(self):
      for i in range(0, 81):
         res = True
         while(res):
            res = False
            for j in   grid_utils.get_row_indexes(i) \
                     + grid_utils.get_col_indexes(i) \
                     + grid_utils.get_square_indexes(i):
               if self.cells[i].remove_possible(self.cells[j].value):
                  res = True

   def check_row(self, index):
      value_exists = [False]*9
      for i in grid_utils.get_row_indexes(index):
         val = self.cells[i].value
         if val != 0:
            if value_exists[val-1]:
               return False
            value_exists[val-1] = True
      return True
   
   def check_col(self, index):
      value_exists = [False]*9
      for i in grid_utils.get_col_indexes(index):
         val = self.cells[i].value
         if val != 0:
            if value_exists[val-1]:
               return False
            value_exists[val-1] = True
      return True
   
   def check_square(self, index):
      value_exists = [False]*9
      for i in grid_utils.get_square_indexes(index):
         val = self.cells[i].value
         if val != 0:
            if value_exists[val-1]:
               return False
            value_exists[val-1] = True
      return True

   def check_cell(self, index):
      return self.check_row(index) and self.check_col(index) and self.check_square(index)

   def resolve_brute(self, index=0, test_val=1):
      # Last cell has been processed
      if index > 80:
         return True
      # Value too high
      if test_val > 9:
         self.cells[index].value = 0
         # Go back
         return False

      # If the cell is not set at initialization
      if self.cells[index].init is False:
         self.cells[index].value = test_val
         # If the value is correct
         if self.check_cell(index):
            # Check next cell
            if self.resolve_brute(index + 1):
               return True
            else:
               return self.resolve_brute(index, test_val + 1)
         # If the value is not correct
         else:
            return self.resolve_brute(index, test_val + 1)

      # If the cell is set at initialization
      else:
         # Check next cell
         return self.resolve_brute(index + 1)
