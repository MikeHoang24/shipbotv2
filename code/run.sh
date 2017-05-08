#!/bin/bash
echo "Resetting hebi file."

python hebi_reset.py

echo "Initializing hebi control."

./../../shipbot-hebi/armcontrol/armcontrol > hebiout.txt &

echo "Running main function."

python main.py
