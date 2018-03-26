import matplotlib
matplotlib.use('Agg')
from pylab import *
import time
from graph_tool.all import *
import graph_tool
import numpy
import matplotlib.pyplot as plt
from collections import Counter
import sys
import os
import pymongo
import json
import datetime


t = time.time()
print("Starting at: " + str(time.time()-t))

tmp_graph = load_graph("data/graphs/graph.gt")

print("loaded After: " + str(time.time()-t))

indegrees = []
outdegrees = []
comdegrees = []


for i in tmp_graph.vertices():
	indegrees.append(i.in_degree())
print("In After: " + str(time.time()-t))

for i in tmp_graph.vertices():
	outdegrees.append(i.out_degree())
print("Out After: " + str(time.time()-t))

for i in tmp_graph.vertices():
	comdegrees.append(i.out_degree()+i.in_degree())
print("Commulated After: " + str(time.time()-t))

incounted = Counter(indegrees)
counted = Counter(outdegrees)
comcounted = Counter(comdegrees)

insort = sorted(incounted.items(), reverse=True)
sort = sorted(counted.items(), reverse=True)
comsort = sorted(comcounted.items(), reverse=True)


fig = plt.figure()
inax = fig.add_subplot(2,2,1)
ax = fig.add_subplot(2,2,2)
comax = fig.add_subplot(2,2,3)

inline, = inax.plot(*zip(*insort),"*")
line, = ax.plot(*zip(*sort),"*")
comlin, = comax.plot(*zip(*comsort),"*")

inax.set_xscale('log')
inax.set_yscale('log')
inax.set_xlabel("Number of Ingoing TX")
inax.set_ylabel("Number of address")

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Number of outgoing TX")
ax.set_ylabel("Number of address")

comax.set_xscale('log')
comax.set_yscale('log')
comax.set_xlabel("Number of comulated TX")
comax.set_ylabel("Number of address")


plt.tight_layout()

fig.savefig("powerLaw/powerLaw.png")
print("saves")
