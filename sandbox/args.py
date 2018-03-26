import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-min" ,"--minblocketh" , type=int, default=2900000)
parser.add_argument("-max", "--maxblocketh" , type=int, default=-1)
parser.add_argument("-gh", "--gethhost", default="10.0.2.2")
parser.add_argument("-mh", "--mongohost", default="10.0.2.2")
parser.add_argument("-s", "--start", default= False)


args = parser.parse_args()

if not args.minblock: 
	args.minblock = 0
if not args.maxblock:
	args.maxblock = 50

minblock = args.minblock
maxblock = args.maxblock

print("min= %3d, max=%3d" % (minblock, maxblock))

print(args)