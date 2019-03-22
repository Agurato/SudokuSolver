class Cell:
   def __init__(self, value=0):
      self.value = value
      self.init = (value != 0)
      self.possible = [True]*9
      if self.init:
         for i in range(0, 9):
            self.possible[i] = (i == value-1)
   
   def remove_possible(self, v):
      """
      Returns True if the value has been modified consequently
      """
      if v != 0:
         self.possible[v-1] = False
         if self.value == 0:
            nb_possible = 0
            for number in range(0, 9):
               if self.possible[number] is True:
                  self.value = number+1
                  nb_possible += 1
            if nb_possible > 1:
               self.value = 0
            else:
               return True
      return False