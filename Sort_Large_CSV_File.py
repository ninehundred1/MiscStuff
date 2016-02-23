import csv
import sys
import msvcrt
import numpy as np

def parse_file(filename, out_file, minimal_count):
	#parser function in
	data = csv.reader(open(filename, "rb"),delimiter='\t')
	#parser function out
	file_parse_out = open(out_file,'a')
	counter = 0
	current_count = 0
	previous_word = ''
	for row in data:
		current_word = row[0]
		if previous_word == current_word:
			current_count += int(row[2])
		else:
			if current_count > int(minimal_count):
				file_parse_out.write(previous_word+'\t'+str(current_count)+'\n')
			current_count = int(row[2])
					
			
		previous_word = current_word	
		counter += 1
		if counter %100000 ==0:
			print counter
		if counter >100000000:
			break
  			
def sort_file(file_name, out_file):
	text = np.genfromtxt(file_name,dtype='str')
	second = sorted(text, key=lambda tup: tup[1], reverse = True)
	np.savetxt(out_file,second,delimiter='\t', fmt="%s")
	
def first_row_file(file_name, out_file):
	out = []
	counter = 0
	with open(file_name) as f:
		for line in f:
			counter += 1
			if len(line)==2:
				print str(counter)+': '+line
			  
		
def make_dict(files, out):
	d_out = set()
	file_parse_out = open(out,'a')
	for i in files:
		with open(i) as f:
			for line in f:
				d_out.add(line)
	second = sorted(d_out, key=lambda i: i)			
	for item in second:
		file_parse_out.write("%s" % item)
		
	
print 'parsing file..'	
first_row_file('GermanComplete2nospace.txt', 'GermanDictDone.txt')
