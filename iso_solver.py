#!/usr/bin/python
import argparse, re
import zone_melting

def load(filename):

	p = re.compile('\d+')
	with open(filename) as f:
		lines = f.readlines()

	items = p.findall(lines[0])

	if len(items) != 2:
		return []

	point_count = int(items[0])

	matrix = [[0 for i in range(point_count + 1)] for j in range(point_count)]

	for i in range(1, len(lines)):
		items = p.findall(lines[i])

		if len(items) != 2:
			continue

		matrix[int(items[0])-1][int(items[1])-1] = 1
		matrix[int(items[1])-1][int(items[0])-1] = 1

	for i in range(point_count):
		matrix[i][point_count] = i + 1

	return matrix

parser = argparse.ArgumentParser()
parser.add_argument("-i1",  help="first file",type=str, required=True)
parser.add_argument("-i2",  help="second file",type=str, required=True)
#parser.add_argument("-f",  help="input file",type=str, required=True)
parser.add_argument("-o",  help="output file",type=str, default="out.txt")

args = parser.parse_args()

#slice = args.f[:-1]

left  = load(args.i1)
right  = load(args.i2)


index, message = zone_melting.refine(left,right)

if not index:
	print(message)
else:
	print('{}\n'.format(message))

	
	with open(args.o ,'w') as out:
		out.write(  ' {}\n'.format(message))
		

		for  line in index:
			out.write('{} {}\n'.format(line[0],line[1]))

	out.close()






