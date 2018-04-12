db.ToContractTxns.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$group: {
			    _id : "$transactions.to",
			    totalValue: { $sum: "$transactions.value" },
			    transactions: { $sum: 1 }
			}
		},

		// Stage 2
		{
			$sort: {
			    "totalValue" : -1
			}
		},

		// Stage 3
		{
			$out: "ToContractTxnsVol"
		},
	],

	// Options
	{
		allowDiskUse: true
	}

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
