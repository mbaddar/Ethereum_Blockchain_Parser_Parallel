# Acknowledgement!
This is a fork of the github Repository https://github.com/alex-miller-0/Ethereum_Blockchain_Parser/ from Alex Miller and some of his code and structure in the Analysis and Preprocessing folder to parse the blockchain and build a transaction graph is obtained!

The python scripts in the Scripts folder are all written by me for the master thesis analysis of the Ethereum main network.


# Prerequisites
Following tools must be installed.

## Geth
[Geth](https://github.com/ethereum/go-ethereum/wiki/Geth) is the Go implementation of a full Ethereum node. 

## graph-tool
[graph-tool](https://graph-tool.skewed.de/) graph analysis tool.

## python 3
[python3](https://www.python.org/downloads/release/python-352/) programming language python 3

## MongoDB
[mongoDB](https://www.mongodb.com/)

# Setup
##Project
Clone this github project.
execute in rootfolder: `install -r requirements.txt`

##Download Blockchain
execute on a shell `geth`  to download the blocks until at least block 4'700'000 (may take many hours)

##Parse to mongodb
execute on a shell `geth --rpc` to start the JSON RPC API of the blockchain
execute on a shell `mongod` to start the database
execute `python3 parseBlockchain.py` in the Scripts folder of the project to parse the blockchain to the mongoDB

##build Transaction graph
execute `python3 buildTransactionGraphs.py` to build the transaction graph (takes several hours!). The graph is saved as graph.gt to the data/graphs/ folder. For the build graph it is alrdy saved on the DVD in that folder.


# Information Retrievel
All scripts to retrieve the data for analysis and plot/chart creation are in the Scripts/-folder!

##powerLaw
`python3 plottingPowerLaw.py` plots are saved to powerLaw/

##Generate DataSet Information:
run `mongod` on another shell
`python3 retrieveDataSetInformations.py` jsons saved to timeseries/ folder
`python3 plottingIntervalsOfTransactionValues.py` plots saved to timeseries/figures/
`python3 plottingIntervalsOfBlockValues.py` plots saved to timeseries/figures/


##graphAnalysis rankings
run `mongod` on another shell
`python3 graphAnalysis.py` jsons saved to rankings/ folder
`python3 pieChartingRankingTags.py`  pie charts saved to rankings/ folder


##Tagging transactions
run `mongod` on another shell
`python3 taggedAnalysis.py`
`python3 plottingTaggedTransactionVolumes.py` tagged_timeseries/
`python3 plottingOnlyTaggedTransactionVolumes.py` plots saved to tagged_timeseries/OnlyTagged/
`python3 plottingOnlyUntaggedTransactionVolumes.py` plots saved to tagged_timeseries/OnlyUntagged/


##Volumes over time 
run `mongod` on another shell
`python3 taggedAnalysis.py`
`python3 plottingVolumesTotal.py` plots saved to tagged_timeseries/totalVolumes/


##GenesisAnalysis
`python3 genesisEtherLoss.py`
`python3 plottingLosingEther.py`
results are saved to the genesisLoss/ folder

##Motif detection

`python3 smallGraphAnaylsis.py` saves pictures of motifs with number of occurances in the name to motifs/2 and motifs/3