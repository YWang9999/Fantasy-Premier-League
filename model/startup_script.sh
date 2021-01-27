#! /bin/bash
# VM setup
sudo apt-get update
sudo apt-get install git
git clone https://github.com/Jonwalk30/Fantasy-Premier-League.git
git checkout gcp-runner
cd Fantasy-Premier-League/
sudo apt install python3-pip
pip3 install -r requirements.txt


export PROJECT_ID=lbghack2021team14
export PATH_TO_JSON_KEY=model/lbghack2021team14-7efa23028478.json

# Run modelling
python3 global_scraper.py
python3 model/data_ingester.py
python3 model/feature_engineer.py
python3 model/modeller.py



