"""Pull data from geth and parse it into mongo.
WINDOWS configurations:
Mongo and geth processes must be on
Run the following commands before running this script:
geth --rpc
mongod 
from https://www.lfd.uci.edu/~gohlke/pythonlibs/#cytoolz
download: 
cytoolz-0.9.0.1-cp36-cp36m-win_amd64.whl
then: 
pip install path\cytoolz-0.9.0.1-cp36-cp36m-win_amd64.whl

pip install eth-utils
pip install eth-hash[pycryptodome]
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

