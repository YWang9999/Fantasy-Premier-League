#! /bin/bash
# VM setup
sudo apt-get update
sudo apt-get install git
cd /srv
sudo git clone https://github.com/Jonwalk30/Fantasy-Premier-League.git
# git clone https://github.com/Jonwalk30/Fantasy-Premier-League.git
cd Fantasy-Premier-League/
# git checkout gcp-runner
sudo git checkout gcp-runner
sudo apt install python3-pip
pip3 install -r requirements.txt
pip3 install pyarrow==2.0.0
pip3 install pandas-gbq
chmod 777 andreasarmstrong94

gcloud secrets versions access 1 --secret="service-account-key-compute-engine-user2" > model/key.json
export PROJECT_ID=lbghack2021team14
export PATH_TO_JSON_KEY=model/key.json





# Run modelling
#! /bin/bash
cd /~/Fantasy-Premier-League/
git pull
pip3 install -r requirements.txt
python3 global_scraper.py
python3 model/data_ingester.py
python3 model/feature_engineer.py
python3 model/modeller.py









# check startup script
cat /var/log/daemon.log
