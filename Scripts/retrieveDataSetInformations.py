import sys
import os
import pymongo
import json
import datetime

#important values
block_max = 4369999
quadrillion = 1000000000000000000

#connecting to mongo to get collection
client = pymongo.MongoClient(serverSelectionTimeoutMS=1000)
collection=client["blockchainExtended2"]["blocks"]


def retrieveTransactionValueMinMaxAvg():
    #querry
    txs = collection.aggregate([{"$unwind" : '$transactions' }])

    commulated={}
    maximum={}
    minimum={}

    commulated["value"]=0.0
    commulated["gas"]=0
    commulated["gasPrice"]=0
    commulated["input"]=0

    maximum["value"]=0
    maximum["gas"]=0
    maximum["gasPrice"]=0
    maximum["input"]=0
    minimum["value"]=100000000
    minimum["gas"]=10000000000
    minimum["gasPrice"]=100000000000000
    minimum["input"]=100000000

    #iterate
    for tx in txs:
        commulated["value"]+=tx["transactions"]["value"]
        commulated["gas"]+=int(tx["transactions"]["gas"], 16)
        commulated["gasPrice"]+=int(tx["transactions"]["gasPrice"], 16)
        commulated["input"]+=len(tx["transactions"]["input"])
        maximum["value"]=max(tx["transactions"]["value"],maximum["value"])
        maximum["gas"]=max(int(tx["transactions"]["gas"], 16),maximum["gas"])
        maximum["gasPrice"]=max(int(tx["transactions"]["gasPrice"], 16),maximum["gasPrice"])
        maximum["input"]=max(len(tx["transactions"]["input"]),maximum["input"])
        minimum["value"]=min(tx["transactions"]["value"],minimum["value"])
        minimum["gas"]=min(int(tx["transactions"]["gas"], 16),minimum["gas"])
        minimum["gasPrice"]=min(int(tx["transactions"]["gasPrice"], 16),minimum["gasPrice"])
        minimum["input"]=min(len(tx["transactions"]["input"]),minimum["input"])

    #save to json
    output={}
    output["commulated"]=commulated
    output["maximums"]=maximum
    output["minimums"]=minimum
    with open('timeseries/minMaxAvg.json', 'w') as outfile:
        json.dump(output, outfile)


def calculateBlockDataFieldsIntervalAverages():
    #TWO WEEKS in SECONDS
    fourWeeks = 1209600
    #2 weeks
    interval = fourWeeks
        
    #unixtimestamp
    startTime = 1438269988
    intervalsCommulated={}

    #loop over 2 week intervals
    while startTime < 1508340388:
        print(datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S'))
        blocksInInterval = collection.aggregate([{ "$match" : {"$and":[{ "timestamp" : {"$lt":(startTime+interval) }},{"timestamp" : {"$gte":startTime }}] }}])
        startTime+=interval

        commulatedSize=0
        commulatedDifficulty=int(0)
        commulatedGasUsed=0
        commulatedGasLimit=0
        commulatedDollarPrice=0.0
        commulatedNumberOfTransactions=0
        blocks=0

        #loop over all blocks within the two weeks
        for block in blocksInInterval:
            commulatedSize+=block["size"]
            commulatedDifficulty+=block["difficulty"]
            commulatedGasUsed+=block["gasUsed"]
            commulatedGasLimit+=block["gasLimit"]
            commulatedDollarPrice+=block["dollarPrice"]
            commulatedNumberOfTransactions+=len(block["transactions"])
            blocks+=1

        #calcualte averages
        intervalsCommulated[startTime]={}
        intervalsCommulated[startTime]["size"]=commulatedSize/blocks
        intervalsCommulated[startTime]["difficulty"]=commulatedDifficulty/blocks
        intervalsCommulated[startTime]["gasUsed"]=commulatedGasUsed/blocks
        intervalsCommulated[startTime]["gasLimit"]=commulatedGasLimit/blocks
        intervalsCommulated[startTime]["dollarPrice"]=commulatedDollarPrice/blocks
        intervalsCommulated[startTime]["numberOfTransactions"]=commulatedNumberOfTransactions/blocks


        #save to json
        with open('timeseries/blockValueAverages.json', 'w') as outfile:
            json.dump(intervalsCommulated, outfile)


def calculateTxnDataFieldsIntervalAverages():   
    #TWO WEEKS in SECONDS
    fourWeeks = 1209600
    interval = fourWeeks
        
    #unixtimestamp
    startTime = 1438269988
    intervalsCommulated={}

    while startTime < 1508340388:
        print(datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S'))
        txsInInterval = collection.aggregate([{ "$match" : {"$and":[{ "timestamp" : {"$lt":(startTime+interval) }},{"timestamp" : {"$gte":startTime }}] }},{ "$unwind" : '$transactions'}])
        startTime+=interval


        commulatedInput=0
        commulatedGas=0
        commulatedGasPrice=0
        commulatedValue=0.0
        blocks=0

        for tx in txsInInterval:
            commulatedInput+=len(tx["transactions"]["input"])
            commulatedGas+=int(tx["transactions"]["gas"], 16)
            commulatedGasPrice+=int(tx["transactions"]["gasPrice"], 16)
            commulatedValue+=tx["transactions"]["value"]
            blocks+=1
    
        intervalsCommulated[startTime]={}
        intervalsCommulated[startTime]["input"]=commulatedInput/blocks
        intervalsCommulated[startTime]["gas"]=commulatedGas/blocks
        intervalsCommulated[startTime]["gasPrice"]=commulatedGasPrice/blocks
        intervalsCommulated[startTime]["value"]=commulatedValue/blocks
    
        with open('timeseries/transactionValueAverages.json', 'w') as outfile:
            json.dump(intervalsCommulated, outfile)



retrieveTransactionValueMinMaxAvg()
calculateBlockDataFieldsIntervalAverages()
calculateTxnDataFieldsIntervalAverages()