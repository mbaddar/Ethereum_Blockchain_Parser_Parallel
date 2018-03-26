import sys
sys.path.append("./../Analysis")
import os
os.environ['ETH_BLOCKCHAIN_ANALYSIS_DIR'] = './../Analysis/'
import pymongo
import json
import datetime


#Check if addresses are tagged twice
def check_duplicates():
    addresses={}
    duplicates=0
    for fn in os.listdir('./tagged_addresses'):
        with open("./tagged_addresses/"+fn) as addr_json:
            jsonn=json.load(addr_json)
            for i in jsonn.keys():
                if i in addresses:
                    duplicates+=1
                    print("duplicate Found")
            addresses.update(jsonn)           
    return duplicates

#load all addresses with tags into one dictionary
def load_tagged_addresses():
	addresses={}

	for fn in os.listdir('./tagged_addresses'):
		with open("./tagged_addresses/"+fn) as addr_json:
			addresses.update(json.load(addr_json))
	return addresses



def iterateOverTransactionsForTagging():
    #important values
    block_max = 4369999
    quadrillion = 1000000000000000000

    #TWO WEEKS in SECONDS
    twoWeeks = 1209600
    #2 weeks
    interval = twoWeeks
         
    #unixtimestamp
    startTime = 1438269988

    #connecting to mongo to get collection
    client = pymongo.MongoClient(serverSelectionTimeoutMS=1000)
    collection=client["blockchainExtended2"]["blocks"]

    tags=load_tagged_addresses()

    taggedFromEtherToCertainTime = {}
    taggedToEtherToCertainTime ={}
    while startTime < 1508340388:
        print(datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S'))
        txsInInterval = collection.aggregate([{ "$match" : {"$and":[{ "timestamp" : {"$lt":(startTime+interval) }},{"timestamp" : {"$gte":startTime }}] }},{ "$unwind" : '$transactions'}])
        startTime+=interval
        fromValues={1:[0,0,0],2:[0,0,0],3:[0,0,0],4:[0,0,0],5:[0,0,0],6:[0,0,0],7:[0,0,0],10:[0,0,0]}
        toValues={1:[0,0,0],2:[0,0,0],3:[0,0,0],4:[0,0,0],5:[0,0,0],6:[0,0,0],7:[0,0,0],10:[0,0,0]}

        for i in txsInInterval:
            fro = i["transactions"]["from"]
            to = i["transactions"]["to"]
            ether=i["transactions"]["value"]*quadrillion
            dollar=i["transactions"]["value"]*i["dollarPrice"]
            if fro in tags:
                #adding values to specific wallet types for each measurement
                fromValues[tags[fro]][0]+=ether
                fromValues[tags[fro]][1]+=dollar
                fromValues[tags[fro]][2]+=1
            else:
                #10 indicating untagged
                fromValues[10][0]+=ether
                fromValues[10][1]+=dollar
                fromValues[10][2]+=1
            if to in tags:
                #adding values to specific wallet types for each measurement
                toValues[tags[to]][0]+=ether
                toValues[tags[to]][1]+=dollar
                toValues[tags[to]][2]+=1
            else:
                #10 indicating untagged
                toValues[10][0]+=ether
                toValues[10][1]+=dollar
                toValues[10][2]+=1


            taggedFromEtherToCertainTime[startTime]=fromValues
            taggedToEtherToCertainTime[startTime]=toValues

        with open('tagged_timeseries/from_tags.json', 'w') as outfile:
            json.dump(taggedFromEtherToCertainTime, outfile)
        with open('tagged_timeseries/to_tags.json', 'w') as outfile:
            json.dump(taggedToEtherToCertainTime, outfile)

iterateOverTransactionsForTagging()