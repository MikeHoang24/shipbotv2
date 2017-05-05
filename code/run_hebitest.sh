#!/bin/bash
echo "Testing hebis."

python hebi_reset.py

./../../shipbot-hebi/armcontrol/armcontrol > hebiout.txt &

python test_hebi.py


