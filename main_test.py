from sudoku import Sudoku

if __name__ == '__main__':
   grid = Sudoku()
   grid.load_from_file("grids/test.txt")
   grid.update()
   grid.display_full()
   if grid.resolve_brute():
      print("SOLVED")
   grid.display_full()