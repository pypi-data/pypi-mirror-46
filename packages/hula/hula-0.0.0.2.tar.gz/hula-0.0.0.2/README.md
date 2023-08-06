# hula-0.0.0.2

## What is hula?

Hula is a set of unconventional machine learning modules. Hula is designed to unify the desired aspects of most machine learning capabilities out there. 

Within hula are a few machine learning algorithms which I've coined as the following:

-  Deep Recursive Learning
-  Reinforcement via Similarity
-  Comprehensive Learning

Respectively, the modules are named:

- RecursiveL
- ReinforcementL
- ComprehensiveNet

I will be working on a blog to explain the workings behind each algorithm.

## Documentation

---

### hula.ComprehensiveNet.CNET(*design*)

Generates an Artificial Neural Network comprised of Memory Activation nodes corresponding to the dimensions of *design*

---

#### hula.ComprehensiveNet.CNET.activate(*X*)

Feeds X through the network and returns the output of the last layer.

---

#### hula.ComprehensiveNet.CNET.act(*alpha*)

Generates a limbo-action proportional to alpha for each memory node in the network.

---

#### hula.ComprehensiveNet.CNET.score(*score*)

Retroactively scores each limbo-action and turns them into state-actions. Higher scores are favored.

---

#### hula.ComprehensiveNet.CNET.train(*alpha*)

Finds the lowest distance to each action's state minus the score of that action.

---

#### hula.ComprehensiveNet.CNET.trim(*perc*)

removes perc percent of state-actions from the state-action tree

----


This list is not complete. There are many more modules, classes, and methods to cover.