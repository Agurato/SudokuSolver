import copy
import os
import sys
import time

from cell import Cell
import grid_utils


class Sudoku:

   def __init__(self):
      self.cells = [None]*81
   
   def load_from_file(self, filename, number=1):
      with open(filename, "r") as f:
         data = f.readlines()
         if number > len(data):
            raise ValueError(f"There is only {len(data)} grids (n°{number} requested)")
         line = data[number-1][:-1]
         if len(line) == 81:
            values = []
            for char in line:
               value = 0
               try:
                  value = int(char)
               except ValueError:
                  value = 0
               if value < 1 or value > 9:
                  value = 0
               values.append(value)
            self.set_values(values)
         else:
            raise ValueError(f"len(line) = {len(line)}")
   
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
      sys.stdout.flush()

   def display_full(self):
      #os.system('cls' if os.name == 'nt' else 'clear')
      print(" ===================================================================")
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
            cell = self.cells[int(y/3)*9 + int(x/3)]
            poss_index = int(y%3)*3 + int(x%3)
            if cell.possible[poss_index]:
               disp += " " + str(poss_index+1)
            else:
               disp += " ."
         disp += "\n"
      print(disp)
      sys.stdout.flush()

   def display_mix(self):
      #os.system('cls' if os.name == 'nt' else 'clear')
      print(" ===================================================================")
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
            cell = self.cells[int(y/3)*9 + int(x/3)]
            poss_index = int(y%3)*3 + int(x%3)
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
      sys.stdout.flush()
   
   def set_values(self, values):
      if len(values) == 81:
         for i in range(0, 81):
            if self.cells[i] is None:
               self.cells[i] = Cell(values[i])
   
   def reset_possibilities(self):
      for i in range(0, 81):
         if self.cells[i].value == 0:
            self.cells[i].possible = [True]*9
         else:
            self.cells[i].possible = [False]*9
            self.cells[i].possible[self.cells[i].value - 1] = True

   def update_old(self):
      res = True
      while(res):
         res = False
         for i in range(0, 81):
            unique_indexes = set().union(grid_utils.get_row_indexes(i), grid_utils.get_col_indexes(i), grid_utils.get_square_indexes(i))
            unique_indexes.remove(i)
            for j in list(unique_indexes):
               changes = self.cells[j].remove_possible(self.cells[i].value)
               if changes > 1:
                  res = True

   def update(self, indexes=list(range(0, 81))):
      new_list = []
      for i in indexes:
         related = set().union(grid_utils.get_row_indexes(i), grid_utils.get_col_indexes(i), grid_utils.get_square_indexes(i))
         related.remove(i)
         for j in list(related):
            changes = self.cells[j].remove_possible(self.cells[i].value)
            if changes > 1:
               new_list.append(j)
      if len(new_list) > 0:
         self.update(new_list)

   def check_indexes(self, indexes):
      value_exists = [False]*9
      for i in indexes:
         val = self.cells[i].value
         if val != 0:
            if value_exists[val-1]:
               return False
            value_exists[val-1] = True
      return True

   def check_row(self, index):
      return self.check_indexes(grid_utils.get_row_indexes(index))
   
   def check_col(self, index):
      return self.check_indexes(grid_utils.get_col_indexes(index))
   
   def check_square(self, index):
      return self.check_indexes(grid_utils.get_square_indexes(index))

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
   
   def resolve_smart(self, index=0, test_val=1):
      #self.display_full()
      #self.display()
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
         # If test_val is not possible
         if self.cells[index].possible[test_val-1] is False:
            return self.resolve_smart(index, test_val + 1)

         self.cells[index].value = test_val
         # If the value is correct
         if self.check_cell(index):
            self.update()
            self.display_full()
            self.display()
            backup_cells = copy.deepcopy(self.cells)
            # Check next cell
            if self.resolve_smart(index + 1):
               return True
            else:
               self.cells = copy.deepcopy(backup_cells)
               return self.resolve_smart(index, test_val + 1)
         # If the value is not correct
         else:
            return self.resolve_smart(index, test_val + 1)

      # If the cell is set at initialization
      else:
         # Check next cell
         return self.resolve_smart(index + 1)

