db.NonContractTxns.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$bucket: {
			    groupBy: "$transactions.timestamp", // usually "$path.to.field"
			    boundaries: [ 1480550400, 1483228800, 1485907200, 1488326400, 1491001200, 1493593200, 1496271600, 1498863600, 1501542000],
			    default: "Other", // optional
			    output: { 
			      txnsCount: { $sum: 1 },
			      txnVol: { $sum : "$transactions.value" }
			       } // optional
			}
		},

		// Stage 2
		{
			$out: "MonthlyNonContractTxnVol"
		},

	]

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
