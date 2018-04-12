from pymongo import MongoClient
import DataExtractionUtilities as utils
import VisualizationUtility as plotter
           
            
if __name__=="__main__":
    client = MongoClient()
    database = client["blockchainExtended2"]
    
    try:
        
        #####Visualization routines######
        plotter.plotMonthlyContractTxnVol(database)
        plotter.plotMonthlyNonContractTxnVol(database)
        plotter.plotTransactionVolPieChart(database)
        plotter.plotMonthlyContractCreationCount(database)

    finally:
        client.close()