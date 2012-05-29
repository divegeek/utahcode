#!/bin/sh -e
LOGFILE=~/log/utahcode.log
touch $LOGFILE
date >> $LOGFILE
cd ~/sources/utahcode
git pull -q origin master
rm -rf code constitution
python /home/shawn/sources/utahcode/src/retrieve_code.py . >> $LOGFILE
git add code constitution >> $LOGFILE
git status >> $LOGFILE
if [ $? -eq 0 ]; then
    git commit -m "`date`" -a
    git tag -f -a -m "Daily tag" `date +"%F"`
    git push --tag origin master
fi