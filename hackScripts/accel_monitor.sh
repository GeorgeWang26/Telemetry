#!/bin/sh

server=10.8.0.2
port=8000

while [ 1 ]
do
    echo 
    accelerometerStatus=$(ps -e | grep 'accel.py' | grep -v 'grep')

    if [ ! -z "$accelerometerStatus" ]; then
        echo "accelerometer already running"

    else

        echo "accelerometer does not exist"
        serverConnection=$(ping -c 1 $server | grep ' 0%' | grep -v 'grep')

        if [ ! -z "$serverConnection" ]; then

            echo "server connection succeeded"
            portConnection=$(netcat -v -z $server $port 2>&1 | grep 'succeeded' | grep -v 'grep')

            if [ ! -z "$portConnection" ]; then
                echo "port connection succeeded"
                echo "start accel.py"
                /home/pi/hackScripts/accel.py &

            else
                echo "port connection failed"
            
            fi

        else
            echo "server connection failed"

        fi

    fi

	sleep 1
done
