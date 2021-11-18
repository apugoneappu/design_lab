def has_intersection(x, y):

	if type(x) is not range:
		x = range(x[0], x[1])
	
	if type(y) is not range:
		y = range(y[0], y[1])

	ts = y[0]
	te = y[-1]+1

	cs = x[0]
	ce = x[-1]+1

	if (ts <= cs and cs < te):
		return True
	
	if (ts < ce and ce <= te):
		return True

	if (cs <= ts and ts < ce):
		return True
	
	if (cs < te and te <= ce):
		return True
	
	return False

def get_waiting_time(job_start, job_duration, unavailable_times):

	unavailable_times = sorted(unavailable_times, key = lambda x: x[1])
	unavailable_times = sorted(unavailable_times, key = lambda x: x[0])

	waiting_time = 0
	job_range = range(job_start, job_start+job_duration)

	last_idx = None
	for idx, unavailable_time in enumerate(unavailable_times):

		if (idx >= 1):
			s = max(unavailable_times[idx-1][-1]+1, job_start)
			job_range = range(s, s+job_duration)

		if (has_intersection(job_range, unavailable_time)):
			last_idx = idx

	if last_idx is None:
			return waiting_time

	waiting_time = unavailable_times[last_idx][-1]+1 - job_start

	return waiting_time

if __name__ == '__main__':

	ret = has_intersection([8, 9], [10, 15])
	print(ret)

	ret = has_intersection([8, 10], [10, 15])
	print(ret)

	ret = has_intersection([8, 12], [10, 15])
	print(ret)

	ret = has_intersection([12, 13], [10, 15])
	print(ret)

	ret = has_intersection([15, 16], [10, 15])
	print(ret)

	ret = has_intersection([17, 18], [10, 15])
	print(ret)

	ret = has_intersection([15, 19], [17, 22])
	print(ret)

	ret = get_waiting_time(9, 4, [range(10, 15), range(17, 22), range(26, 35)])
	print(ret)
