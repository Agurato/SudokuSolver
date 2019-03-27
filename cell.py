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
      Returns: 2 if the value has been modified consequently
               1 if the possibilities have been modified
               0 if nothing has been modified
      """
      ret = 0
      if v != 0:
         if self.possible[v-1] == True:
            self.possible[v-1] = False
            ret = 1
         if self.value == 0:
            nb_possible = 0
            for number in range(0, 9):
               if self.possible[number] is True:
                  self.value = number+1
                  nb_possible += 1
            if nb_possible > 1:
               self.value = 0
            else:
               self.possible = [False]*9
               self.possible[self.value-1] = True
               ret = 2
      return ret