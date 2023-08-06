import numpy as np
from random import choice, uniform
from hula.rlutils import *

class ANN:
  def __init__(self, design):
    
    self.WS = []

    for dim in lagzip(design):
      self.WS.append(np.random.randn(*dim))

    self.design = design

    self.epoch = 0
    
    self.error = 1

  def _getWeights(self):
    return tuple([tuple([tuple(j) for j in i]) for i in self.WS])

  def _getAction(self):
    return tuple([tuple([tuple(j) for j in i]) for i in self.action])

  def activate(self, X):
    latest = np.array(X)
    for n, W in enumerate(self.WS):
      latest = latest.dot(W)
      if W.all() == self.WS[-1].all():
        latest = latest/5
      elif W.all() == self.WS[0].all():
        latest = latest/5
      else:
        latest = tanh(latest)*2
    return latest

  def __init__TrainDR(self):
    self.limboActions = []
    self.StateActions = {}
    self.action = []
    for dim in lagzip(self.design):
      self.action.append(np.random.randn(*dim)/100)
    self.epoch = 1

  def _actAddition(self):
    for n, a, w in zip(range(len(self.WS)), self.action, self.WS):
      self.WS[n] = w + a

  def _randomAction(self, alpha):
    self.action = []
    for dim in lagzip(self.design):
      self.action.append(np.random.randn(*dim)*alpha)
    
  def GenDR(self, X, Y, alpha):
    if self.epoch == 0:
      self.__init__TrainDR()

    ogerror = float(np.mean((self.activate(X) - Y)**2))

    currentW = self._getWeights()

    self.error = ogerror
    self._randomAction(alpha)
    self._actAddition()

    newerror = float(np.mean((self.activate(X) - Y)**2))

    self.StateActions[currentW] = {
      'action':self._getAction(),
      'score':(newerror - ogerror) / newerror
    }

  def _error(self, a, b):
    return TwDimDistance(a, b)

  def simplify(self, thresh, maxscore):
    newStateActions = {}
    finalStateActions = {}

    self.StateActions = {s:self.StateActions[s] for s in sorted(self.StateActions, key=lambda s: ThrDimMagnitude(s))}

    last_checkpoint = 0
    for x in self.StateActions:
      if ThrDimMagnitude(x) - last_checkpoint > thresh:
        newStateActions[x] = self.StateActions[x]
        last_checkpoint = ThrDimMagnitude(x)

    for state in newStateActions:
      if newStateActions[state]['score'] < maxscore:
        finalStateActions[state] = newStateActions[state]
    
    self.StateActions = finalStateActions

  def nonSpecificGenDR(self, alpha):
    if self.epoch == 0:
      self.__init__TrainDR()

    self._randomAction(alpha)

    self.limboActions.append([self._getWeights(), self._getAction()])

    self._actAddition()

  def nonSpecificScoreDR(self, score):

    for action in self.limboActions:
      self.StateActions[action[0]] = {
        'action':action[1],
        'score':score
      }

    self.limboActions = []

  def TrainDR(self, X, Y, alpha, genaction=True):
    
    if genaction:
      self.GenDR(X, Y, alpha)

    else:
      self.error = float(np.mean((self.activate(X) - Y)**2))
    
    self.epoch += 1

    currentState = self._getWeights()

    choices = []

    if self.epoch > 5:
      mnd = min([ThrDimDistance(currentState, state) for state in self.StateActions])
      mnscore = min([self.StateActions[state]['score'] for state in self.StateActions])

      mxd = max([ThrDimDistance(currentState, state)-mnd for state in self.StateActions])
      mxscore = max([self.StateActions[state]['score']-mnscore for state in self.StateActions])

      for state in self.StateActions:
        d, a = [(ThrDimDistance(currentState, state)-mnd)/mxd, (self.StateActions[state]['score']-mnscore)/mxscore]
        choices.append([state, (d*3 + a*7)/10, self.StateActions[state]['action']])

      for n, W, act in zip(range(len(self.WS)), self.WS, sorted(choices, key=lambda x: x[1])[0][2]):
        self.WS[n] = self.WS[n] + np.array(act) * (1 + alpha)

      self.error = float(np.mean((self.activate(X) - Y)**2))

  def split(self, layern):
    a1 = ANN(self.design[:layern])
    a2 = ANN(self.design[layern:])
    a1.WS = self.WS[:layern]
    a2.WS = self.WS[layern:]

    return (a1, a2)

  def nonSpecificTrainDR(self, alpha):

    self.epoch += 1

    currentState = self._getWeights()

    choices = []

    if self.epoch > 1:
      mxd = max([ThrDimDistance(currentState, state) for state in self.StateActions])
      mxscore = max([self.StateActions[state]['score'] for state in self.StateActions])

      for state in self.StateActions:
        d, a = [(ThrDimDistance(currentState, state))/mxd, (self.StateActions[state]['score'])/mxscore]
        choices.append([state, (d*3 + a*7)/10, self.StateActions[state]['action']])

      for n, W, act in zip(range(len(self.WS)), self.WS, sorted(choices, key=lambda x: x[1])[0][2]):
        self.WS[n] = self.WS[n] + np.array(act) * (1 + alpha)
