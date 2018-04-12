from pymongo import MongoClient
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdate
import seaborn as sns


def plotMonthlyContractCreationCount(database):
    
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

    label=plot.set_title("Monthly Contract Creation Count", fontsize=16)  

    plot.xaxis_date()

    fig.autofmt_xdate()


    fig.savefig("Results/MonthlyContractCreationCount.png",bbox_extra_artists=(label,), bbox_inches='tight')



def plotMonthlyContractTxnVol(database):
    
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
    
    


def plotMonthlyNonContractTxnVol(database):
    
    collection = database["MonthlyNonContractTxnVol"]
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

    label=plot.set_title("Monthly Non Contract Txn. Vol.", fontsize=16)  

    plot.xaxis_date()

    fig.autofmt_xdate()


    fig.savefig("Results/MonthlyNonContractTransactionVolumes.png",bbox_extra_artists=(label,), bbox_inches='tight')
    


def plotTransactionVolPieChart(database):
    
    collection1 = database["TotalContractTxnsCountAndVol"]
    collection2 = database["TotalNonContractTxnCountAndVol"]
    contractTxns = collection1.find({}).next()
    nonContractTxns = collection2.find({}).next()
    xLabels = ["Contract Txns", "Non-Contract Txns"]
    xValues = [float(contractTxns["totalValue"]), float(nonContractTxns["totalValue"])]
    xCounts = [float(contractTxns["transactionCount"]), float(nonContractTxns["transactionCount"])]
    
    
    #Graph generation:
    fig = plt.figure()
    plot1 = fig.add_subplot(1,2,1)
    plot2 = fig.add_subplot(1,2,2)
    
    plot1.pie(xValues, explode=(0.1, 0), labels=xLabels, colors=["lightskyblue", "yellowgreen"], autopct='%1.1f%%', shadow=True)
    plot2.pie(xCounts, explode=(0.1, 0), labels=xLabels, colors=["lightskyblue", "yellowgreen"], autopct='%1.1f%%', shadow=True)
    plot1.set_title('Volume')
    plot2.set_title('Number of Transactions')
    plot1.axis('equal')
    plot2.axis('equal')
    fig.subplots_adjust(wspace=0.4)
    fig.savefig("Results/VolumeBreakdown.png")