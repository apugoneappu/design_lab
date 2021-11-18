# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize
from itertools import permutations, product
import asyncio

def in_range(range1, range2):
	return range1[0] in range2 and range1[-1] in range2

# Driver Code
if __name__ == "__main__":

	services_locations = {
		0: [0],
		1: [1],
		2: [2],
		3: [3]
	}

	location_service_times = {
		0: [0, maxsize, maxsize, maxsize],
		1: [maxsize, 5, maxsize, maxsize],
		2: [maxsize, maxsize, 10, maxsize],
		3: [maxsize, maxsize, maxsize, 5],
	}
	
	book_times = {
		0: [],
		1: [],
		2: [],
		3: []
	}

	closing_times = {
		0: [],
		1: [range(10, 90)],
		2: [],
		3: []
	}

	# matrix representation of graph
	graph = [[0, 11, 5, 10],
			[11, 0, 10, 15],
			[5, 10, 0, 11],
			[10, 15, 11, 0]]

	requests = [
		(0, [1, 2, 3]),
		(2, [0, 1, 3]),
		(3, [0, 1, 2, 3]),
		(2, [1, 3])
	]
	V = 4
	# print(travellingSalesmanProblem(graph, s, wait))

	wait_times = [0, 10, 100, 10]

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

		best_path = None
		best_service_order = None
		best_time = maxsize
				
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

					current_time += travel_time

					wait_time_due_to_closed = sum([max(0, closing_time[-1]+1-current_time) for closing_time in closing_times[loc] if current_time in closing_time])

					current_time += wait_time_due_to_closed

					wait_time_due_to_booked = sum([max(0, book_time[-1]+1-current_time) for book_time in book_times[loc] if current_time in book_time])

					current_time += wait_time_due_to_booked

					current_time +=  location_service_times[loc][ser]

				# Time to return to home after last node
				current_time += graph[current_path[-1]][s]

				if current_time < best_time:
					best_path = current_path
					best_time = current_time
					best_service_order = service_order
					
		
		# Determined the best path
		print('Locations order: ', best_path)
		print('Service order: ', best_service_order)
		print('Best time: ',  best_time)

		# Iterate over the path again
		simulated_time = 0
		for idx, (ser, loc) in enumerate(zip(best_service_order, best_path)):
			
			if idx == 0:
				travel_time = graph[s][best_path[0]]
			else:
				travel_time = graph[best_path[idx - 1]][best_path[idx]]

			simulated_time += travel_time

			wait_time_due_to_closed = sum([max(0, closing_time[-1]+1-simulated_time) for closing_time in closing_times[loc] if simulated_time in closing_time])

			simulated_time += wait_time_due_to_closed

			wait_time_due_to_booked = sum([max(0, book_time[-1]+1-simulated_time) for book_time in book_times[loc] if simulated_time in book_time])

			simulated_time += wait_time_due_to_booked

			simulated_time += location_service_times[loc][ser]

			book_times[loc].append(range(simulated_time - location_service_times[loc][ser], simulated_time))
			book_times[loc] = sorted(book_times[loc], key = lambda x: x[0])
			print(book_times)

			# Debug
			# print(loc, travel_time, wait_time_due_to_closed, wait_time_due_to_booked, location_service_times[loc][ser])
		

		break
