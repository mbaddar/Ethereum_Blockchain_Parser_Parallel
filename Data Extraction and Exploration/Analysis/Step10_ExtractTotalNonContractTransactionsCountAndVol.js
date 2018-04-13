db.NonContractTxns.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$group: {
				_id : null,
			    totalValue: { $sum: "$transactions.value" },   
			    transactionCount: { $sum: 1 }
			
			}
		},

		// Stage 2
		{
			$out: "TotalNonContractTxnCountAndVol"
		},

	]

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
