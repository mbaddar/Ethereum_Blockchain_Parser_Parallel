import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import json
import collections
import seaborn as sns
import datetime
import matplotlib.dates as mdate


tags=['1','2','3','4','5','6','7','10']
legend=['Exchanges','Tokens','Mining Pools','Dapps','Scam','Eth Developer','Genesis','Untagged']

quadrillion = 1000000000000000000
datasets=[]

with open('tagged_timeseries/from_tags.json') as data_file:
    datasets.append(json.load(data_file))

with open('tagged_timeseries/to_tags.json') as data_file:
    datasets.append(json.load(data_file))

filenames=["fromEther","fromDollar","fromNumber","toEther","toDollar","toNumber"]
filenamecounter=0
for data in datasets:
	for measure in [0,1,2]:
		measureNames=["ether","dollar","txNumber"]
		#calculate commulated volume for a timepoint
		volumes={}
		timepoints={}
		ordered= collections.OrderedDict(sorted(data.items()))
		for timepoint in ordered:
			volume=0
			for tag in tags:
				volume+=data[timepoint][tag][measure]
			volumes[timepoint]=volume


		
		
		#parse unixtimestamps to x values
		x=[]
		for i in ordered.keys():
			x.append(int(i))

		y=[]
		tagValues=[]
		for timepoint in ordered:
			value=0
			for tag in tags:
				value+=data[timepoint][tag][measure]
			tagValues.append(value)
		y.append(tagValues)


		x=[]
		for i in ordered.keys():
			x.append(int(float(i)))




		#Graph generation:
		fig = plt.figure()
		plot = fig.add_subplot(1,1,1)
		convertedValues = mdate.epoch2num(x)
		pal = sns.color_palette()
		plot.stackplot(convertedValues,y,labels=tags,colors=pal, alpha=0.4 )
		plot.spines["top"].set_visible(False)  
		plot.spines["right"].set_visible(False) 

		plot.grid(True)

		label=plot.set_ylabel("total "+measureNames[measure]+"-volume", fontsize=16)  

		plot.xaxis_date()

		fig.autofmt_xdate()


		fig.savefig("tagged_timeseries/totalVolumes/"+filenames[filenamecounter]+".png",bbox_extra_artists=(label,), bbox_inches='tight')
		filenamecounter+=1