import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import json
import seaborn as sns
import collections

measurementNames=["number","ether","dollar"]

algorithms=[[],[],[],[],[]]

for measure in [0,1,2]:
	print("Starting with measurement: "+measurementNames[measure])
	with open('rankings/'+measurementNames[measure]+'taggedRankings.json') as data_file:
	    data = json.load(data_file)
	algorithm=0
	for ranking in data:
		#print(len(ranking))
		counts=[]
		for tag in [1,2,3,4,5,6,7]:
			count=0
			for rank in ranking:
				if int(rank[1]) == tag and int(rank[2])<100:
					count+=1
			counts.append(count)
		algorithms[algorithm].append(counts)

		algorithm+=1


print(algorithms)

labels=['Exchanges','Tokens','Mining Pools','Dapps','Scam','Eth Developer','Genesis','Untagged']
measureNames=["txNumber","ether","dollar"]

algoNames=["in","out","pr","auth","hub"]
for i in range(len(algoNames)):
	print("plotting: "+algoNames[i])
	measured=0
	for measure in algorithms[i]:
		fig = plt.figure()
		plot = fig.add_subplot(1,1,1)
		measure.append((100-sum(measure)))
		pal = sns.color_palette("Set2", 10)
		def my_autopct(pct):
			return ('%.0f' % pct) if pct > 1 else ''
		plot.pie(measure,colors=pal,explode=[0,0,0,0,0,0,0,0.1],autopct=my_autopct,
		shadow=True, startangle=90)
		plot.legend(labels)
		plot.axis('equal')
		fig.savefig('rankings/'+algoNames[i]+measureNames[measured]+"TaggedRankings.png")
		measured+=1