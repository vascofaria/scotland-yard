import math
import pickle
import time

def minIndex(l):
  _min = math.inf
  ind = 0
  for i in range(len(l)):
    if l[i] < _min:
      _min = l[i]
      ind = i
  return ind

def isPositionFree(position, positions):
  for p in positions:
    if p == position:
      return False
  return True
  
class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal    = goal
    self.model   = model
    self.auxheur = auxheur

    self.positions   = [0]
    self.agentStatus = []

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    path = []
    self.tickets = tickets

    if (len(init) == 1):
      path.append([[], [init[0]]])
      position = init[0]

      while position != self.goal[0]:
        transp, position = self.expand(position, 0)
        self.tickets[transp] -= 1
        path.append([[transp], [position]])

    else:
      path.append([[], [init[0], init[1], init[2]]])
      self.positions = [init[0], init[1], init[2]]

      # while (self.positions[0] != self.goal[0]) or (self.positions[1] != self.goal[1]) or (self.positions[2] != self.goal[2]):
      #   pass

    return path

  def expand(self, position, agent_number):
    childs = [child[1] for child in self.model[position]]
    heuristics = [self.heuristicFunction(position, child, agent_number) for child in childs]
    return self.model[position][minIndex(heuristics)][0], childs[minIndex(heuristics)]

  def heuristicFunction(self, srcVertex, destVertex, agent_number):
    objVertex = self.goal[agent_number]
    if not isPositionFree(destVertex, self.positions[:agent_number]):
      return math.inf
    if self.tickets[self.getTicketType(srcVertex, destVertex)] > 0:
      return math.sqrt(math.pow(self.getCoordinates(objVertex)[0] - self.getCoordinates(destVertex)[0], 2) + math.pow(self.getCoordinates(objVertex)[1] - self.getCoordinates(destVertex)[1], 2))
    return math.inf

  def getTicketType(self, src, dest):
    for vertex in self.model[src]:
      if (vertex[1] == dest):
        return vertex[0]

  def getCoordinates(self, vertex):
    return self.auxheur[vertex-1]
