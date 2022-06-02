#!/bin/bash

python faustgen.py $1 $2 $3 $4

wait 

faust2jaqt -osc main.dsp

wait

python video2.py &

./main
