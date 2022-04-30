# bdfr-automation
Scripts that I use with BDFR

These should help you automate grabbig stuff from reddit every night and getting rid of dumps which seems to be a huge problem.
I would sugguest that you follow my layout at first and get things working before branching off.

You will need python, I am using 3.9 nothing fancy, and the the system runs on windows, the python shoud be portable to linux etc with the exception of the screen clear.
The batch file that kicks the grab off is windows.  I may move it to python at some point just to make it portable.  Don't hold yout breath.
The grabbing batch file also calls ffmpeg, you can sklip this if you want.  I make a carefully named jpg that has the format !subname.jpg with every nights run in
every sub that I grab.  These are done after the grabbing so if you sort by date it will be the first thing and if you sort by name it will be the first thing.  This
guarentees you that you can use the MS slide show/video player that may not be the default app for video files.  If start on a dir that starts with am image it will
display the videos when it gets to them.

You also need the bulk video downloader for reddit, that does all theh heavy lifting as far as grabbig stuff.  Leave the defaiults alone for now..

This system depends on a directory structure, and all of it is UNC safe.  For the media you are grabbing you want a subdir called reddit.  
When you run the downloader, it will make a sub dir for each sub you have in the list of stuff to get.  You have one special sub, caleld bdfr, 
that has two subs in it, one is called logs, each group will make a log fine in there.  And a sub caled excs for the exception files, one per group, 
and this has the ID's of files for BDFR not to get, ie stuff you already have.

In the root of the of reddit place the 0000doit.bat file, this kicks the BDFR process off.  You also need to create a file called subreddit.lst, 
this holds the list of subs you want to harvest, one per line.  Get this going.  Note nothingwill wind up in the execs subdir yet, but the system 
should harvest and create logs as well as files.  I think I have the main batch file set up to nuke text and gif images, you may wanna delete those lines..

Before you have this harvest too many times or get too much stuff, you want to run the populatebb_v2.py program.  It will try and load up a sqlite db if it exists,
if not, it will start one.  It breaks out file names, sizes and id's of the files.  Each time it finds  afile it checks to see if a file of the same zize is in the db
already.  If not, it adds it, if there is, it computes the md5 of both files, and if they are the same, commits the new one (yet to happen BTW), else, updates the one
in the db with it's md5, deletes the dupe, and logs it to a text file.  It only does md5's when there is a file size match so it is pretty quick.  It also uses an in
mempry db, but saves it every 10K transactions.  It will log that to the console.  It also logs when it moves to a new sub, and what it is depeating and why.  There is
a small zize limit, I have it set for 1K, you can tweak it.  Most of the tiny files are just slides saying the file went by by..  Any file that starts with ! like the 
ones we make are skipped.  The populate db takes one command line argument:  THe group in the list to start on.  

I am still toying with how to trap errors.  I get occasional network errors and I am not sure if I should just hammer on retrying or wait for a few secs and retry etc.  
So for now it does nothing, it will jsut barf.  However with the db auto loading and saving, and the command line argiment you can just start it back up in the sub it
barfed in and pick back up again.  I am thinking about how to deal with the erors.  Honest.

I am also pondering changing the logging so it writes the log files and cleans them every pass.

Note that is it possible to have dupes in the exception files. I don't think they hurt anything but speed but I like to keep them clean, so once in a while you can
run the exec check program that will purify any dupes.

I am not a python propeller head so there are no doubt better ways of doing things.  I am all ears.  This has been a fun project and if you have ideas or better
ways of coding things, lemme know!

