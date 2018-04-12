from pymongo import MongoClient
import json
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdate
import seaborn as sns

def plot(database):
    
    collection = database["MonthlyContractTxnVol"]
    entries = collection.find({})
    xLabels = []
    xValues = []
    yValues = []
    
    for entry in entries:
        xLabels.append(datetime.datetime.fromtimestamp(int(entry['_id'])).strftime('%d-%m-%Y'))
        xValues.append(mdate.epoch2num(int(entry['_id'])))
        yValues.append(float(entry['txnVol']))
    
    #Graph generation:
    fig = plt.figure()
    plot = fig.add_subplot(111)
    pal = sns.color_palette()
    plot.stackplot(xValues,yValues,labels=xLabels,colors=pal, alpha=0.4 )
    plot.spines["top"].set_visible(False)  
    plot.spines["right"].set_visible(False) 
    plot.grid(True)

    label=plot.set_title("Monthly Contract Txn. Vol.", fontsize=16)  

    plot.xaxis_date()

    fig.autofmt_xdate()


    fig.savefig("Results/MonthlyContractTransactionVolumes.png",bbox_extra_artists=(label,), bbox_inches='tight')
    
    