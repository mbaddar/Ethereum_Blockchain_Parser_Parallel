from pymongo import MongoClient
import DataExtractionUtilities as utils
import json
           
            
if __name__=="__main__":
    client = MongoClient()
    database = client["blockchainExtended2"]
    collection = database["blocks"]

    
    
    try:
        #utils.noOfContractsInTimeInterval(collection)
        #utils.transactionVolContractVSRest(collection)
        #utils.transactionsOfContracts()      
        utils.extractTransactionInformation()

    finally:
        client.close()