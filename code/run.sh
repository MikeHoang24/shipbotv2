#!/bin/bash

echo "Running the demo."

./../../shipbot-hebi/armcontrol/armcontrol > hebiout.txt &

python main.py
