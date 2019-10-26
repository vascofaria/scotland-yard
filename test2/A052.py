# Grupo 52, Bruno Meira (89421), Vasco Faria (89559)

import math
import pickle
import time
  
class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal    = goal
    self.model   = model

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):

    self.tickets = tickets

    if (len(init) == 1):
      return self.bfs1(init[0], limitexp, limitdepth)

    elif anyorder:
      goalsPermutations = [ [self.goal[0], self.goal[1], self.goal[2]],
                            [self.goal[0], self.goal[2], self.goal[1]],
                            [self.goal[1], self.goal[0], self.goal[2]],
                            [self.goal[1], self.goal[2], self.goal[0]],
                            [self.goal[2], self.goal[0], self.goal[1]],
                            [self.goal[2], self.goal[1], self.goal[0]]]
      min_path = math.inf
      selectedPath = []

      for i in range(6):
        self.goal = goalsPermutations[i]
        path = self.bfs3(init, limitexp, limitdepth)
        if path != None and len(path) < min_path:
          selectedPath = path[:]
          min_path = len(path)

      return selectedPath

    else:
      return self.bfs3(init, limitexp, limitdepth)

  def bfs3(self, init, limitexp, limitdepth):
    numexp = 0
    depth = 0
    levelQueues = []
    nextLevelQueues = [[], [], []]

    status = [False, False, False]
    solutions = [[], [], []]

    path = []

    done = False

    levelQueues.append([(init[0], None, None)])
    levelQueues.append([(init[1], None, None)])
    levelQueues.append([(init[2], None, None)])

    while not done and depth < limitdepth:

      for agentNumber in range(3):
        for el in levelQueues[agentNumber]:
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
          solutions[agentNumber] = []

      while len(levelQueues[0]) != 0 or len(levelQueues[1]) != 0 or len(levelQueues[2]) != 0:
        
        for agentNumber in range(3):

          if len(levelQueues[agentNumber]) != 0:

            current = levelQueues[agentNumber].pop(0)
            numexp += 1

            for vertex in self.model[current[0]]:

              nextLevelQueues[agentNumber].append((vertex[1], current, vertex[0]))

      levelQueues = nextLevelQueues[:]
      nextLevelQueues = [[], [], []]
      depth += 1

    return None

  def validateSolution(self, solutions):

    for i in range(len(solutions[0])):
      for j in range(len(solutions[1])):
        for k in range(len(solutions[2])):
          aproved = True
          auxs = [solutions[0][i], solutions[1][j], solutions[2][j]]
          ticketsAux = self.tickets[:]

          pos = [0, 0, 0]

          while auxs[0][1] != None:
            for agentNumber in range(3):
              pos[agentNumber] = auxs[agentNumber][0]
              ticketsAux[auxs[agentNumber][2]] -= 1
              auxs[agentNumber] = auxs[agentNumber][1]
            if pos[0] == pos[1] or pos[0] == pos[2] or pos[1] == pos[2]:
              aproved = False

            for x in range(3):
              if ticketsAux[x] < 0:
                aproved = False

          if aproved:
            return [solutions[0][i], solutions[1][j], solutions[2][k]]
    return None

  def bfs1(self, srcVertex, limitexp, limitdepth):
    numexp = 0
    depth = 0

    queue = []
    path = []

    queue.append((srcVertex, None, None, self.tickets[:]))

    done = False

    while len(queue) != 0 and not done:
      current = queue.pop(0)
      numexp += 1

      if current[0] == self.goal[0]:
        aux = current
        while aux[1] != None:
          path.insert(0, [[aux[2]], [aux[0]]])
          aux = aux[1]
          done = True
          depth += 1

      for vertex in self.model[current[0]]:
        ticketsAux = current[3][:]
        if ticketsAux[vertex[0]] > 0 and vertex[1] != current[1]:
          ticketsAux[vertex[0]] -= 1
          queue.append((vertex[1], current, vertex[0], ticketsAux))
          self.tickets[vertex[0]] -= 1

    path.insert(0, [[], [srcVertex]])
    return path
