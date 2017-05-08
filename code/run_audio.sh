#!/bin/bash
echo "Resetting hebi file."

python hebi_reset.py

echo "Initializing hebi control."

./../../shipbot-hebi/armcontrol/armcontrol > hebiout.txt &

python audio_loop.py > audioout.txt &

echo "Audio loop initiated."

echo "Running main function."

python main.py
