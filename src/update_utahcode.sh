#!/bin/sh
LOGFILE=~/log/utahcode.log
touch $LOGFILE
date >> $LOGFILE
cd ~/sources/utahcode
git pull -q origin master
rm -rf code constitution
python /home/shawn/sources/utahcode/src/retrieve_code.py . >> $LOGFILE
if [ $? -ne 0 ]; then
  echo "Aborting git update due to retrieval error"
fi

git add -A code constitution >> $LOGFILE
DIFFLOG=`git status --porcelain`
if [ ! -z "$DIFFLOG" ]; then
    echo "$DIFFLOG" >> $LOGFILE
    git commit -m "`date`"
    git tag -f -a -m "Daily tag" `date +"%F"`
    git push --tag origin master
fi
