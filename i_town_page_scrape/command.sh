#!/bin/bash

./clean.sh
source ~/venv/py3.10.12/bin/activate
mkdir -p output
python3 i_town_page_scrape.py ${1} ${2}
