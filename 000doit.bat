::  (c) 2021 mfk 
::  This script loops through each of the lines in the subreddit.txt file.
::
:: The disadvantage is that it runs the python file multiple times in a sequence
::
:: The advantage is if there is a file that causes the python sctipt to hang or abort it
:: it only causes that line to fail.
::
:: This is probably the best option for now..
::
@echo off
::
:: Update pip and the bdfr program
python -m pip install pip--upgrade
python -m pip install bdfr --upgrade
::
:: Create the exe file in case the group is newly addeed
for /F %%x in (\\192.168.1.124\reddit\subreddit.lst) do type nul >> \\192.168.1.124\reddit\bdfr\excs\%%x.exc
::
:: Do the fetching
for /f %%g in (\\192.168.1.124\reddit\subreddit.lst) do python -m bdfr download \\192.168.1.124\reddit --subreddit %%g --no-dupes --exclude-id-file \\192.168.1.124\reddit\bdfr\excs\%%g.exc --log \\192.168.1.124\reddit\bdfr\logs\%%g.log --skip txt --skip gif 
::
:: Do some clean up of the old logs
del \\192.168.1.124\reddit\bdfr\logs\*.log.1 \\192.168.1.124\reddit\bdfr\logs\*.log.2 \\192.168.1.124\reddit\bdfr\logs\*.log.3 \\192.168.1.124\reddit\bdfr\logs\*.log.4 \\192.168.1.124\reddit\bdfr\logs\*.log.5
::
:: Create the picture title sldes every day to they are at the top of the sort list by date
for /f %%g in (\\192.168.1.124\reddit\subreddit.lst) do (
	ffmpeg -y -loglevel panic -f lavfi -i color=blue:size=1280x720 -frames:v 1 \\192.168.1.124\reddit\%%g\!%%g.jpg > nul
	ffmpeg -loglevel panic -i \\192.168.1.124\reddit\%%g\!%%g.jpg -vf drawtext="fontsize=100:fontcolor=yellow:text=%%g:x=(w-text_w)/2:y=(h-text_h)/2" -y \\192.168.1.124\reddit\%%g\!%%g.jpg > nul
)