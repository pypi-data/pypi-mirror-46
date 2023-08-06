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

  def __init__(self, starting_state=0, params=[0, 0, 0, 0, 0, 0]):

    self.state = starting_state
    self.rw, self.uw, self.nw, self.rb, self.ub, self.nb = params

    self.stateActions = []
    self.limboActions = []


  def activate(self, x):

    replace, use = sigmoid(self.rw * x + self.rb), sigmoid(self.uw * x + self.ub)

    self.state = self.state * (1-replace) + x * replace
    
    return tanh(x * (1 - use) + self.state * use + self.nb)

  def multiactivate(self, X):
    o = []
    for x in X:
      o.append(self.activate(x))

    return sigmoid(sum(o))

  def setParams(self, params):
    self.rw, self.uw, self.nw, self.rb, self.ub, self.nb = params


  def getParams(self):
    return [self.rw, self.uw, self.nw, self.rb, self.ub, self.nb]


  def randomAct(self, alpha=0.01):

    action = [uniform(-alpha, alpha) for _ in range(6)]

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
