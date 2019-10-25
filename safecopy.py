import math
import pickle
import time
import heapq, time, sys

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
    self.heapSet = [[], [], []]
    self.agentStatus = [False, False, False]

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    path = []
    self.tickets = tickets

    if (len(init) == 1):
      return self.bfs1(init[0])
      #path.append([[], [init[0]]])
      #position = init[0]

      #while position != self.goal[0]:
      #  transp, position = self.expand(position, 0)
      #  self.tickets[transp] -= 1
      #  path.append([[transp], [position]])

    else:
      return self.bfsVeryNice(init)
      #self.bfs3(init, limitexp)
      return []
      path.append([[], [init[0], init[1], init[2]]])
      self.positions = [init[0], init[1], init[2]]

      # for agentNumber in range(3):
      #   heapq.heappush(self.heapSet[agentNumber], (math.inf, init[agentNumber], None)) # (h, p, t)

      while self.positions[0] != self.goal[0] or self.positions[1] != self.goal[1] or self.positions[2] != self.goal[2]: #not self.agentStatus[0] or not self.agentStatus[1] or not self.agentStatus[2]:
        transp0, self.positions[0] = self.expand(self.positions[0], 0)
        self.tickets[transp0] -= 1
        transp1, self.positions[1] = self.expand(self.positions[1], 1)
        self.tickets[transp1] -= 1
        transp2, self.positions[2] = self.expand(self.positions[2], 2)
        self.tickets[transp2] -= 1

        path.append([[transp0, transp1, transp2], [self.positions[0], self.positions[1], self.positions[2]]])

        #for agentNumber in range(3):
        #  current = heapq.heappop(self.heapSet[agentNumber])
        #  print('Current ' + str(current))
        #  print('Positions ' + str(self.positions))
        #  self.positions[agentNumber] = current[1]
        #  path[len(path)-1][0].append(current[2])
        #  path[len(path)-1][1].append(current[1])
        #  self.expand_heap(current[1], agentNumber)
        #  print(path)
        # print(f'Agent: {agentNumber} --> {self.heapSet[agentNumber]}')

      print(path)

    return path

  def expand(self, position, agentNumber):
    childs = [child[1] for child in self.model[position]]
    heuristics = [self.heuristicFunction(position, child, agentNumber) for child in childs]
    return self.model[position][minIndex(heuristics)][0], childs[minIndex(heuristics)]

  def expand_heap(self, position, agentNumber):
    for route in self.model[position]:
      if (self.heuristicFunction(position, route[1], agentNumber)) != math.inf:
        heapq.heappush(self.heapSet[agentNumber], (self.heuristicFunction(position, route[1], agentNumber), route[1], route[0]))

  def expand_child(self, position):
    for route in self.model[position]:
      self.checkRoute(route, agentNumber)

  def checkRoute(self, route, agentNumber):
    if route[1] == self.goal[agentNumber]:
      self.agentStatus[agentNumber] = True

  def bfsVeryNice(self, init):
    levelQueues = []
    nextLevelQueues = [[], [], []]
    currents = [None, None, None]
    status = [False, False, False]
    solutions = [[], [], []]
    path = []

    done = False

    levelQueues.append([(init[0], None, None)])
    levelQueues.append([(init[1], None, None)])
    levelQueues.append([(init[2], None, None)])

    while not done:

      for agentNumber in range(3):
        for el in levelQueues[agentNumber]: #pode haver mais de um element solution
          if self.goal[agentNumber] == el[0]:
            solutions[agentNumber].append(el)
            status[agentNumber] = True

      if status[0] and status[1] and status[2]:
        aprovedSolutions = self.validateSolution(solutions)
      else:
        aprovedSolutions = None

      if aprovedSolutions != None:

        auxs = [aprovedSolutions[0], aprovedSolutions[1], aprovedSolutions[2]]
        while auxs[0][1] != None:
          path.insert(0, [[], []])

          for agentNumber in range(3):
            path[0][0].append(auxs[agentNumber][2])
            path[0][1].append(auxs[agentNumber][0])
            auxs[agentNumber] = auxs[agentNumber][1]

        path.insert(0, [[], [init[0], init[1], init[2]]])
        done = True
        return path

      else:
        for agentNumber in range(3):
          status[agentNumber] = False

      while len(levelQueues[0]) != 0 or len(levelQueues[1]) != 0 or len(levelQueues[2]) != 0:
        
        for agentNumber in range(3):

          if len(levelQueues[agentNumber]) != 0:

            current = levelQueues[agentNumber].pop(0)

            for vertex in self.model[current[0]]:

              nextLevelQueues[agentNumber].append((vertex[1], current, vertex[0]))

      levelQueues = nextLevelQueues[:]
      nextLevelQueues = [[], [], []]

  def validateSolution(self, solutions):

    for i in range(len(solutions[0])):
      for j in range(len(solutions[1])):
        for k in range(len(solutions[2])):
          aproved = True
          auxs = [solutions[0][i], solutions[1][j], solutions[2][j]]

          pos = [0, 0, 0]

          while auxs[0][1] != None:
            for agentNumber in range(3):
              pos[agentNumber] = auxs[agentNumber][0]
              auxs[agentNumber] = auxs[agentNumber][1]
            if pos[0] == pos[1] or pos[0] == pos[2] or pos[1] == pos[2]:
              aproved = False

          #check tickets

          if aproved:
            return [solutions[0][i], solutions[1][j], solutions[2][k]]
    return None

    #auxs = [solutions[0], solutions[1], solutions[2]]

    #pos = [0, 0, 0]
    #while auxs[0][1] != None:
    #  for agentNumber in range(3):
    #    pos[agentNumber] = auxs[agentNumber][0]
    #    auxs[agentNumber] = auxs[agentNumber][1]
    #  if pos[0] == pos[1] or pos[0] == pos[2] or pos[1] == pos[2]:
    #    print(solutions)
    #    print('hey')
    #    return False
    #check tickets
    #return True

  def bfs3(self, init, limitexp):
    queue = []
    currents = [None, None, None]
    path = []

    done = False

    queue.append([(init[0], None, None)])
    queue.append([(init[1], None, None)])
    queue.append([(init[2], None, None)])

    while not done and limitexp > 0:
      if currents[0] != None and currents[1] != None and currents[2] != None:
        if currents[0][0] == self.goal[0] and currents[1][0] == self.goal[1] and currents[2][0] == self.goal[2]:
          print(currents)
          # checkar tickets and same position
          auxs = [currents[0], currents[1], currents[2]]
          while auxs[0][1] != None:
            path.insert(0, [[], []])
            print(path)
            print(path[0])
            print(path[0][0])
            for agentNumber in range(3):
              path[0][0].append(auxs[agentNumber][2])
              path[0][1].append(auxs[agentNumber][0])
              auxs[agentNumber] = auxs[agentNumber][1]

          #for agentNumber in range(3):
          #  aux = currents[agentNumber]
          #  while aux[1] != None:
          #    path.insert(0, [[aux[2]], [aux[0]]])
          #    print(aux[0])
          #    aux = aux[1]
          print(path)
          done = True
        
        #print(currents[0][0], currents[1][0], currents[2][0])

      for agentNumber in range(3):
        currents[agentNumber] = queue[agentNumber].pop(0)

        for vertex in self.model[currents[agentNumber][0]]:
          queue[agentNumber].append((vertex[1], currents[agentNumber], vertex[0]))

      limitexp -= 1

  def bfs1(self, srcVertex):
    queue = []
    path = []

    queue.append((srcVertex, None, None, self.tickets[:]))

    done = False

    while len(queue) != 0 and not done:
      current = queue.pop(0)

      if current[0] == self.goal[0]:
        aux = current
        while aux[1] != None:
          path.insert(0, [[aux[2]], [aux[0]]])
          print(aux[0])
          aux = aux[1]
          done = True

      for vertex in self.model[current[0]]:
        ticketsAux = current[3][:]
        if ticketsAux[vertex[0]] > 0 and vertex[1] != current[1]:
          ticketsAux[vertex[0]] -= 1
          queue.append((vertex[1], current, vertex[0], ticketsAux))
          self.tickets[vertex[0]] -= 1

    path.insert(0, [[], [srcVertex]])
    return path


  def heuristicFunction(self, srcVertex, destVertex, agent_number):
    objVertex = self.goal[agent_number]
    if not isPositionFree(destVertex, self.positions):
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
