# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize
from itertools import permutations, product

from attr import resolve_types
from utils import get_waiting_time, has_intersection

class Salesman:

	def __init__(self, num_locations, num_services, services_locations, location_service_times, closing_times, graph):
			clock = 0

			self.num_locations = num_locations
			self.num_services = num_services
			self.services_locations = services_locations
			self.location_service_times = location_service_times
			self.closing_times = closing_times
			self.graph = graph
			self.book_times = {i: [] for i in range(num_locations)}

			self.requests = []
			self.clock = 0

			# services_locations = {
			# 	0: [0, 1],
			# 	1: [0, 2, 3],
			# 	2: [1, 3],
			# 	3: [2, 3]
			# }

			# location_service_times = {
			# 	0: [10, 8, maxsize, maxsize],
			# 	1: [12, maxsize, 20, maxsize],
			# 	2: [maxsize, 4, maxsize, 30],
			# 	3: [maxsize, 2, 40, 20],
			# }
			

			# requests = [
			# 	[0, [1, 2, 3], False],
			# 	[2, [0, 1, 3], False],
			# 	[3, [0, 1, 2, 3], False],
			# 	[2, [1, 3], False]
			# ]

			# closing_times = {
			# 	0: [range(5, 15), range(25, 50)],
			# 	1: [range(10, 90)],
			# 	2: [range(25, 45), range(60, 90)],
			# 	3: [range(15, 35)]
			# }

			# # matrix representation of graph
			# graph = [[0, 11, 5, 10],
			# 		[11, 0, 10, 15],
			# 		[5, 10, 0, 11],
			# 		[10, 15, 11, 0]]
	
	def handle_request(self, requests):

		for request in requests:
			self.requests.append([*request, False])
		
		result = self.plan()

		return result

	def handle_booked(self):

		for loc in self.book_times.keys():

			new_times = [book_time for book_time in self.book_times[loc] if self.clock <= (book_time[-1]+1)]

			if (len(new_times) != len(self.book_times[loc])):
				print('Old bookings: ', self.book_times[loc])
				print('New bookings: ', new_times)
				self.book_times[loc] = new_times
			
	def plan(self):

		# Handle new requests
		results = []
		for idx, request in enumerate(self.requests):
			
			#starting node
			# s = 2
			s = request[0] 

			#list of service to be availed
			# [0, 1]
			services = request[1] 

			is_done = request[2]

			if is_done:
				continue
				
			# list of locations for each service (list of lists)
			# {
			# 	0: [0, 1],
			# 	1: [1, 2],
			# }
			# locations = [ [0, 1], [1, 2] ]
			locations = [ self.services_locations[service] for service in services ]

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
							travel_time = self.graph[s][current_path[0]]
						
						# Time to visit current node from previous node
						else:
							travel_time = self.graph[current_path[cur_idx - 1]][current_path[cur_idx]]

						current_time += travel_time

						wait_time = get_waiting_time(current_time, self.location_service_times[loc][ser], self.closing_times[loc] + self.book_times[loc])

						current_time += wait_time

						current_time +=  self.location_service_times[loc][ser]

					# Time to return to home after last node
					current_time += self.graph[current_path[-1]][s]

					if current_time < best_time:
						best_path = current_path
						best_time = current_time
						best_service_order = service_order
						
			
			# Determined the best path
			print('Locations order: ', best_path)
			print('Service order: ', best_service_order)
			print('Best time: ',  best_time)

			result = []

			# Iterate over the path again
			simulated_time = 0
			for idx, (ser, loc) in enumerate(zip(best_service_order, best_path)):
				
				if idx == 0:
					travel_time = self.graph[s][best_path[0]]
				else:
					travel_time = self.graph[best_path[idx - 1]][best_path[idx]]

				simulated_time += travel_time

				wait_time = get_waiting_time(simulated_time, self.location_service_times[loc][ser], self.closing_times[loc] + self.book_times[loc])

				simulated_time += wait_time

				simulated_time += self.location_service_times[loc][ser]

				self.book_times[loc].append(range(simulated_time - self.location_service_times[loc][ser], simulated_time))
				self.book_times[loc] = sorted(self.book_times[loc], key = lambda x: x[0])

				result.append((ser, loc, simulated_time - self.location_service_times[loc][ser], wait_time, simulated_time))

				# Debug
				print(loc, travel_time, wait_time, self.location_service_times[loc][ser], simulated_time)
			
			# Update the request
			self.requests[idx][-1] = True
			results.append(result)
			
		return results

	def tick(self):

		print('Clock: ', self.clock)
		
		self.handle_booked()
		self.clock += 1
	
if __name__ == '__main__':


	V = 4
	# print(travellingSalesmanProblem(graph, s, wait))

	services_locations = {
		0: [0, 1],
		1: [0, 2, 3],
		2: [1, 3],
		3: [2, 3]
	}

	location_service_times = {
		0: [10, 8, maxsize, maxsize],
		1: [12, maxsize, 20, maxsize],
		2: [maxsize, 4, maxsize, 30],
		3: [maxsize, 2, 40, 20],
	}
	

	requests = [
		[0, [1, 2, 3], False],
		[2, [0, 1, 3], False],
		[3, [0, 1, 2, 3], False],
		[2, [1, 3], False]
	]

	closing_times = {
		0: [range(5, 15), range(25, 50)],
		1: [range(10, 90)],
		2: [range(25, 45), range(60, 90)],
		3: [range(15, 35)]
	}

	# matrix representation of graph
	graph = [[0, 11, 5, 10],
			[11, 0, 10, 15],
			[5, 10, 0, 11],
			[10, 15, 11, 0]]
	
	sales = Salesman(V, V, services_locations, location_service_times, closing_times, graph)

	ret = sales.handle_request(requests)

	print(ret)

	while sales.clock < 200:
		sales.tick()


