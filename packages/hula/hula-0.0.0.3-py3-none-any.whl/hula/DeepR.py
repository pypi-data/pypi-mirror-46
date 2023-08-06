from hula.rlutils import *
import numpy as np
import random

class RecurrentLayer:

  def __init__(self, isize, osize, activeFunc=sigmoid):
    self.WS = np.array([[random.uniform(-10, 10) for _ in range(osize)] for _ in range(isize)])
    self.PWS = np.array([[random.uniform(-10, 10) for _ in range(osize)] for _ in range(osize)])
    self.activeFunc = activeFunc
    self.isize = isize
    self.osize = osize
    self.state = np.array([1 for _ in range(osize)])

    self.limboActions = []
    self.stateActions = []

  def activate(self, X):
    X = np.array(X)
    self.state = self.activeFunc(X.dot(self.WS) + self.state.dot(self.PWS))
    return self.state

  def randomAct(self, alpha=0.01):
    action = [
      np.array([[random.uniform(-alpha, alpha) for _ in range(self.osize)] for _ in range(self.isize)]), 
      np.array([[random.uniform(-alpha, alpha) for _ in range(self.osize)] for _ in range(self.osize)])
    ]
    
    currentState = self.WS

    self.WS = self.WS + action[0]
    self.PWS = self.PWS + action[1]

    self.limboActions.append([action, currentState])
  
  def score(self, score):
    for action in self.limboActions:
      self.stateActions.append({
        'action1':action[0][0],
        'action2':action[0][1],
        'state':action[1],
        'score':score
      })

    self.limboActions = []

  def train(self, alpha=0.65):

    currentState = self.WS
    
    ds = [TwDimDistance(x['state'], currentState) for x in self.stateActions]
    mxds = max(ds)
    mxs = max([x['score'] for x in self.stateActions])
    ss = [mxs - x['score'] for x in self.stateActions]
    acs1 = [x['action1'] for x in self.stateActions]
    acs2 = [x['action2'] for x in self.stateActions]

    self.WS = self.WS + np.array(min([[c, a / mxds + b / mxs] for a, b, c in zip(ds, ss, acs1)], key=lambda x: x[1])[0])*alpha
    self.PWS = self.PWS + np.array(min([[c, a / mxds + b / mxs] for a, b, c in zip(ds, ss, acs2)], key=lambda x: x[1])[0])*alpha
  
  def simplify(self, thresh, minscore):
    newStateActions = []
    finalStateActions = []

    self.StateActions = sorted(self.stateActions, key=lambda s: TwDimMagnitude(s['state']))

    last_checkpoint = 0
    for x in self.StateActions:
      if TwDimMagnitude(x['state']) - last_checkpoint > thresh:
        newStateActions.append(x)
        last_checkpoint = TwDimMagnitude(x['state'])

    for act in newStateActions:
      if act['score'] > minscore:
        finalStateActions.append(act)
    
    self.stateActions = finalStateActions
  
class FeedForwardLayer:

  def __init__(self, isize, osize, activeFunc=sigmoid):
    self.WS = np.array([[random.uniform(-10, 10) for _ in range(osize)] for _ in range(isize)])
    self.activeFunc = activeFunc
    self.isize = isize
    self.osize = osize

    self.limboActions = []
    self.stateActions = []

  def activate(self, X):
    X = np.array(X)
    return self.activeFunc(X.dot(self.WS))

  def randomAct(self, alpha=0.01):
    action = np.array([[random.uniform(-alpha, alpha) for _ in range(self.osize)] for _ in range(self.isize)])
    
    currentState = self.WS

    self.WS = self.WS + action

    self.limboActions.append([action, currentState])
  
  def score(self, score):
    for action in self.limboActions:
      self.stateActions.append({
        'action':action[0],
        'state':action[1],
        'score':score
      })

    self.limboActions = []

  def train(self, alpha=0.65):

    currentState = self.WS
    
    ds = [TwDimDistance(x['state'], currentState) for x in self.stateActions]
    mxds = max(ds)
    mxs = max([x['score'] for x in self.stateActions])
    ss = [mxs - x['score'] for x in self.stateActions]
    acs = [x['action'] for x in self.stateActions]

    self.WS = self.WS + np.array(min([[c, a / mxds + b / mxs] for a, b, c in zip(ds, ss, acs)], key=lambda x: x[1])[0])*alpha
  
  def simplify(self, thresh, minscore):
    newStateActions = []
    finalStateActions = []

    self.stateActions = sorted(self.stateActions, key=lambda s: TwDimMagnitude(s['state']))

    last_checkpoint = 0
    for x in self.stateActions:
      if TwDimMagnitude(x['state']) - last_checkpoint > thresh:
        newStateActions.append(x)
        last_checkpoint = TwDimMagnitude(x['state'])

    for act in newStateActions:
      if act['score'] > minscore:
        finalStateActions.append(act)
    
    self.stateActions = finalStateActions

class Net:
  def __init__(self, *layers):
    self.layers = layers

  def activate(self, X):
    latest = X
    for layer in self.layers:
      latest = layer.activate(latest)
    return latest

  def randomAct(self, alpha=0.01):
    for layer in self.layers:
      layer.randomAct(alpha)

  def score(self, score):
    for layer in self.layers:
      layer.score(score)

  def train(self, alpha=0.65):
    for layer in self.layers:
      layer.train(0.65)

  def simplify(self, thresh, minscore):
    for layer in self.layers:
      layer.simplify(thresh, minscore)