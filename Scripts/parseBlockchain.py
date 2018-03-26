"""Pull data from geth and parse it into mongo.
The code must run on Linux. However geth and mongo can 
run on windows.

WINDOWS configurations:
Mongo and geth processes must be on
Run the following commands before running this script:
geth --rpc --rpcport "8545" --rpcaddr "0.0.0.0"
mongod 


"""

import subprocess
import sys
Preprocessing_dir = './../Preprocessing'
Crawler_dir = './../Preprocessing/Crawler'
Analysis_dir = './../Analysis'
sys.path.append(Preprocessing_dir)
sys.path.append(Crawler_dir)
sys.path.append(Analysis_dir)
import os
os.environ['ETH_BLOCKCHAIN_ANALYSIS_DIR'] = Preprocessing_dir
from Crawler import Crawler
#from ContractMap import ContractMap
import time
LOGDIR = './../logs'


print("Booting processes.")
# Catch up with the crawler
c = Crawler.Crawler()

print("completed")

#ContractMap(c.mongo_client, last_block=c.max_block_mongo)

