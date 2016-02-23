# -*- coding: utf-8 -*-
import numpy as np
import sys
import msvcrt

def load_text(file_location, progress_file):
	text = np.genfromtxt(file_location,dtype='str')
	text_temp = []
	start_index = 0
	progress_text = []
	if progress_file:
		progress_text = np.genfromtxt(progress_file,dtype=str)
		if len(progress_text) > 0:
			index = np.where(text == progress_text[len(progress_text)-1])
			start_index = index[0]
	print 'start:'+str(start_index)
	key = ''
	prev_word = []
	for word in text[start_index+1:]:
		print word
		key = msvcrt.getch()
		if key == 'k': 
			progress_text = np.append(progress_text, word)
		elif key == 'b':
			progress_text = np.append(progress_text, prev_word)
			print prev_word + ' added. add:'+ word+'?'
			key = msvcrt.getch()
			if key == 'k': 
				progress_text = np.append(progress_text, word)
			else:
				print '--'
		elif key == 'q':
			break
		else:
			print '--'
		prev_word = word
		
	np.savetxt('KeptWords.txt',progress_text,delimiter='\n', fmt="%s")
	


			
		
#python QuickDelete.py German.dic KeptWords.txt 

print 'press k to keep, any other to delete, b to add previous word. q to quit.'	
source_file = sys.argv[1]
if len(sys.argv) < 3:
	progress_file = []
else:
	progress_file = sys.argv[2]
load_text(source_file,progress_file)