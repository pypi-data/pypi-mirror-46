from math import e
import numpy as np

def lagzip(l, lagfactor=1):
  for n, x in enumerate(l[:-lagfactor]):
    yield (l[n], l[n+lagfactor])

def softmax(*args):
  return np.exp(args)/np.sum(np.exp(args))

def sigmoid(x):
  return 1/(1+np.exp(-x))

def tanh(x):
  return (np.exp(x)-np.exp(-x)) / (np.exp(x)+np.exp(-x))

def distance(a, b):
  return sum(map(lambda x, y: (x-y)**2, a, b))**(0.5)

def magnitude(a):
  return sum(map(lambda x: x**2, a))**(1/2)

def TwDimMagnitude(a):
  out = []
  for row in a:
    out.append(magnitude(row))
  return magnitude(out)

def ThrDimMagnitude(a):
  out = []
  for matrix in a:
    out.append(TwDimMagnitude(matrix))
  return magnitude(out)

def TwDimDistance(a, b):
  out = []
  for rowa, rowb in zip(a, b):
    out.append(distance(rowa, rowb))
  return magnitude(out)

def ThrDimDistance(a, b):
  out = []
  for matrixa, matrixb in zip(a, b):
    out.append(TwDimDistance(matrixa, matrixb))
  return magnitude(out)

def normalize(a):
  amag = magnitude(a)
  return list(map(lambda x: x/amag, a))
