import math
import pickle
import time
import heapq
import sys

class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal      = goal
		self.model     = model
		self.auxheur   = auxheur
		self.openSet   = [[], [], []]
		self.inOpenSet = [[], [], []]
		self.paths     = [[], [], []]

	def done(self):
		if len(self.goal) == 1:
			return len(self.openSet[0]) == 0 or (len(self.paths[0]) > 0 and self.paths[0][len(self.paths[0]) - 1][1] == self.goal[0])
		else:
			return ((len(self.openSet[0]) == 0 and 
				     len(self.openSet[1]) == 0 and 
				     len(self.openSet[2]) == 0) or 
					((len(self.paths[0]) > 0 and self.paths[0][len(self.paths[0]) - 1][1] == self.goal[0]) and
					 (len(self.paths[1]) > 0 and self.paths[1][len(self.paths[1]) - 1][1] == self.goal[1]) and
					 (len(self.paths[2]) > 0 and self.paths[2][len(self.paths[2]) - 1][1] == self.goal[2])))


	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf, math.inf, math.inf]):

		for i in range (len(self.model)):
			self.inOpenSet[0].append(False)
			self.inOpenSet[1].append(False)
			self.inOpenSet[2].append(False)

		for i in range (len(self.goal)):
			heapq.heappush(self.openSet[i], (math.inf, init[i], []))
			self.inOpenSet[i][init[i]] = True

		i = 0

		while (not self.done()):
			print(i)
			current = heapq.heappop(self.openSet[i])
			self.inOpenSet[i][current[1]] = False
			self.paths[i].append([current[2], current[1]])
			print(self.paths[i])
			if current[1] == self.goal[i]:
				i += 1
				if i == len(self.goal):
					i = 0
				print(self.paths)
				sys.exit(0)
				continue
			for neighbor in self.model[current[1]]:
				f = self.heuristicFunction(current[1], self.getPosition(neighbor), i)
				if not (self.inOpenSet[i][self.getPosition(neighbor)]):
					heapq.heappush(self.openSet[i], (f, self.getPosition(neighbor), [self.getTicketType(neighbor)]))	 
					self.inOpenSet[i][self.getPosition(neighbor)] = True
		
			i += 1
			if i == len(self.goal):
				i = 0

		print(self.paths)

		return []

	def heuristicFunction(self, srcVertex, destVertex, agent_number):
		objVertex = self.goal[agent_number]
		return math.sqrt(math.pow(self.getCoordinates(objVertex)[0] - self.getCoordinates(destVertex)[0], 2) + math.pow(self.getCoordinates(objVertex)[1] - self.getCoordinates(destVertex)[1], 2))

	def getCoordinates(self, vertex):
		return self.auxheur[vertex - 1]

	def getTicketType(self, vertex):
		return vertex[0]

	def getPosition(self, vertex):
		return vertex[1]
