# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 14:07:06 2018

@author: Omar Waqar
"""
from pymongo import MongoClient
import json
from bson.json_util import dumps

import os.path


def transactionsOfContracts(db):
    
    try:
        blockCollection = db["blocks"]
        
        
        
        pipeline = [
            {
                u"$unwind": u"$transactions"
            }, 
            {
                u"$lookup": {
                    u"from": u"ContractAddresses",
                    u"localField": u"transactions.to",
                    u"foreignField": u"Address",
                    u"as": u"transactions_docs"
                }
            }
        ]
        
        cursor = blockCollection.aggregate(
            pipeline, 
            allowDiskUse = True
        )
        print("Aggragation pipeline made.")
        entries=[]
        i=1
        for doc in cursor:
            entry={}
            print("Entries {} appended".format(i))
            i+=1
            entry["Address"] = doc["transactions"]["to"]
            entry["Timestamp"] = doc["transactions"]["timestamp"]
            entry["Value"] = doc["transactions"]["value"]
            entries.append(entry)
                 
        print("Writing entries to file")
        with open('Analysis/ToContractTransaction.json', 'w') as outfile:
            json.dump(entries, outfile)
            
    except Exception as e:
        print ("Error Message: ", str(e))

def extractTransactionInformation():
    
    #connecting to mongo to get collection
    client = MongoClient(serverSelectionTimeoutMS=1000)
    collection=client["blockchainExtended2"]["Transactions"]
    
    with open('Analysis/contractAddresses.json', 'r') as infile:
        contractAddresses = json.load(infile)
        
    lastIndexRead = 0
    
    if os.path.exists('Analysis/CheckPoint.txt'):
        with open('Analysis/CheckPoint.txt', 'r') as outfile:
            lastIndexRead = int(outfile.read())
    
    addressCount = len(contractAddresses)
    n = (addressCount // 20) + 1
    addressChunkIndices = []
    for i in range(lastIndexRead, len(contractAddresses), n):
       addressChunkIndices.append(contractAddresses[i:i + n]) 
       lastIndexRead = i + n
    print("Starting")
    txsInInterval = collection.find({}).batch_size(100000)
    lastIndexProcessed = 0
    for chunk in addressChunkIndices:        
        transactFromContract = []
        transactionToContract =[]
        transactionNoncontract = []

        for t in txsInInterval:
            tData = {}
            tData["from"] = t["transactions"]["from"]
            tData["to"] = t["transactions"]["to"]
            tData["ether"] = t["transactions"]["value"]*1000000000000000000
            tData["timeStamp"] = t["transactions"]["timestamp"]

            if  tData["from"] in chunk:
                transactFromContract.append(tData)
            elif tData["to"] in chunk:
                transactionToContract.append(tData)
            else:
                transactionNoncontract.append(tData)
        
        if(len(transactFromContract) > 0):
            with open('Analysis/TransactionToContract{}.json'.format(lastIndexProcessed), 'a') as outfile:
                json.dump(transactFromContract, outfile)
        
        if(len(transactionToContract) > 0):
            with open('Analysis/TransactionFromContract{}.json'.format(lastIndexProcessed), 'a') as outfile:
                json.dump(transactionToContract, outfile)
        
        if(len(transactionNoncontract) > 0):
            with open('Analysis/TransactionsNoncontract{}.json'.format(lastIndexProcessed), 'a') as outfile:
                json.dump(transactionNoncontract, outfile)
            
        lastIndexProcessed = lastIndexRead
        print("{} indices processed".format(lastIndexProcessed))
        with open('Analysis/CheckPoint.txt', 'w') as outfile:
            outfile.write(str(lastIndexProcessed))

    
    
    
def convertJsonFileToCollection(fullFileName, dataBase, collectionName):
    with open(fullFileName, 'r') as infile:
        contractAddresses = json.load(infile)
    
    if(collectionName not in dataBase.collection_names()):
        dataBase.create_collection(collectionName)
        
    coll = dataBase[collectionName]
    for entry in contractAddresses:
        coll.insert_one({ "Address": entry})

def noOfContractsInTimeInterval(dbBlocks):
     try:
         results = {}
         contractAddresses = set([])
         day = 86400
         
         interval = day
         #unixtimestamp
         startTime = 1438269988
         blocks = dbBlocks.find({})
         for block in blocks:
             if "result" in block:
                 block = block["result"]
       
             for t in block["transactions"]:
                 if t["isContractCreation"]:
                     contractAddresses.add(t["to"])
                     timeInterval = (((t["timestamp"] - startTime) // interval) * interval) + startTime
                     results[timeInterval] = results.get(timeInterval,0) + 1
        
         with open('Analysis/contractCreationCount_daily.json', 'a') as outfile:
             json.dump(results, outfile)
             
         with open('Analysis/contractAddresses.json', 'a') as outfile:
             json.dump(list(contractAddresses), outfile)

     except Exception as e:
        print ("Error decoding block:" , block["number"])
        print ("Error Message: ", str(e))
        