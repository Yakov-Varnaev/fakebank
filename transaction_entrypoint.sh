#!/bin/bash
# Not ideal but depends_on doesn't work as expected
sleep 5

python app/main.py --name=transactions
