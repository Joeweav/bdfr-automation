# Exceptions file purifier - nukes dupes
#
# 4/25/2022 Matthew Kleinmann
#
# V 4.25.11.33


from pathlib import Path # needed for all file manipulations
import os

bd = "//192.168.1.124/reddit/bdfr/excs"

for rfn in Path(bd).glob('**/*'):
	if rfn.suffix != ".exc":
		continue
	rfile = open(rfn, 'r')
	wfile = open("%s.tmp" % (rfn), 'w', newline="\n")
	Lines = rfile.readlines()
# Get rid of dupes in the list
#	Lines.sort()
# insert the list to the set
	list_set = set(Lines)
# convert the set to the list
	unique_list = (list(list_set))
# Strips the newline character
#	for line in Lines:
	for line in unique_list:
		line = line.strip()
		if len(line) == 6 and line.isalnum() and line.islower():
			wfile.write("%s\n" % (line))
	rfile.close()
	wfile.close()
	rfn.unlink(Path("%s" % (rfn))) #Rename will bitch if dest file exists
	os.rename(Path("%s.tmp" % (rfn)), Path("%s" % (rfn)))


		
	
