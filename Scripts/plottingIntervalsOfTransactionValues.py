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



with open('timeseries/transactionValueAverages.json') as data_file:
    data = json.load(data_file)



volumes={}

quadrillion = 1000000000000000000

ordered= collections.OrderedDict(sorted(data.items()))
timepoints={}
values=[]
timepoints["input"]=[]
timepoints["value"]=[]
timepoints["gas"]=[]
timepoints["gasPrice"]=[]

for timepoint in ordered:
	timepoints["input"].append(data[""+str(timepoint)]["input"])
	timepoints["value"].append(data[""+str(timepoint)]["value"])
	timepoints["gas"].append(data[""+str(timepoint)]["gas"])
	timepoints["gasPrice"].append(data[""+str(timepoint)]["gasPrice"])

	values.append(int(float(timepoint)))



figSize= plt.figure()
figDiff= plt.figure()
figUsed= plt.figure()
figLimit= plt.figure()

plotSize = figSize.add_subplot(1,1,1)
plotDiff = figDiff.add_subplot(1,1,1)
plotUsed = figUsed.add_subplot(1,1,1)
plotLimit = figLimit.add_subplot(1,1,1)

convertedValues = mdate.epoch2num(values)


plotSize.plot_date(convertedValues,timepoints["input"])
plotSize.grid(True)
plotSize.spines["top"].set_visible(False)  
plotSize.spines["right"].set_visible(False) 
plotSize.set_ylabel("Average input length in Bytes", fontsize=16)  

plotDiff.plot_date(convertedValues,timepoints["value"])
plotDiff.grid(True)
plotDiff.spines["top"].set_visible(False)  
plotDiff.spines["right"].set_visible(False) 
plotDiff.set_ylabel("Average value in ether", fontsize=16)  

plotUsed.plot_date(convertedValues,timepoints["gas"])
plotUsed.grid(True)
plotUsed.spines["top"].set_visible(False)  
plotUsed.spines["right"].set_visible(False) 
plotUsed.set_ylabel("Average gas used", fontsize=16)  

plotLimit.plot_date(convertedValues,timepoints["gasPrice"])
plotLimit.grid(True)
plotLimit.spines["top"].set_visible(False)  
plotLimit.spines["right"].set_visible(False) 
plotLimit.set_ylabel("Average gasPrice in wei", fontsize=16)  


figSize.suptitle('Two week averages of datafield : input',fontsize=22)
figDiff.suptitle('Two week averages of datafield : value',fontsize=22)
figUsed.suptitle('Two week averages of datafield : gas',fontsize=22)
figLimit.suptitle('Two week averages of datafield : gasPrice',fontsize=22)

figSize.autofmt_xdate()
figDiff.autofmt_xdate()
figUsed.autofmt_xdate()
figLimit.autofmt_xdate()


figSize.savefig("timeseries/figures/input.png")
figDiff.savefig("timeseries/figures/value.png")
figUsed.savefig("timeseries/figures/gas.png")
figLimit.savefig("timeseries/figures/gasPrice.png")