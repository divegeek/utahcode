#!/bin/sh
date
cd ~/sources/utahcode
git pull -q origin master
rm -rf code constitution
python /home/shawn/sources/utahcode/src/retrieve_code.py .
git add code constitution
git status
if [ $? -eq 0 ]; then
    git commit -m "`date`" -a
    git tag -f -a -m "Daily tag" `date +"%F"`
    git push --tag origin master
fi
