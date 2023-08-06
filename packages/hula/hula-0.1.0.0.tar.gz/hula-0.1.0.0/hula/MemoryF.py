from math import e
import numpy as np
from random import uniform

def softmax(*args):
  return np.exp(args)/np.sum(np.exp(args))

def sigmoid(x):
  return 1/(1+np.exp(-x))

def tanh(x):
  return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

def distance(x, y):
  return np.sum([(a-b)**2 for a, b in zip(x, y)])**(0.5)

def magnitude(x):
  return np.sum([a**2 for a in x])**(0.5)

class MemoryActivation:

  def __init__(self, starting_state=uniform(-1, 1), params=[uniform(-1, 1) for _ in range(5)]):

    self.state = starting_state
    self.rw, self.uw, self.sw, self.ow, self.tw = params

    self.stateActions = []
    self.limboActions = []


  def activate(self, x):

    x = x

    replace, use = sigmoid(self.state * self.rw), sigmoid(x * self.uw)

    self.state = (self.state * (1-replace) + x * replace) * self.sw
    
    return (x * (1 - use) + self.state * use) * self.ow

  def multiactivate(self, X):
    o = []
    s = 0
    for x in X:
      o.append(self.activate(x))
      s += self.state
    
    self.state = s / len(X)

    return sigmoid(sum(o))*self.tw

  def setParams(self, params):
    self.rw, self.uw, self.sw, self.ow, self.tw = params


  def getParams(self):
    return [self.rw, self.uw, self.sw, self.ow, self.tw]


  def randomAct(self, alpha=0.01):

    action = [uniform(-alpha, alpha) for _ in range(5)]

    currentstate = self.getParams()

    self.setParams(np.add(self.getParams(), action))

    self.limboActions.append([currentstate, action])


  def score(self, score):

    for action in self.limboActions:
      self.stateActions.append({
        'action':action[1],
        'score':score,
        'state':action[0]
      })

    self.limboActions = []
  

  def train(self, alpha):

    currentState = self.getParams()
    
    ds = [distance(x['state'], currentState) for x in self.stateActions]
    mxs = max([x['score'] for x in self.stateActions])
    ss = [mxs - x['score'] for x in self.stateActions]
    acs = [x['action'] for x in self.stateActions]

    self.setParams(np.add(currentState, np.array(min([[c, a + b] for a, b, c in zip(softmax(*ds), softmax(*ss), acs)], key=lambda x: x[1])[0])*alpha))


  def trim(self, threshold):
    
    newStateActions = []

    for x in self.stateActions:
      if uniform(0, 1) < threshold:
        newStateActions.append(x)

    self.stateActions = newStateActions
