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

def heuristicFunction(vertexCoord, objCoord):
  return math.sqrt(math.pow(vertexCoord[0] - objCoord[0], 2) + math.pow(vertexCoord[1] - objCoord[1], 2))


def positionFree(position, positions):
  for p in positions:
    if p == position:
      return False
  return True
  
class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal    = goal
    self.model   = model
    self.auxheur = auxheur

    self.agentStatus = []

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    path = []
    self.tickets = tickets

    if (len(init) == 1):
      path.append([[], [init[0]]])
      position = init[0]

      if (tickets[0] == math.inf):
        while position != self.goal[0]:
          transp, position = self.expand_2(position, 0)
          path.append([[transp], [position]])

      else:
        while position != self.goal[0]:
          transp, position = self.expand_2(position, 0)
          self.tickets[transp] -= 1
          path.append([[transp], [position]])



    # else:
    #   path.append([[], [init[0], init[1], init[2]]])
    #   positions = [init[0], init[1], init[2]]
    #
    #   while (positions[0] != self.goal[0]) or (positions[1] != self.goal[1]) or (positions[2] != self.goal[2]):
    #     if (positions[0] != self.goal[0]):
    #       transp1, positions[0] = self.expand(positions[0], [], 0)
    #     if (positions[1] != self.goal[1]):
    #       transp2, positions[1] = self.expand(positions[1], [positions[0]], 1)
    #     if (positions[2] != self.goal[2]):
    #       transp3, positions[2] = self.expand(positions[2], [positions[0], positions[1]], 2)
    #
    #     print(f'Agente 1: {positions[0]} from {transp1}')
    #     print(f'Agente 2: {positions[1]} from {transp2}')
    #     print(f'Agente 3: {positions[2]} from {transp3}')
    #
    #     path.append([[transp1, transp2, transp3], [positions[0], positions[1], positions[2]]])

    print(path)

    return path

  def expand_1(self, position, agent_number):
    childs = [child[1] for child in self.model[position]]
    heuristics = [heuristicFunction(self.auxheur[child-1], self.auxheur[self.goal[0]-1]) for child in childs]
    return self.model[position][minIndex(heuristics)][0], childs[minIndex(heuristics)]

  def expand_2(self, position, agent_number):
    childs = [child[1] for child in self.model[position]]
    heuristics = [self.heuristicFunction(position, child, agent_number) for child in childs]
    return self.model[position][minIndex(heuristics)][0], childs[minIndex(heuristics)]

  def expand(self, position, auxP, g):
    childs = [child[1] for child in self.model[position] if positionFree(child[1], auxP)]
    heuristics = [heuristicFunction(self.auxheur[child-1], self.auxheur[self.goal[g]-1]) for child in childs]
    return self.model[position][minIndex(heuristics)][0], childs[minIndex(heuristics)]

  def heuristicFunction(self, srcVertex, destVertex, agent_number):
    objVertex = self.goal[agent_number]
    if self.tickets[self.getTicketType(srcVertex, destVertex)] > 0:
      return math.sqrt(math.pow(self.getCoordinates(objVertex)[0] - self.getCoordinates(destVertex)[0], 2) + math.pow(self.getCoordinates(objVertex)[1] - self.getCoordinates(destVertex)[1], 2))
    return math.inf

  def heuristicFunction2(self, srcVertex, destVertex, agent_number):
    objVertex = self.goal[agent_number]
    d = math.sqrt(math.pow(self.getCoordinates(objVertex)[0] - self.getCoordinates(destVertex)[0], 2) + math.pow(self.getCoordinates(objVertex)[1] - self.getCoordinates(destVertex)[1], 2))
    nt = self.tickets[self.getTicketType(srcVertex, destVertex)]
    print(f'Heuristic value: {d/nt}')
    return d / nt

  def getTicketType(self, src, dest):
    for vertex in self.model[src]:
      if (vertex[1] == dest):
        return vertex[0]

  def getCoordinates(self, vertex):
    return self.auxheur[vertex-1]
