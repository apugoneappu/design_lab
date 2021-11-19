import streamlit as st
from sys import maxsize
from utils import init
from salesman import Salesman
	
st.title('Design Lab - Apoorve Singhal (17CS30007)')
st.write('')

st.write('# Input graph details')
st.write('For easy usage, default values have been entered for all fields on this page. Scroll down and hit run to simulate !')

input_row = st.columns(2)

with input_row[0]:
	st.write('### Number of locations')
	num_nodes = int(st.number_input('Please enter the number of locations here', min_value=2, value=4, step=1, key='locations'))

with input_row[1]:
	st.write('### Number of services')
	num_services = int(st.number_input('Please enter the number of services here', min_value=2, value=6, step=1, key='services'))

services_list = list(range(num_services))
locations_list = list(range(num_nodes))

st.markdown('----')

location_services = [[] for _ in range(num_nodes)]
location_services_init = [
	[0, 1],
	[0, 2],
	[1, 3],
	[1, 2, 3]
]

init(location_services, location_services_init)
# location_services[:min(len(location_services), len(location_services_init))] = location_services_init[:min(len(location_services), len(location_services_init))]

closing_times = [[] for _ in range(num_nodes)]
closing_times_init = [
	[range(5, 15), range(25, 50)],
	[range(10, 90)],
	[range(25, 45), range(60, 90)],
	[range(15, 35)]
]

init(closing_times, closing_times_init)
# closing_times[:min(len(closing_times), len(closing_times_init))] = closing_times_init[:min(len(closing_times), len(closing_times_init))]

location_service_times = [[maxsize] * num_services for i in range(num_nodes)]
location_service_times_init = [
	[10, 8, maxsize, maxsize],
	[12, maxsize, 20, maxsize],
	[maxsize, 4, maxsize, 30],
	[maxsize, 2, 40, 20],
]
init(location_service_times, location_service_times_init)

for loc in range(num_nodes):

	st.markdown(f'### Inputs for node #{loc}')

	row1 = st.columns(2)
	with row1[0]:
		location_services[loc] = st.multiselect(f'Select services offered (one or more)', services_list, key=f'services{loc}', default=location_services[loc])
	
	with row1[1]:
		closing_time = st.text_input(f'Intervals for which node is closed.', key=f'closing_times{loc}', value=', '.join(f'{x[0]}-{x[-1]+1}' for x in closing_times[loc]))
		if closing_time:
			closing_times[loc] = [range(int(x.split('-')[0]), int(x.split('-')[1])) for x in closing_time.replace(' ', '').split(',')]
		else:
			closing_times[loc] = []

	if not location_services[loc]:
		st.error('No services selected for this location. Please select atleast one service.')
	else:				
		row2 = st.columns(len(location_services[loc]))
		for service_idx, service in enumerate(location_services[loc]):
			with row2[service_idx]:
				# st.write(f'Service #{service}')
				location_service_times[loc][service] = st.number_input(f'Service time for service #{service}', min_value=1, value=location_service_times[loc][service], step=1, key=f'Service time {loc}_{service_idx}')
		
	st.markdown('---')

service_locations = [[]] * num_services
for service in range(num_services):

	# Find all locations in which service i is offered
	service_locations[service] = [loc for loc, services in enumerate(location_services) if service in services]

weights = [[0] * num_nodes for _ in range(num_nodes)]
weights_init = [[0, 11, 5, 10],
			[11, 0, 10, 15],
			[5, 10, 0, 11],
			[10, 15, 11, 0]]

init(weights, weights_init)

st.markdown(f'### Inputs for edge weights')

for i in range(num_nodes):

	i_cols = st.columns(num_nodes)

	for j in range(num_nodes):

		if (i >= j):
			continue

		with i_cols[j]:
			st.write('$W_{{%s}{%s}}$' % (i, j))

			weights[i][j] = int(st.text_input('', value=weights[i][j], key=i*num_nodes+j))
			weights[j][i] = weights[i][j]

st.write('# Input requests')
st.write('For convenience, few requests have been added. Please click Run below to use these. If you wish to simulate your own requests, please clear these, submit new requests and click run.')

if 'requests' not in st.session_state:
	st.session_state['requests'] = [
		[0, 0, [1, 2, 3], False],
		[5, 2, [0, 1, 3], False],
		[15, 3, [0, 1, 2, 3], False],
		[20, 2, [1, 3], False],
	]

request_col = st.columns(3)

with request_col[0]:
	time = st.number_input('Time at which user request comes in', value=0, step=1)

with request_col[1]:
	start = st.selectbox('Starting location', locations_list)

with request_col[2]:
	services_chosen = st.multiselect('Services to avail', services_list)

submit_clear_buttons = st.columns(2)

if submit_clear_buttons[0].button('Submit request'):

		if services_chosen:
			st.session_state['requests'].append([time, start, services_chosen, False])
			st.session_state['requests'] = sorted(st.session_state['requests'], key=lambda x: x[0])
		else:
			st.error('No services selected. Please select atleast one service.')

if submit_clear_buttons[1].button('Clear requests') and st.session_state['requests']:
	st.session_state['requests'] = []
	st.success('Requests cleared.')

st.write('## Requests received')
for idx, request in enumerate(st.session_state['requests']):

	is_done = request[-1]
	status = 'DONE' if is_done else 'PENDING'
	services_text = ', '.join([str(x) for x in request[2]])
	st.write(f"**[{status}]** {idx+1}. T = {request[0]}: Person #{idx+1} starts from location #{request[1]} to avail services: {services_text}")

st.markdown('# Output')
run = st.button('Run')

if run:

	sales = Salesman(num_nodes, num_services, service_locations, location_service_times, closing_times, weights)

	ret = sales.handle_request(st.session_state['requests'])
	while sales.is_left():
		ret, reqs_fulfilled = sales.tick()

		if ret:

			for req, r in zip(reqs_fulfilled, ret):
				for node in r:

					st.write(f'**Person #{req+1}**  \n  Location: {node[1]}  \n  Service: {node[0]}  \n  Arrival info: will reach at {node[3]} after a travel of {node[2]} units  \n  Waiting time: {node[4]}  \n  Service time: {node[5]}  \n  Finish time: {node[6]}')


