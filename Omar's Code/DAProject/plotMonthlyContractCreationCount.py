from pymongo import MongoClient
import json
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdate
import seaborn as sns

def plot(database):
    
    collection = database["MonthlyContractCreationCount"]
    entries = collection.find({})
    xLabels = []
    xValues = []
    yValues = []
    
    for entry in entries:
        xLabels.append(datetime.datetime.fromtimestamp(int(entry['_id'])).strftime('%d-%m-%Y'))
        xValues.append(mdate.epoch2num(int(entry['_id'])))
        yValues.append(float(entry['txnsCount']))
    
    #Graph generation:
    fig = plt.figure()
    plot = fig.add_subplot(111)
    pal = sns.color_palette()
    plot.stackplot(xValues,yValues,labels=xLabels,colors=pal, alpha=0.4 )
    plot.spines["top"].set_visible(False)  
    plot.spines["right"].set_visible(False) 
    plot.grid(True)

    label=plot.set_ylabel("Monthly Contract Creation Count", fontsize=16)  

    plot.xaxis_date()

    fig.autofmt_xdate()


    fig.savefig("Results/MonthlyContractCreationCount.png",bbox_extra_artists=(label,), bbox_inches='tight')
    
    # -*- coding: utf-8 -*-

