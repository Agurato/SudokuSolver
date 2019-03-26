import sys

from sudoku import Sudoku

if __name__ == '__main__':
   grid = Sudoku()
   filename = "grids/easy.txt"
   number = 1
   if len(sys.argv) > 1:
      filename = sys.argv[1]
   if len(sys.argv) > 2:
      number = int(sys.argv[2])

   grid.load_from_file(filename, number)
   grid.display()
   if grid.resolve_brute():
      print("SOLVED\n")
   grid.display()