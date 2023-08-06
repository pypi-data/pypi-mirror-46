from hula.MemoryF import *
from hula.RecursiveL import *
from hula.rlutils import *

class CNET:
  
  def __init__(self, design):
    self.mems = []
    
    for n in design[1:]:
      self.mems.append([MemoryActivation(0, [0, 0, 0, 0, 0, 0]) for _ in range(n)])

  def activate(self, X):
    
    latest = X

    for layer in self.mems:
      temp = []
      for mem in layer:
        temp.append(mem.multiactivate(latest))

      latest = temp

    return latest

  def act(self, alpha):
    for layer in self.mems:
      for mem in layer:
        mem.randomAct(alpha)

  def score(self, score):
    for layer in self.mems:
      for mem in layer:
        mem.score(score)

  def train(self, alpha):
    for layer in self.mems:
      for mem in layer:
        mem.train(alpha)

  def trim(self, perc):
    for layer in self.mems:
      for mem in layer:
        mem.trim(perc)
      


