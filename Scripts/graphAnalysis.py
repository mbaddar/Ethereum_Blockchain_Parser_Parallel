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



def load_tagged_addresses():
	addresses={}

	for fn in os.listdir('./tagged_addresses'):
		with open("./tagged_addresses/"+fn) as addr_json:
			addresses.update(json.load(addr_json))
	return addresses

tags=load_tagged_addresses()



measurements=[None,tmp_graph.ep.weight,tmp_graph.ep.dollar]
measurementNames=["number","ether","dollar"]

for measure in [0,1,2]:
	print("Starting with measurement: "+measurementNames[measure])
	pagerank=graph_tool.centrality.pagerank(tmp_graph,weight =measurements[measure])
	tmp_graph.vp.pr=pagerank
	print("calculated pageranks")
	eig,auth,hub=graph_tool.centrality.hits(tmp_graph,weight =measurements[measure])
	tmp_graph.vp.auth=auth
	tmp_graph.vp.hub=hub
	print("calculated HITS")

	mappings=[]
	counter=0
	#creating address association
	for v in tmp_graph.vertices():
		mapping=[int(v),v.in_degree(weight =measurements[measure]),v.out_degree(weight =measurements[measure]),tmp_graph.vp.pr[v],tmp_graph.vp.auth[v],tmp_graph.vp.hub[v]]
		mappings.append(mapping)
		counter+=1
		if counter%100000 == 0:
			print(counter)

	numpiedMappings=np.array(mappings).astype(float)
	print("Created Numpy Array: " + str(time.time()-t))

	#sort by columns
	inSorted=numpiedMappings[numpiedMappings[:,1].argsort()]
	outSorted=numpiedMappings[numpiedMappings[:,2].argsort()]
	prSorted=numpiedMappings[numpiedMappings[:,3].argsort()]
	authSorted=numpiedMappings[numpiedMappings[:,4].argsort()]
	hubSorted=numpiedMappings[numpiedMappings[:,5].argsort()]

	print("Sorted Numpy Arrays: " + str(time.time()-t))

	print(str(inSorted[-1]))
	print(str(outSorted[-1]))
	print(str(prSorted[-1]))
	print(str(authSorted[-1]))
	print(str(hubSorted[-1]))


	allsorted=[inSorted,outSorted,prSorted,authSorted,hubSorted]

	allTaggedRanks=[]
	topTens=[]

	for oneSorted in allsorted:
		rank=10000
		TaggedRanks=[]
		topTen=[]
		for topranked in oneSorted[-10000:]:
			addr=tmp_graph.vp.address[int(topranked[0])]
			if addr in tags:
				taggedRank=[addr,str(tags[addr]),str(rank)]
				TaggedRanks.append(taggedRank)
			if rank<11:
				topTen.append([str(rank),addr])
			rank-=1
		allTaggedRanks.append(TaggedRanks)
		topTens.append(topTen)

	with open('rankings/'+measurementNames[measure]+'taggedRankings.json', 'w') as outfile:
		json.dump(allTaggedRanks, outfile)

	with open('rankings/'+measurementNames[measure]+'topTen.json', 'w') as outfile:
		json.dump(topTens, outfile)