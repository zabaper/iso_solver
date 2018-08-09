#!/usr/bin/python
import argparse
from lxml import objectify, etree


import zone_melting

def swap( b, i, j):


	b[i],b[j] = b[j],b[i]
	for item in b:
		item[i],item[j] = item[j],item[i]

parser = argparse.ArgumentParser()
parser.add_argument("-i",  help="input file",type=str, required=True)
parser.add_argument("-o",  help="output file",type=str, default="out.graphml")

args = parser.parse_args()


tree = objectify.parse( args.i )
root = tree.getroot()

ids = []

for node in root.graph.nodes.iterchildren():
	ids.append( node.get("id"))

len_i = len(ids)

if len_i % 2 != 0:
	print('vertex is odd')
	exit()

a = [[0 for i in range(len_i+1)] for j in range( len_i)]


for position,char in enumerate(ids):
	a[position][len_i] = char
	

for edge in root.graph.edges.iterchildren():
	a[ids.index(edge.get("vertex1"))][ids.index(edge.get("vertex2"))] = 1
	a[ids.index(edge.get("vertex2"))][ids.index(edge.get("vertex1"))] = 1
	



stack_all = [a[0][len_i]]
stack_tmp = [a[0][len_i]]

row_index = 0

while len(stack_tmp) > 0:

	current_row_index = a[row_index][len_i]
	
	try :
		tmp_stack_index = stack_tmp.index(current_row_index)
		
	except:
		tmp_stack_index = 0

	
	x = stack_tmp.pop(tmp_stack_index)
	
	swap_row_index = row_index
	
	for position,line in enumerate(a):
		if line[len_i] == x:
			swap_row_index = position
			
			
	if swap_row_index != row_index:
		swap(a,row_index,swap_row_index)
		
	for position, item in enumerate(a[row_index]):
		if position < len_i:
			if a[row_index][position]==1:
				x = a[position][len_i]
			
				try:
					x = stack_all.index(x)
				except:
					stack_all.append(x)
					stack_tmp.append(x)
	
	
	row_index = row_index + 1






len_plus_1 = len_i + 1
mid = len_i // 2

a00 = [a[i][:mid]+[a[i][len_i]] for i in range(0,mid)]
a01 = [a[i][mid:len_i] for i in range(0,mid)]
a10 = [a[i][:mid] for i in range(mid,len_i)]
a11 = [a[i][mid:len_plus_1] for i in range(mid,len_i)]



'''
b00 = ''.join(str(r) for v in a00 for r in v)
print( b00 )
b11 = ''.join(str(r) for v in a11 for r in v)
print( b11 )
'''

bxx = ''.join(str(r) for v in a01 for r in v).join(str(r) for v in a10 for r in v)
bxx = bxx.replace("0","")

if bxx!='':
	print('number of graph not 2')
	exit()

index, message = zone_melting.refine(a00,a11)

print(message)

if  index:

	for position,line in  enumerate(index):
		for node in root.graph.nodes.iterchildren():
			if node.get("id") == str(line[0]):
				node.set('upText', str(position))

			if node.get("id") == str(line[1]):
				node.set('upText', str(position))


	obj_xml = etree.tostring(root, pretty_print = True, xml_declaration = True)
	with open(args.o, 'wb') as xml_writer:
		xml_writer.write(obj_xml)






