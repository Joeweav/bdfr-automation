#
# Matthew Kleinmann - 4/14/2022
#
#

version = "4.29.20.50"

from pathlib import Path # needed for all file manipulations
from datetime import datetime # needed for making logs unique
import re # needed for the regex search
import hashlib # needed for md5 
import sqlite3  # needed for all db stuff
import os # needed for clearing the screen -- ugh
import argparse # for command line args

base_dir = "//192.168.1.124"
sfn = 'subreddit.lst'
disk_db_name = 'bdfr.db'

parser = argparse.ArgumentParser()
parser.add_argument('ssub', nargs="?", default="", type=str)
args = parser.parse_args()
ssub = args.ssub

os.system('cls')  # on windows
print("\n\n\nPopulating database and nuking dupes")
print("Version   : %s" % (version))

# If there is a db file load it
path = Path(disk_db_name)
if path.is_file():
	print("Loading   : %s" % (disk_db_name))
	source = sqlite3.connect(disk_db_name)
	con = sqlite3.connect(':memory:')
	source.backup(con)

con = sqlite3.connect(':memory:')
cur = con.cursor()

date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")

bf = open("bad_file_%s.txt" % (date), "a+")
ef = open("exc_file_%s.txt" % (date), "a+")
df = open("del_file_%s.txt" % (date), "a+")

def log_bad_file(i):
	bf.write(str(i) +'\n')
	
def log_exc_file(sub, rid):
	ef.write("%s %s \n" % (sub, rid))
	
def remove_file(remfile, reason): 
	print("Deleating : %s %s" % (remfile, reason))
	rmf = Path(remfile)
	rmf.unlink()
	df.write("%s\t%s\n" % (remfile, reason))
	
def add_rid(subpath, rid):
#	pass
	rid_file = open(subpath,'a+')
	rid_file.write("%s\n" % (rid))
	rid_file.close()
	
def compute_md5(i):
	with open(i, "rb") as f:
		file_hash = hashlib.md5()
		while chunk := f.read(8192):
			file_hash.update(chunk)
	return(file_hash.hexdigest())

cur.execute("CREATE TABLE bdfr (name TEXT, size INTEGER, md5 TEXT, sub TEXT, rid TEXT)")

rx = r"_"
regex = re.compile(rx)

p = Path('%s/reddit' % (base_dir))

entry = 0
flag = 0

##################################################################

subfh = open("%s/%s" % (p,sfn), 'r')
subs = subfh.readlines()
for sub in subs:
	sub = sub.strip()
	if ssub != "" and flag == 0:
		if sub != ssub:
			continue
		else:
			flag = 1
	print("Opening   : %s" % (sub))
	for i in p.glob("%s/*" % (sub)):
		parent = str(i.parent)
		sub = parent.split("\\")[4]
		size = i.stat().st_size	
		md5 = ""
		rid = ""
		ext = ""
		name = i.name
		name_len = len(name)
		
		if name.startswith('!'): #The jpg text files...  Leave them alone
			continue
			
#case1 no extension in filename - attempt to figure out rid and ext
		if len(i.suffix) == 0:
			rname = name[::-1]
			rrid_ext = rname.split("_")[0]
			rid_ext = rrid_ext[::-1]
			rid = rid_ext[0:6:]
			ext = rid_ext[6:]
		
#case2 !!!!!NORMAL!!!!! extension in filename
		if ext == "":	
			ext = i.suffix
			ext_len = len(ext)
			ext=ext[1:] # Take the dot off the extension .jpg -> jpg
	
#case3 Probably normal rid - check for _ below
		if rid == "":
			rid=name[name_len - ext_len - 6:-ext_len]

#case4 Multiple dupes with underscores - May be messed up from case 1 or 3
		if re.search(regex, rid, flags=0):
			a=0
			eman=name[::-1]
			for x in range(len(eman)):
				if eman[x]=="_":
					if a==0:
						start=x+1
						a=1
						continue
					end=x
					break
			idr=eman[start:end]
			rid=idr[::-1]


#Checks rid for size and make sure it is alpanumaric and lower case
		if len(rid) == 6 and rid.isalnum() and rid.islower():
			pass
		else:
			continue
	
		entry = entry + 1 # Write the db to disk every 10000 files
		if entry == 10000:
			print("Backing up: %s" % (disk_db_name))
			dest = sqlite3.connect(disk_db_name)
			con.backup(dest)
			dest.close()
			entry = 0
			
		a = 'SELECT COUNT(*) FROM bdfr WHERE size="%i"' % size
		dataCopy = cur.execute(a)
		values = dataCopy.fetchone()
		if values[0] != 0:
			a = 'SELECT name, md5, sub, rid FROM bdfr WHERE size="%i"' % size
			for row in cur.execute(a):
				if md5 == "":
					md5 = compute_md5('%s/reddit/%s/%s' % (base_dir, sub, name))
					a='UPDATE bdfr SET md5 = "%s" WHERE name = "%s" AND sub = "%s"' % (md5, row[0],row[2])
					cur.execute(a)
					con.commit()
				if compute_md5(i) == md5: # Both file size and md5 match
					rem_file = Path('%s/reddit/%s/%s' % (base_dir, sub, name,))
					remove_file(rem_file, "Dupe")
					subpath = '%s/reddit/bdfr/excs/%s.exc' % (base_dir, sub)
#					add_rid(subpath, rid)
					log_exc_file(sub, rid)
					continue
		
		# Get rid of small files...
		if size < 1024:
			rem_file = Path('%s/reddit/%s/%s' % (base_dir, sub, name,))
			remove_file(rem_file, "Size")
			subpath = '%s/reddit/bdfr/excs/%s.exc' % (base_dir, sub)
#			add_rid(subpath, rid)
			log_exc_file(sub, rid)
			continue
		
		a = 'INSERT INTO bdfr (name, size, md5, sub, rid) VALUES ("%s", "%i", "%s", "%s", "%s")' % (name, size, md5, sub, rid)
		cur.execute(a)
		con.commit()
		subpath = '%s/reddit/bdfr/excs/%s.exc' % (base_dir, sub)
		add_rid(subpath, rid)
		log_exc_file(sub, rid)
		
bf.close()
ef.close()
df.close()

print("Saving    : %s" % (disk_db_name))
dest = sqlite3.connect(disk_db_name)
con.backup(dest)
cur.close()
con.close()
dest.close()
