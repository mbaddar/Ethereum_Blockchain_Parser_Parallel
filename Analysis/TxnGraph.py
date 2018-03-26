"""Create a snapshot of the Ethereum network."""

import six.moves.cPickle as pickle
from graph_tool.all import *
import graph_tool
import pymongo
import os
import subprocess
import signal
import copy
from tags import tags

import analysis_util
env = analysis_util.set_env()
DIR = env["mongo"] + "/data"
DATADIR = env["txn_data"]

class TxnGraph(object):


    def __init__(self,
                *args,
                snap=True,
                save=True,
                load=False,
                previous=None,
                **kwargs):

        self.f_pickle = None
        self.f_snapshot = None
        self.start_block = max(args[0] if len(args) > 0 else 1, 1)
        self.end_block = args[1] if len(args) > 1 else 2

        self.start_timestamp = None
        self.end_timestamp = None

        # A lookup table mapping ethereum address --> graph node
        self.nodes = dict()
        self.edges = list()
        # A graph_tool Graph object
        self.graph = None
        # Store the graph separately in a file
        self.f_graph = None
        # PropertyMap of edges weighted by eth value of transaction
        self.edgeWeights = None
        # PropertyMap of vertices weighted by eth value they hold
        self.edgedollars = None
        # at the time of the end_block.
        self.vertexWeights = None
        # All addresses (each node has an address)
        self.addresses = None
        # Record big exchange addresses
        self.exchanges = list()
        # Record all contracts
        self.contracts = list()
        # Run
        self._init(snap, save, load, previous)

    def _init(self, snap, save, load, previous):
        self.graph = Graph()

        # Accept a previous graph as an argument
        if previous:
            a_str = "prev is of form {'graph': <Graph>, 'end_block': <int>}"
            assert "graph" in previous, a_str
            self.graph = previous["graph"]
            assert "end_block" in previous, a_str
            self.start_block = previous["end_block"]

        # Set filepaths
        self._setFilePaths()

        print(DATADIR)
        # Load a previous graph
        if load:
            self.load(self.start_block, self.end_block)

        else:
            # Take a snapshot
            if snap:
                self.snap()

            # Save this graph automatically
            if save:
                self.save()

    def _setFilePaths(self, start=None, end=None):
        """Set the file paths based on the start/end block numbers."""
        if not start:
            start = self.start_block
        if not end:
            start = self.end_block

        self.f_pickle = "{}/pickles/{}_{}.p".format(DATADIR, start, end)
        self.f_graph = "{}/graphs/{}_{}.gt".format(DATADIR, start, end)
        self.f_snapshot = "{}/snapshots/{}_{}.png".format(DATADIR, start, end)

    def _getMongoClient(self):
        """Connect to a mongo client (assuming one is running)."""
        try:
            # Try a connection to mongo and force a findOne request.
            # See if it makes it through.
            client = pymongo.MongoClient(serverSelectionTimeoutMS=1000)
            transactions = client["blockchainExtended2"]["blocks"]
            test = client.find_one({"number": {"$gt": 1}})
            popen = None
        except Exception as err:
            # If not, open up a mongod subprocess
            cmd = "(mongod --dbpath {} > {}/mongo.log 2>&1) &".format(
                "/mnt/c/data/db",
                "/mnt/c/data/anaLogs")

            popen = subprocess.Popen(cmd, shell=True)
            client = pymongo.MongoClient(serverSelectionTimeoutMS=1000)
            transactions = client["blockchainExtended2"]["blocks"]

        # Update timestamps
        transactions = self._updateTimestamps(transactions)

        return transactions, popen

    def _updateTimestamps(self, client):
        """Lookup timestamps associated with start/end blocks and set them."""
        start = client.find_one({"number": self.start_block})
        end = client.find_one({"number": self.end_block})
        #TODO stuff
        self.start_timestamp =  "xx"
        self.end_timestamp = "xx"
        return client

    def _addEdgeWeight(self, newEdge, value):
        """
        Add to the weight of a given edge (i.e. the amount of ether that has
        flown through it). Create a new one if needed.
        """
        if self.edgeWeights[newEdge] is not None:
            self.edgeWeights[newEdge] += max(0.000000000000000001,value)
        else:
            self.edgeWeights[newEdge] = max(0.000000000000000001,value)

    def _addEdgeDollar(self, newEdge, value):
        """
        Add to the weight of a given edge (i.e. the amount of ether that has
        flown through it). Create a new one if needed.
        """
        if self.edgedollars[newEdge] is not None:
            self.edgedollars[newEdge] += max(0.000000000000000001,value)
        else:
            self.edgedollars[newEdge] = max(0.000000000000000001,value)

    def _addVertexWeight(self, from_v, to_v, value):
        """
        Add to the weight of a given vertex (i.e. the amount of ether)
        it holds. Create a new weight if needed.
        """
        if self.vertexWeights[to_v] is not None:
            self.vertexWeights[to_v] += value
        else:
            self.vertexWeights[to_v] = 0
        if self.vertexWeights[from_v] is not None:
            # We shouldn't need to worry about overspending
            # as the ethereum protocol should not let you spend
            # more ether than you have!
            self.vertexWeights[from_v] -= value
        else:
            self.vertexWeights[from_v] = 0

    def _addVertieces(self):

        addresses = pickle.load(open("data/.addresses.p", "rb"))
        for addr in addresses.keys():
            self.nodes[addr] = self.graph.add_vertex()
            self.vertexWeights[self.nodes[addr]] = 1
            self.addresses[self.nodes[addr]] = addr


    def _addEdges(self, client):
        blocks = client.find(
            {"number": {"$gt": 0, "$lt": 4370000}},
            sort=[("number", pymongo.ASCENDING)]
        )
        for block in blocks:
            if block["number"]%1000 ==0:
                print(block["number"])
            for txn in block["transactions"]:
                if txn["to"] != None:
                    toV = self.nodes[txn["to"]]
                    fromV = self.nodes[txn["from"]]
                    newEdge = self.graph.add_edge(fromV,toV)
                    self.edges.append(newEdge)
                    self._addEdgeWeight(newEdge,txn["value"])
                    self._addEdgeDollar(newEdge,txn["value"]*block["dollarPrice"])





    def _addBlocks(self, client, start, end):

        """Add new blocks to current graph attribute."""
        # Get a cursor containing all of the blocks
        # between the start/end blocks
        blocks = client.find(
            {"number": {"$gt": start, "$lt": end}},
            sort=[("number", pymongo.ASCENDING)]
        )
        for block in blocks:
            print(block["number"])
            if "uncles" in block:
                for uncle in block["uncles"]:
                    to_v = None
                    from_v = None
                    #if uncle["miner"] not in self.nodes:
                    #    to_v = self.graph.add_vertex()
                    #    self.nodes[uncle["miner"]] = to_v
                    #    self.addresses[to_v] = uncle["miner"]
                    #else:
                    #    to_v = self.nodes[uncle["miner"]]

                    to_v = self.graph.add_vertex()

                    if "uncle" not in self.nodes:
                        from_v = self.graph.add_vertex()
                        self.nodes["uncle"] = from_v
                        self.addresses[from_v] = "uncle"
                    else:
                        from_v = self.nodes["uncle"]

                    # Graph vetices will be referenced temporarily, but the
                    #   unique addresses will persist in self.nodes
                    #to_v = self.graph.add_vertex()

                    newEdge = self.graph.add_edge(from_v, to_v)
                    self.edges.append(newEdge)
                    if uncle["reward"] >5:
                        self._addEdgeWeight(newEdge,10.0-uncle["reward"]) #if >5
                    else:
                        self._addEdgeWeight(newEdge,uncle["reward"])
            if block["transactions"]:
                # Loop through all of the transactions in the current block
                # Add all the nodes to a global set (self.nodes)
                for txn in block["transactions"]:

                    # Graph vetices will be referenced temporarily, but the
                    #   unique addresses will persist in self.nodes
                    to_v = None
                    from_v = None

                    # Exclude self referencing transactions
                    #TODO Do something with self refencing e.g. search for text
                    if txn["to"] == txn["from"]: #and txn["input"] != "0x":
                        continue

                    # Set the "to" vertex
                    if txn["to"] not in self.nodes:
                        to_v = self.graph.add_vertex()
                        self.nodes[txn["to"]] = to_v
                        self.addresses[to_v] = txn["to"]

                        # If there is data, this is going to a contract
                        if "data" in txn:
                            if txn["data"] != "0x":
                                self.contracts.append(txn["to"])
                    else:
                        to_v = self.nodes[txn["to"]]

                    # Set the "from" vertex
                    if txn["from"] not in self.nodes:
                        from_v = self.graph.add_vertex()
                        self.nodes[txn["from"]] = from_v
                        self.addresses[from_v] = txn["from"]
                    else:
                        from_v = self.nodes[txn["from"]]

                    # Add a directed edge
                    newEdge = self.graph.add_edge(from_v, to_v)
                    self.edges.append(newEdge)

                    # Update the weights
                    self._addEdgeWeight(newEdge, txn["value"])
                    self._addVertexWeight(from_v, to_v, txn["value"])
        self._addPropertyMaps()

    def _addPropertyMaps(self):
        """Add PropertyMap attributes to Graph instance."""
        self.graph.vertex_properties["weight"] = self.vertexWeights
        self.graph.vertex_properties["address"] = self.addresses
        self.graph.edge_properties["weight"] = self.edgeWeights
        self.graph.edge_properties["dollar"] = self.edgedollars


    # PUBLIC
    # ------
    def snap(self):
        client, popen = self._getMongoClient()

        # Add PropertyMaps
        self.edgeWeights = self.graph.new_edge_property("double")
        self.vertexWeights = self.graph.new_vertex_property("double")
        self.addresses = self.graph.new_vertex_property("string")
        self.edgedollars = self.graph.new_edge_property("double")

        # Add blocks to the graph
        self._addVertieces()
        print("Added Vertieces")
        self._addEdges(client)
        print("Added Edges")

        self._addPropertyMaps()

        #self._addBlocks(client, self.start_block, self.end_block)
        #print("Added Blocks")
        # Kill the mongo client if it was spawned in this process
        #if popen:
            # TODO get this to work
            #popen.kill()


    def save(self):
        """Pickle TxnGraph. Save the graph_tool Graph object separately."""
        if not os.path.exists(DATADIR+"/pickles"):
            os.makedirs(DATADIR+"/pickles")
        if not os.path.exists(DATADIR+"/graphs"):
            os.makedirs(DATADIR+"/graphs")
        if not os.path.exists(DATADIR+"/snapshots"):
            os.makedirs(DATADIR+"/snapshots")

        # We cannot save any of the graph_tool objects so we need to stash
        # them in a temporary object
        tmp = {
            "nodes": self.nodes,
            "edges": self.edges,
            "edgeWeights": self.edgeWeights,
            "edgeDollars": self.edgedollars,
            "vertexWeights": self.vertexWeights,
            "addresses": self.addresses,
            "graph": self.graph
        }
        # Empty the graph_tool objects
        #self.nodes = dict()
        self.edges = list()
        self.edgeWeights = None
        self.vertexWeights = None
        self.addresses = None

        # Save the graph to a file (but not if it is empty)
        if len(self.nodes) > 0:
            self.graph.save(self.f_graph, fmt="gt")

        self.graph = None

        # Save the rest of this object to a pickle
        #with open(self.f_pickle, "wb") as output:
        #    pickle.dump(self.__dict__, output)
        #    output.close()

        # Reload from tmp
        self.nodes = tmp["nodes"]
        self.edges = tmp["edges"]
        self.edgeWeights = tmp["edgeWeights"]
        self.edgedollars = tmp["edgeDollars"]
        self.vertexWeights = tmp["vertexWeights"]
        self.addresses = tmp["addresses"]
        self.graph = tmp["graph"]

    def load(self, start_block, end_block):
        """
        Load a TxnGraph.

        Description:
        ------------
        Load a pickle of a different TxnGraph object as well as a saved Graph
        object as TxnGraph.graph. This can be called upon instantiation with
        load=True OR can be called any time by passing new start/end block
        params.

        Parameters:
        -----------
        start_block <int>
        end_block <int>
        """
        self._setFilePaths(start_block, end_block)

        # Load the graph from file
        tmp_graph = load_graph(self.f_graph)

        # Load the object from a pickle
        with open(self.f_pickle, "rb") as input:
            tmp = pickle.load(input)
            self.__dict__.update(tmp)
            self.graph = tmp_graph
            input.close()
