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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-min" ,"--minblockgeth" , type=int, default=2900000)
parser.add_argument("-max", "--maxblockgeth" , type=int, default=-1)
parser.add_argument("-gh", "--gethhost", default="10.0.2.2")
parser.add_argument("-mh", "--mongohost", default="10.0.2.2")
parser.add_argument("-s", "--start", default= False)


args = parser.parse_args()


print("Booting processes.")
# Catch up with the crawler
c = Crawler.Crawler(args.start)

print("completed")

#ContractMap(c.mongo_client, last_block=c.max_block_mongo)

