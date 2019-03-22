import math

def get_row_indexes(index, size=9):
      start = (index / size)*size
      return range(start, start + size)
   
def get_col_indexes(index, size=9):
   return range(index % size, size*size, size)

def get_square_indexes(index, size=9):
   square_size = int(math.sqrt(size))
   startx = (index % size)/square_size * square_size
   starty = (index / size)/square_size * square_size
   indexes = []
   for x in range(startx, startx + square_size):
      for y in range(starty, starty + square_size):
         indexes.append(size*y + x)
   return indexes