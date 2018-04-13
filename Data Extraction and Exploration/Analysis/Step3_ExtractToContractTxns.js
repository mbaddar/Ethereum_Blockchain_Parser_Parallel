db.Transactions.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$project: {
			    "transactions.to":1, "transactions.from":1, "transactions.value":1, "transactions.timestamp":1, "transactions.fromContract":1,
			     "transactions.toContract":1
			}
		},

		// Stage 2
		{
			$match: {
			    $and: [ { "transactions.toContract" : {$eq: true}}, {"transactions.to" : { $ne: "to"}} ]
			}
		},

		// Stage 3
		{
			$project: {
			    _id: 0, "transactions":1
			}
		},

		// Stage 4
		{
			$out: "ToContractTxns"
		},
	],

	// Options
	{
		allowDiskUse: true
	}

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
