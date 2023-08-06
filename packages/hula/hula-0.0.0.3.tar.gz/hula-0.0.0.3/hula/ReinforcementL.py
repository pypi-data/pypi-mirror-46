from random import randint, uniform

def squish(x, mx, mn):
  return ( x - mn ) / (mx - mn)

def invsquish(x, mx, mn):
  return ( mx - x ) / ( mx - mn )

def distance(x, y):
  return sum(map(lambda a, b: (a - b)**2, x, y))**(1/2)

def normalize(x):
  try:
    return tuple([i / distance((0, 0), x) for i in x])
  except:
    return (0, 0)

class Actor:
  
  def __init__(self):
    raise NotImplementedError("Method hasn't been implemented yet.")

  def act(self):
    raise NotImplementedError("Method hasn't been implemented yet.")

  def getState(self):
    raise NotImplementedError("Method hasn't been implemented yet.")

class Environment:
  
  def __init__(self):
    self.attributions = {}

  def train(self, score, action, state):
    
    if not state in self.attributions:
      
      self.attributions[state] = {"action":action, "score":score}

    elif self.attributions[state]["score"] < score and uniform(0, 1) < (1/3):
      
        self.attributions[state] = {"action":action, "score":score}

  def act(self, current_state):

    self.info = list(map(lambda state: [self.attributions[state]["action"], self.attributions[state]["score"], distance(state, current_state)], self.attributions))

    info = self.info
    
    max_dist = max(info, key=lambda x: x[2])[2]
    min_dist = min(info, key=lambda x: x[2])[2]
    max_score = max(info, key=lambda x: x[1])[1]
    min_score = min(info, key=lambda x: x[1])[1]

    info = list(map(lambda a: [a[0], (invsquish(a[1], max_score, min_score) * 10 + squish(a[2], max_dist, min_dist) * 2) / 12], info))

    return min(info, key=lambda x: x[1])[0]
    
  
