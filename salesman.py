# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize
from itertools import permutations, product

# implementation of traveling Salesman Problem
'''
def travellingSalesmanProblem(graph, s, wait):

	assert len(graph) == len(wait), "Invalid graph or wait times"
	assert len(graph[0]) == len(wait), "Invalid graph or wait times"

	# store all vertex apart from source vertex
	vertex = []
	for i in range(V):
		if i != s:
			vertex.append(i)

	# store minimum weight Hamiltonian Cycle
	min_path = maxsize
	next_permutation=permutations(vertex)

	best_perm = None
	for i in next_permutation:

		# store current Path weight(cost)
		current_pathweight = 0

		# compute current path weight
		k = s
		for j in i:
			current_pathweight += graph[k][j] + max(0, wait[j] - (current_pathweight + graph[k][j]))
			k = j
		current_pathweight += graph[k][s]

		# update minimum
		if (current_pathweight < min_path):
			min_path = current_pathweight
			best_perm = i
		
	return min_path, [s, *best_perm, s]
'''


# Driver Code
if __name__ == "__main__":

	services_locations = {
		0: [0, 1, 3],
		1: [1, 2],
		2: [0, 3],
		3: [1, 3]
	}

	location_service_times = {
		0: [0, maxsize, 2, maxsize],
		1: [0, 1, maxsize, 1],
		0: [maxsize, 1, maxsize, maxsize],
		0: [1, maxsize, 1, 1],
	}
	
	book_times = {
		0: [],
		1: [],
		2: [],
		3: []
	}

	closing_times = {
		0: [],
		1: [],
		2: [],
		3: []
	}

	# matrix representation of graph
	graph = [[0, 10, 15, 20],
			[10, 0, 35, 25],
			[15, 35, 0, 30],
			[20, 25, 30, 0]]

	service_time = [0, 20, 5, 5]

	requests = [
		(0, [0, 2, 1]),
		(2, [0, 1, 3]),
		(3, [0, 1, 2, 3]),
		(2, [1, 3])
	]
	V = 4
	# print(travellingSalesmanProblem(graph, s, wait))

	for request in requests:
		
		#starting node
		# s = 2
		s = request[0] 

		#list of service to be availed
		# [0, 1]
		services = request[1] 

		# list of locations for each service (list of lists)
		# {
		# 	0: [0, 1],
		# 	1: [1, 2],
		# }
		# locations = [ [0, 1], [1, 2] ]
		locations = [ services_locations[service] for service in services ]

		# all permutations in which services may be availed
		# = [(0, 1), (1, 0)]
		services_perm = list(permutations(services))

		# all permutations of sets of locations for each request 
		# [
		#	[[0, 1], [1, 2]],
		#	[[1, 2], [0, 1]],
		# ]
		location_choices_perm = list(permutations(locations))

		# all possible locations
		# first = product ([0, 1], [1, 2]) = [(0, 1), (0, 2), (1, 1), (1, 2)]
		# second = product ([1, 2], [0, 1]) = [(1, 0), (1, 1), (2, 0), (2, 1)]
		all_locations = [product(*loc_cho_perm) for loc_cho_perm in location_choices_perm]

		# services_perm and all_locations are in sync of index

		optimal_path = None
		optimal_path_weight = maxsize
				
		for idx in range(len(all_locations)):
			
			service_order = services_perm[idx] # (0, 1)

			for current_path in all_locations[idx]:

				# current_path = (0, 1)

				current_time = 0

				for cur_idx, (ser, loc) in enumerate(zip(service_order, current_path)):
					
					# Time to visit first node from home
					if cur_idx == 0:
						travel_time = graph[s][current_path[0]]
					
					# Time to visit current node from previous node
					else:
						travel_time = graph[current_path[cur_idx - 1]][current_path[cur_idx]]

					#TODO: add waiting time
					current_time += \
						travel_time + \
						service_time[ser] 
				
				# Time to return to home after last node
				current_time += graph[current_path[-1]][s]

					
		
		break



		# store all vertex apart from source vertex
		vertex = []
		for i in range(V):
			if i != s:
				vertex.append(i)

		# store minimum weight Hamiltonian Cycle
		min_path = maxsize
		next_permutation=permutations(vertex)

		best_perm = None
		for i in next_permutation:

			# store current Path weight(cost)
			current_pathweight = 0

			# compute current path weight
			k = s
			for j in i:
				current_pathweight += graph[k][j] + max(0, wait[j] - (current_pathweight + graph[k][j]))
				k = j
			current_pathweight += graph[k][s]

			# update minimum
			if (current_pathweight < min_path):
				min_path = current_pathweight
				best_perm = i
			

