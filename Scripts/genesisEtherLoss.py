import sys
import os
import pymongo
import json
import datetime


if __name__=="__main__":

    block_max = 4369999
    quadrillion = 1000000000000000000

    client = pymongo.MongoClient(serverSelectionTimeoutMS=1000)
    collection=client["blockchainExtended2"]["blocks"]


    with open('data/genesis_block.json') as data_file:
        data = json.load(data_file)
    genesisAddresses = []
    commulatedGenesisEther=0
    for addr in data:
        genesisAddresses.append("0x" + addr)
        commulatedGenesisEther+=float(data[addr]["wei"])

    fourWeeks = 2419200
    interval = fourWeeks


    startTime = 1438269988 

    genesisEtherToCertainTime={}

    while startTime < 1508340388:
        print(datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S'))
        txsInInterval = collection.aggregate([{ "$match" : {"$and":[{ "timestamp" : {"$lt":(startTime+interval) }},{"timestamp" : {"$gte":startTime }}] }},{ "$unwind" : '$transactions'}])
        startTime+=interval

        for i in txsInInterval:
            if i["transactions"]["from"] in genesisAddresses:
                if float(data[i["transactions"]["from"][2:]]["wei"]) >=0:
                    ether=i["transactions"]["value"]
                    if float(data[i["transactions"]["from"][2:]]["wei"])<=ether*quadrillion:
                        data[i["transactions"]["from"][2:]]["wei"]=0
                        commulatedGenesisEther-=data[i["transactions"]["from"][2:]]["wei"]
                    else:
                        data[i["transactions"]["from"][2:]]["wei"]= float(data[i["transactions"]["from"][2:]]["wei"])-ether*quadrillion
                        commulatedGenesisEther-=ether*quadrillion

            #print(commulatedGenesisEther)

        genesisEtherToCertainTime[startTime]=commulatedGenesisEther

        with open('genesisLoss/losingEther.json', 'w') as outfile:
            json.dump(genesisEtherToCertainTime, outfile)
