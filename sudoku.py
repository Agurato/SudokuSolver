class Cell:
   def __init__(self):
      self.possible = [True]*9
      self.value = 0
      self.init = False
   
   def remove_possible(self, v):
      self.possible[v-1] = False
      if self.value != 0:
         nb_possible = 0
         for number in possible:
            if number is True:
               self.value = number
               nb_possible += 1
         if nb_possible > 1:
            self.value = 0

class SudokuGrid:

   def __init__(self):
      self.cells = [Cell()]*81
   
   def set_values(self, values):
      if len(values) == 81:
         for i in range(0, 81):
            self.cells[i].value = values[i]
            if values[i] != 0:
               self.cells[i].init = True

   def set_value(self, value, index):
      """
      index can be either a tuple (x, y) or an integer
      """
      i = 0
      if type(index) is tuple:
         i = 9*index(1) + index(0)
      elif type(index) is int:
         i = index
      self.cells[i].value = value

   def get_row_indexes(self, index):
      start = (index % 9)*9
      return range(start, start + 9)
   
   def get_col_indexes(self, index):
      return range(index % 9, 81, 9)

   def get_square_indexes(self, index):
      startx = (index % 9)/3 * 3
      starty = (index / 9)/3 * 3
      indexes = []
      for x in range(startx, startx+3):
         for y in range(starty, starty+3):
            indexes.append(9*y + x)
      return indexes

   def check_row(self, index):
      count = 0
      for i in get_row_indexes(index):
         count += self.cells[i].value
      return (count == 45)
   
   def check_col(self, index):
      count = 0
      for i in get_col_indexes(index):
         count += self.cells[i].value
      return (count == 45)
   
   def check_square(self, index):
      count = 0
      for i in get_square_indexes(index):
         count += self.cells[i].value
      return (count == 45)

   def check_cell(self, index):
      return self.check_row(index) and self.check_col(index) and self.check_square(index)

   def resolve_brute(self, index, test_val):
      go_next_cell = False

      # Last cell has been processed
      if index > 80:
         return

      if self.cells[index].init is False:
         self.cells[index].value = test_val
         if self.check_cell(index):
            go_next_cell = True
         else:
            self.resolve_brute(index, test_val + 1)
      else:
         go_next_cell = True
      
      if go_next_cell:
         self.resolve_brute(index + 1, 1)

if __name__ == '__main__':
   grid = SudokuGrid()
   for i in range(27, 54):
      grid.check_square(i)