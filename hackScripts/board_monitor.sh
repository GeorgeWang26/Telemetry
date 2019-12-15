#!/bin/sh

while [ 1 ]
do
    echo
    boardStatus=$(ps -e | grep 'boardControl.py' | grep -v 'grep')

    if [ ! -z "$boardStatus" ]; then
        echo "boardControl already running"
# > /home/pi/hackScripts/test.log
        #echo "already"
    else
        echo "boardControl does not exist"
# > /home/pi/hackScripts/test.log
        /home/pi/hackScripts/boardControl.py &
# > /home/pi/hackScripts/testpy.log & 
#        echo "after start boardControl.py" >> /home/pi/hackScripts/test.log
    fi

    sleep 1
done
