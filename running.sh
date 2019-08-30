#!/bin/bash

num=$(ps aux | grep cloud.py | grep $1 | sed /grep/d | wc -l)
#echo $num
if [ "$num" -gt "0" ]; then
  exit 0
  #echo "running"
else
  echo "not"
  exit 1
fi
