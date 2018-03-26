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



with open('timeseries/blockValueAverages.json') as data_file:
    data = json.load(data_file)



volumes={}

quadrillion = 1000000000000000000

ordered= collections.OrderedDict(sorted(data.items()))
timepoints={}
values=[]
timepoints["size"]=[]
timepoints["difficulty"]=[]
timepoints["gasUsed"]=[]
timepoints["gasLimit"]=[]
timepoints["dollarPrice"]=[]

for timepoint in ordered:
	timepoints["size"].append(data[""+str(timepoint)]["size"])
	timepoints["difficulty"].append(data[""+str(timepoint)]["difficulty"])
	timepoints["gasUsed"].append(data[""+str(timepoint)]["gasUsed"])
	timepoints["gasLimit"].append(data[""+str(timepoint)]["gasLimit"])
	timepoints["dollarPrice"].append(data[""+str(timepoint)]["dollarPrice"])
	values.append(int(float(timepoint)))






figSize= plt.figure()
figDiff= plt.figure()
figUsed= plt.figure()
figLimit= plt.figure()
figPrice= plt.figure()

plotSize = figSize.add_subplot(1,1,1)
plotDiff = figDiff.add_subplot(1,1,1)
plotUsed = figUsed.add_subplot(1,1,1)
plotLimit = figLimit.add_subplot(1,1,1)
plotPrice = figPrice.add_subplot(1,1,1)

convertedValues = mdate.epoch2num(values)


plotSize.plot_date(convertedValues,timepoints["size"])
plotSize.grid(True)
plotSize.spines["top"].set_visible(False)  
plotSize.spines["right"].set_visible(False) 
plotSize.set_ylabel("Average size in Bytes", fontsize=16)  

plotDiff.plot_date(convertedValues,timepoints["difficulty"])
plotDiff.grid(True)
plotDiff.spines["top"].set_visible(False)  
plotDiff.spines["right"].set_visible(False) 
plotDiff.set_ylabel("Average difficulty", fontsize=16)  

plotUsed.plot_date(convertedValues,timepoints["gasUsed"])
plotUsed.grid(True)
plotUsed.spines["top"].set_visible(False)  
plotUsed.spines["right"].set_visible(False) 
plotUsed.set_ylabel("Average gas used", fontsize=16)  

plotLimit.plot_date(convertedValues,timepoints["gasLimit"])
plotLimit.grid(True)
plotLimit.spines["top"].set_visible(False)  
plotLimit.spines["right"].set_visible(False) 
plotLimit.set_ylabel("Average gas limit", fontsize=16)  

plotPrice.plot_date(convertedValues,timepoints["dollarPrice"],'-o')
plotPrice.grid(True)
plotPrice.spines["top"].set_visible(False)  
plotPrice.spines["right"].set_visible(False) 
plotPrice.set_ylabel("Average price in dollar", fontsize=16)  


figSize.suptitle('Two week averages of datafield : size',fontsize=22)
figDiff.suptitle('Two week averages of datafield : difficulty',fontsize=22)
figUsed.suptitle('Two week averages of datafield : gasUsed',fontsize=22)
figLimit.suptitle('Two week averages of datafield : gasLimit',fontsize=22)
figPrice.suptitle('Two week averages of datafield : dollarPrice',fontsize=22)

figSize.autofmt_xdate()
figDiff.autofmt_xdate()
figUsed.autofmt_xdate()
figLimit.autofmt_xdate()
figPrice.autofmt_xdate()


figSize.savefig("timeseries/figures/size.png")
figDiff.savefig("timeseries/figures/difficulty.png")
figUsed.savefig("timeseries/figures/gasUsed.png")
figLimit.savefig("timeseries/figures/gasLimit.png")
figPrice.savefig("timeseries/figures/dollarPrice.png")