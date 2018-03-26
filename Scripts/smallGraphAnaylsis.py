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

tmp_graph = load_graph("data/graphs/smallerGraph.gt")

print("loaded After: " + str(time.time()-t))


print("motifs2:")
motifs, counts = graph_tool.clustering.motifs(tmp_graph,k=2)
print(motifs,counts)
print("calculated motifs After: " + str(time.time()-t))

counter=0
for i in range(20):

	graph_draw(motifs[i],output='motifs/2/'+str(counts[i])+'Y'+str(counter)+'.png')
	counter+=1

print(sum(counts))


print("motifs3:")
motifs, counts = graph_tool.clustering.motifs(tmp_graph,k=3)
print(motifs,counts)
print("calculated motifs After: " + str(time.time()-t))

counter=0
for i in range(150):

	graph_draw(motifs[i],output='motifs/3/'+str(counts[i])+'X'+str(counter)+'.png')
	counter+=1

print(sum(counts))