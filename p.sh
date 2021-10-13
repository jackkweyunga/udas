#!/bin/sh

if [[ $1 == "" ]]; then 

    echo "-----------------------------------"
    echo "This is a small tool to help you commit faster."
    echo "[usage] - sh p.sh <message>"

elif [[ $1 != "" ]]; then 

    git add . && git commit -m "$1" && git push

fi