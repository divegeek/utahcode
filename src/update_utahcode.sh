#!/bin/sh
date
pushd ~/sources/utahcode
git pull origin master
rm -rf code constitution
python /home/shawn/sources/utahcode/src/retrieve_code.py .
git add code constitution
git commit -m "`date`" -a
git tag -f -a -m "Daily tag" `date +"%F"`
git push --tag origin master
popd
