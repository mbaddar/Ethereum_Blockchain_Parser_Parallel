"""A client to interact with node and to save data to mongo."""

from pymongo import MongoClient
import crawler_util
import requests
import json
import sys
import os
import logging
import time
import tqdm
import pdb
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
#HOST = "http://10.0.2.2"
#DIR = "C:/data/db"
LOGFIL = "crawler.log"
if "BLOCKCHAIN_ANALYSIS_LOGS" in os.environ:
    LOGFIL = "{}/{}".format(os.environ['BLOCKCHAIN_ANALYSIS_LOGS'], LOGFIL)
crawler_util.refresh_logger(LOGFIL)
logging.basicConfig(filename=LOGFIL, level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Crawler(object):
   

    def __init__(
        self,
        start=True,
        geth_host= "http://10.0.2.2",
        rpc_port=8545,
        mongo_host = "10.0.2.2",
        mongo_port = 27017,
        min_block_geth = 2900000,
        delay=0.0001
    ):
        """Initialize the Crawler."""
        print("Starting Crawler")
        self.url = "{}:{}".format(geth_host, rpc_port)
        self.headers = {"content-type": "application/json"}
        # Initializes to default host/port = localhost/27017
        mongo_url = mongo_host+":" + str(mongo_port)
        
        self.mongo_client = crawler_util.initMongo(MongoClient(host=[mongo_url]))
        # The max block number that is in mongo
        self.max_block_mongo = None
        # The max block number in the public blockchain
        self.max_block_geth = None
        # If you don't want to start from Genesis block
        self.min_block_geth = min_block_geth
        # Record errors for inserting block data into mongo
        self.insertion_errors = list()
        # Make a stack of block numbers that are in mongo
        # # Deprecated as becoming infeasible for a high number of records.
        #self.block_queue = crawler_util.makeBlockQueue(self.mongo_client)
        # The delay between requests to geth
        self.delay = delay

        self.session=requests.Session()

        self.max_block_mongo = self.highestBlockMongo()
        self.max_block_geth =  self.highestBlockEth()
        if start:
            self.run()
        else:
            print("Highest block mongo=%9d" % self.max_block_mongo )
            print("Highest block eth=%9d" % self.highestBlockEth())            

    def _rpcRequest(self, method, params, key):
        """Make an RPC request to geth on port 8545."""
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0
        }
        """time.sleep(self.delay)"""
        data=json.dumps(payload)
        #pdb.set_trace()
        # res = self.session.post(
        #       self.url,
        #       data, stream=True).json()
        res = requests.post(
            self.url,
            data = data,
            headers = self.headers).json()
        return res[key]

    def getBlock(self, n):
        """Get a specific block from the blockchain and filter the data."""
        #pdb.set_trace()
        data = self._rpcRequest("eth_getBlockByNumber", [n, True], "result")
        block = crawler_util.decodeBlock(data)
        uncleHash = data["hash"]
        #pdb.set_trace()
        if data["uncles"]:
            uncles = self.retrieveUncles( uncleHash, block["number"] )
            block["uncles"] = uncles
            #block["uncles"] = uncles
        return block

    def getMiner(self, n):
        miner = self._rpcRequest("eth_getBlockByNumber", [hex(n), False], "result")["miner"]
        crawler_util.insertMiner(self.mongo_client,n,miner)



    def retrieveUncles(self, blockHash, height):
       

        uncleCountHex = self._rpcRequest("eth_getUncleCountByBlockHash",[blockHash],"result")
        uncleCount = int(uncleCountHex, 16)
        uncles = []
        for i in range(uncleCount):
            uncleBlock = self._rpcRequest("eth_getUncleByBlockHashAndIndex",[blockHash,hex(i)],"result")
            newBlock = {
               "miner":uncleBlock["miner"],
               "reward": (8 - (height-int(uncleBlock["number"], 16))) / 8 * 5
            }
            uncles.append(newBlock)
        return uncles

    def highestBlockEth(self):
        """Find the highest numbered block in geth."""
        num_hex = self._rpcRequest("eth_blockNumber", [], "result")
        #return int(num_hex, 16)
        return 5276322

    def saveBlock(self, block):
        """Insert a given parsed block into mongo."""
        #pdb.set_trace()
        e = crawler_util.insertMongo(self.mongo_client, block)
        if e:
            self.insertion_errors.append(e)
            print("Error saving block" )

    def saveMiner(self, block):
        """Insert a given parsed block into mongo."""
        e = crawler_util.insertMiner(self.mongo_client, block)
        if e:
            self.insertion_errors.append(e)
            print("Error saving miner" )

    def highestBlockMongo(self):
        """Find the highest numbered block in the mongo database."""
        highest_block = crawler_util.highestBlock(self.mongo_client)
        logging.info("Highest block found in mongodb:{}".format(highest_block))
        return highest_block

    def add_block(self, n):
        """Add a block to mongo."""

        b = self.getBlock(n)
        if b:
            self.saveBlock(b)
            time.sleep(self.delay)
        else:
            self.saveBlock({"number": n, "transactions": []})


    def add_miner(self, n):
        """Add a block to mongo."""

        self.getMiner(n)
       # else:
        #    self.saveBlock({"number": n, "transactions": []})

    def run(self):
        """
        Run the process.

        Iterate through the blockchain on geth and fill up mongodb
        with block data.
        """
        print("Processing geth blockchain:")
        print("Highest block found as: {}".format(self.max_block_geth))
        # Deprecated 
        # print("Number of blocks to process: {}".format(
        #     len(self.block_queue)))

        # Make sure the database isn't missing any blocks up to this point
        ####################################################################
        # logging.debug("Verifying that mongo isn't missing any blocks...")
        # self.max_block_mongo = 1
        # if len(self.block_queue) > 0:
        #     print("Looking for missing blocks...")
        #     self.max_block_mongo = self.block_queue.pop()
        #     for n in tqdm.tqdm(range(1, self.max_block_mongo)):
        #         if len(self.block_queue) == 0:
        #             # If we have reached the max index of the queue,
        #             # break the loop
        #             break
        #         else:
        #             # -If a block with number = current index is not in
        #             # the queue, add it to mongo.
        #             # -If the lowest block number in the queue (_n) is
        #             # not the current running index (n), then _n > n
        #             # and we must add block n to mongo. After doing so,
        #             # we will add _n back to the queue.
        #             _n = self.block_queue.popleft()
        #             if n != _n:
        #                 self.add_block(n)
        #                 self.block_queue.appendleft(_n)
        #                 logging.info("Added block {}".format(n))
        ####################################################################
        # Get all new blocks
        try:
            self.min_block_geth = self.max_block_mongo 
        except Exception:
            print("Error synching with max block stored in mongo. Min block might be out of sync!")
        print("Processing the specified range of the blockchain from %8d to %8d..." % (self.min_block_geth, self.max_block_geth))
        for n in tqdm.tqdm(range(self.min_block_geth, self.max_block_geth)):
            self.add_block(hex(n))
        #for n in tqdm.tqdm(range(3826871, self.max_block_geth)):
         #  self.add_miner(n)

        print("Done!\n")
