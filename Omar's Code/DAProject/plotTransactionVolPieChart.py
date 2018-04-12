from pymongo import MongoClient
import json
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdate
import seaborn as sns

def plot(database):
    
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
    
    # -*- coding: utf-8 -*-

