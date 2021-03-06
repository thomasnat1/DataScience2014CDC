# 2/13/14
# Charles O. Goddard

import pylab
import numpy
from matplotlib import cm
from matplotlib import pyplot
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap as Basemap

import apidata

m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
			projection='lcc',lat_1=33,lat_2=45,lon_0=-95, resolution=None)
# m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
shp_info = m.readshapefile('st99_d00', 'states', drawbounds=True)

state_populations = {'California': 38332521, 'Texas': 26448193,
'New York': 19651127, 'Florida': 19552860, 'Illinois': 12882135,
'Pennsylvania': 12773801, 'Ohio': 11570808, 'Georgia': 9992167,
'Michigan': 9895622, 'North Carolina': 9848060, 'New Jersey': 8899339,
'Virginia': 8260405, 'Washington': 6971406, 'Massachusetts': 6692824,
'Arizona': 6626624, 'Indiana': 6570902, 'Tennessee': 6495978,
'Missouri': 6044171, 'Maryland': 5928814, 'Wisconsin': 5742713,
'Minnesota': 5420380, 'Colorado': 5268367, 'Alabama': 4833722,
'South Carolina': 4774839, 'Louisiana': 4625470, 'Kentucky': 4395295,
'Oregon': 3930065, 'Oklahoma': 3850568, 'Puerto Rico': 3615086,
'Connecticut': 3596080, 'Iowa': 3090416, 'Mississippi': 2991207,
'Arkansas': 2959373, 'Utah': 2900872, 'Kansas': 2893957,
'Nevada': 2790136, 'New Mexico': 2085287, 'Nebraska': 1868516,
'West Virginia': 1854304, 'Idaho': 1612136, 'Hawaii': 1404054,
'Maine': 1328302, 'New Hampshire': 1323459, 'Rhode Island': 1051511,
'Montana': 1015165, 'Delaware': 925749, 'South Dakota': 844877,
'Alaska': 735132, 'North Dakota': 723393, 'District of Columbia': 646449,
'Vermont': 626630, 'Wyoming': 582658}

with open('../data/CY2013Registrants.csv', 'r') as fd:
	registrant_list = list(apidata.read_csv(fd, 'Registrant'))
registrants = dict((r.registration_token, r) for r in registrant_list)

print('%d registrants known' % (len(registrants),))

unknown = set()
unknown_state = set()
u_pulls = 0
total_pulls = 0

state_pulls = dict((sd['NAME'].lower(), 0) for sd in m.states_info)

with open('../data/CY2013CodePulls.csv', 'r') as fd:
	pulls = apidata.read_csv(fd, 'CodePull')
	for pull in pulls:
		token = pull.registration_token
		if not token in registrants:
			unknown.add(token)
		else:
			state = registrants[token].state.lower()
			if not state in state_pulls:
				unknown_state.add(state)
				u_pulls += 1
			else:
				state_pulls[state] += 1
		total_pulls += 1

minp, maxp = min(state_pulls.values()), max(state_pulls.values())

print('%d total pulls' % (total_pulls, ))
print('%d unknown registrants' % (len(unknown),))
print('%d unknown state names (%d pulls)' % (len(unknown_state), u_pulls))
print('(min, max) = (%d, %d)' % (minp, maxp))

cmap = pyplot.get_cmap('Greys_r')
ax = pyplot.gca()
for i, sd in enumerate(m.states_info):
	state = sd['NAME'].lower()
	pulls = state_pulls[state]
	color = rgb2hex(cmap((pulls - minp) / (1.0 * maxp - minp))[:3])
	poly = Polygon(m.states[i], facecolor=color)
	ax.add_patch(poly)

m.drawparallels(numpy.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(numpy.arange(-120,-40,20),labels=[0,0,0,1])

cax = cm.ScalarMappable(cmap=cmap)
cax.set_array(state_pulls.values())
pyplot.colorbar(cax)
pyplot.title('Code Pulls per State for CY2013')
pyplot.show()
