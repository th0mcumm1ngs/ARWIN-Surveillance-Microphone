#!/bin/bash

cd '/Users/tomcummings/Developer/Projects/ARWIN Repositories/ARWIN-Surveillance-Microphone'

python3 main.py &
python3 transmitter.py &

termainate_program() {
    read -s -p "Enter the terimination key: " teriminationKey

    if [ $teriminationKey = "Otis2015" ]
    then
        echo "Terminating..."
        pkill -f main.py && pkill -f transmitter.py
        exit
    else
        echo "Invalid termination key"
        termainate_program
    fi
}

termainate_program