import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--minblock" )
parser.add_argument("--maxblock")
args = parser.parse_args()

if not args.minblock: 
	args.minblock = 0
if not args.maxblock:
	args.maxblock = 50

minblock = int(args.minblock)
maxblock = int(args.maxblock)

print("min= %3d, max=%3d" % (minblock, maxblock))

print(args)