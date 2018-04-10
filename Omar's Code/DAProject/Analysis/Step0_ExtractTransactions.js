db.blocks.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$project: {
			    "transactions.to":1, "transactions.from":1, "transactions.timestamp":1, "transactions.isContractCreation":1, "transactions.toContract":1,
			    "transactions.fromContract":1, "transactions.value":1
			}
		},

		// Stage 2
		{
			$unwind: {
			    path : "$transactions",
			    includeArrayIndex : "arrayIndex", // optional
			    preserveNullAndEmptyArrays : false // optional
			}
		},

		// Stage 3
		{
			$project: {
			    _id:0, arrayIndex: 1, transactions:1
			}
		},

		// Stage 4
		{
			$out: "Transactions"
		},

	]

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
