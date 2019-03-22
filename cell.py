class Cell:
   def __init__(self, value=0):
      self.possible = [True]*9
      self.value = value
      self.init = (value != 0)
   
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