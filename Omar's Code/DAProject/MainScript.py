from pymongo import MongoClient
import DataExtractionUtilities as utils
import json
import plotMonthlyContractTxnVol
import plotMonthlyNonContractTxnVol
import plotTransactionVolPieChart
import plotMonthlyContractCreationCount
           
            
if __name__=="__main__":
    client = MongoClient()
    database = client["blockchainExtended2"]
    
    try:
        #utils.noOfContractsInTimeInterval(collection)
        #utils.transactionVolContractVSRest(collection)
        #utils.transactionsOfContracts()      
        #utils.extractTransactionInformation()
        plotMonthlyContractTxnVol.plot(database)
        #plotMonthlyNonContractTxnVol.plot(database)
        #plotTransactionVolPieChart.plot(database)
        #plotMonthlyContractCreationCount.plot(database)

    finally:
        client.close()