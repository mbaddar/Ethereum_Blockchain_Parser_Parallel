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
legend=['Tagged','Untagged']

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
				#the [2] is just the number of tx. [1] --> dollar, [0]--> ether
				volume+=data[timepoint][tag][measure]
			volumes[timepoint]=volume


		
		
		#parse unixtimestamps to x values
		x=[]
		for i in ordered.keys():
			x.append(int(i))

		#parse tagged volumes to y values
		y=[]
		tagValues=[]
		tagValues2=[]

		total=0
		antitotal=0
		for timepoint in ordered:
			total+=data[timepoint]["10"][measure]

			amount=data[timepoint]["10"][measure]/max(1,volumes[timepoint])*100
			antiAmount=100-amount
			antitotal+=volumes[timepoint]-data[timepoint]["10"][measure]
			tagValues.append(amount)
			tagValues2.append(antiAmount)
		print(total/(antitotal+total))
		y.append(tagValues2)
		y.append(tagValues)
		x=[]
		for i in ordered.keys():
			x.append(int(float(i)))


		#Graph generation:
		fig = plt.figure()
		plot = fig.add_subplot(1,1,1)
		convertedValues = mdate.epoch2num(x)
		#dollar = fig.add_subplot(2,2,2)
		#number = fig.add_subplot(2,2,3)
		pal = sns.color_palette("Set2", 10)
		plot.stackplot(convertedValues,y,labels=legend,colors=pal, alpha=0.4 )
		plot.spines["top"].set_visible(False)  
		plot.spines["right"].set_visible(False) 
		plot.legend(loc='upper right')
		lgd = plot.legend(legend,bbox_to_anchor=(0.7, 0.8),fontsize=12)

		plot.set_ylabel("stake of "+measureNames[measure]+"-volume in percent", fontsize=16)  

		plot.xaxis_date()

		fig.autofmt_xdate()


		fig.savefig("tagged_timeseries/OnlyUntagged/"+filenames[filenamecounter]+".png",bbox_extra_artists=(lgd,), bbox_inches='tight')
		filenamecounter+=1