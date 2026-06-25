#!/bin/bash

echo "Starting independent Elastic Constant calculations..."

echo "1. Running C11..."
python tetragonal_c11.py > c11.log 2>&1

echo "2. Running C33..."
python tetragonal_c33.py > c33.log 2>&1

echo "3. Running C44..."
python tetragonal_c44.py > c44.log 2>&1

echo "4. Running C66..."
python tetragonal_c66.py > c66.log 2>&1

echo "Initial calculations done! Please check the outputs, update C11 and C33 values in c12.py and c13.py, and then run them manually."
