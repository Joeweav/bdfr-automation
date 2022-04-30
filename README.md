# bdfr-automation
Scripts that I use with BDFR
<p>
These should help you automate grabbig stuff from reddit every night and getting rid of dumps which seems to be a huge problem.
I would sugguest that you follow my layout at first and get things working before branching off.
<p>
You will need python, I am using 3.9 nothing fancy, and the the system runs on windows, the python shoud be portable to linux.  The batch file that kicks the grab off is windows.  I may move it to python at some point just to make it portable. 
<p>
The grabbing batch file also calls ffmpeg, you can sklip this if you want.  I make a carefully named jpg that has the format !subname.jpg with every nights run in
every sub that I grab.  These are done after the grabbing so if you sort by date it will be the first thing and if you sort by name it will be the first thing.  If you  use the MS slide show/video player This guarentees you that the directory will start with an image.  If it starts with a video, it will call up the default video player app which is not good for quickly running through the stuff.  The MS app will play videos if if runs into them in the directory as long as you initally start it with an image.
<p>
You also need the bulk video downloader for reddit, that does all theh heavy lifting as far as grabbig stuff.  Leave the defaiults alone for now..  Get that here:
https://github.com/aliparlakci/bulk-downloader-for-reddit  This has to be installed!  And find a copy of ffmpeg for your platform and inistall it.
<p>
This system depends on a directory structure, and all of it is UNC safe.  For the media you are grabbing you want a subdir called reddit.  
When you run the downloader, it will make a sub dir for each sub you have in the list of stuff to get.  You have one special sub, caleld bdfr, 
that has two subs in it, one is called logs, each group will make a log fine in there.  And a sub caled excs for the exception files, one per group, 
and this has the ID's of files for BDFR not to get, ie stuff you already have.
<p>
In the root of the of reddit place the 0000doit.bat file, this kicks the BDFR process off.  You also need to create a file called subreddit.lst, 
this holds the list of subs you want to harvest, one per line.  Get this going.  Note nothing will wind up in the execs subdir yet, but the system 
should harvest and create logs as well as files.  I think I have the main batch file set up to nuke text and gif images, you may wanna delete those lines.. 
<p>
This is what you need to manually lay out<p>
<p>
base_dir as defined in line 16 of populate_db_v2.py<p>
/base_dir/reddit/<p>
/base_dir/reddit/bdfr/<p>
/base_dir/reddit/bdfr/logs/<p>
/base_dir/reddit/bdfr/excs/<p>
And copy...<p>
/base_dir/reddit/0000doit.bat<p>
and create<p>
/base_dir/reddit/subreddit.lst<p>
<p>
The sub folders will auto create when you run the batch file to kick bdfr over
<p>
Before you have this harvest too many times or get too much stuff, you want to run the populatebb_v2.py program.  It will try and load up a sqlite db if it exists,
if not, it will create one.  It breaks out file names, sizes and id's of the files.  Each time it finds a file it checks to see if a file of the same zize is in the db.  If not, it adds it to the db, if there is a similarly sized file, it computes the md5 of both files, and if they are not the same, commits the md 5 of the old file to the db, and commits all of the new file info to the database and mover on.  If the md5's match, it updates the existing file if it's md5 wa snot in the db and 
deletes the dupe, and logs it to a text file.  It only computes md5's when there is a file size match.
<p>
It also uses an in mempry db, but saves it every 10K transactions.  It will log that to the console.  It also logs when it moves to a new sub, and what it is depeating and why.  There is a small zize limit, I have it set for 1K, you can tweak it.  Most of the tiny files are just slides saying the file went by by..  Any file that starts with ! like the ones we make are skipped.  The populate db takes one command line argument:  THe group in the list to start on.  
<p>
I am still toying with how to trap errors.  I get occasional network errors and I am not sure if I should just hammer on retrying or wait for a few secs and retry etc. <p> 
So for now it does nothing, it will barf.  However with the db auto loading and saving, and the command line argiment you can just start it back up in the sub it
barfed in and pick back up again.  I am thinking about how to deal with the erors. 
<p>
Note that is it possible to have dupes in the exception files. I don't think they hurt anything but speed but I like to keep them clean, so once in a while you can
run the exec check program that will purify any dupes.
<p>
I am not a python propeller head so there are no doubt better ways of doing a lot of things.  I am all ears.  This has been a fun project and if you have ideas or better ways of coding things, lemme know!

