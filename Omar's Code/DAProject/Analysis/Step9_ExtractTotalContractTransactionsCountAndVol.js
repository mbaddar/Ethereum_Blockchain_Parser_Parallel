db.ToContractTxnsVol.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$group: {
				_id : null,
			    totalValue: { $sum: "$totalValue" },   
			    transactionCount: { $sum: "$transactions" }
			
			}
		},

		// Stage 2
		{
			$out: "TotalContractTxnsCountAndVol"
		},

	]

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
