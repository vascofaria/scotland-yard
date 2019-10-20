import math
import pickle
import time
import heapq

class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal      = goal
		self.model     = model
		self.auxheur   = auxheur
		self.openSet   = []
		self.inOpenSet = []
		self.paths     = []

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf, math.inf, math.inf]):

		for i in range (len(self.model)):
			self.inOpenSet.append(False)

		heapq.heappush(self.openSet, (math.inf, init[0], []))
		self.inOpenSet[init[0]] = True

		while (len(self.openSet) != 0):

			current = heapq.heappop(self.openSet)
			self.inOpenSet[current[1]] = False
			self.paths.append([current[2], [current[1]]])
			
			if current[1] == self.goal[0]:
				return self.paths

			for neighbor in self.model[current[1]]:
				f = self.heuristicFunction(current[1], self.getPosition(neighbor), 0)
				if not (self.inOpenSet[self.getPosition(neighbor)]):
					heapq.heappush(self.openSet, (f, self.getPosition(neighbor), [self.getTicketType(neighbor)]))	 
					self.inOpenSet[self.getPosition(neighbor)] = True
		
		return self.paths

	def heuristicFunction(self, srcVertex, destVertex, agent_number):
		objVertex = self.goal[agent_number]
		return math.sqrt(math.pow(self.getCoordinates(objVertex)[0] - self.getCoordinates(destVertex)[0], 2) + math.pow(self.getCoordinates(objVertex)[1] - self.getCoordinates(destVertex)[1], 2))

	def getCoordinates(self, vertex):
		return self.auxheur[vertex - 1]

	def getTicketType(self, vertex):
		return vertex[0]

	def getPosition(self, vertex):
		return vertex[1]
