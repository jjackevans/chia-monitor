# chia-monitor
A simple Python script to pull information from the local Chia node and make it available over an API.

## Prerequisites
1. Register an account [here](http://www.mychiamonitor.com)
2. Create a farm, and copy the created key
3. Make sure you have python3.9 and python3.9-venv installed.

## Installation
```
git clone https://github.com/jjackevans/chia-monitor
cd chia-monitor
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Edit the config.ini file such that you have an entry:
``` 
key = key_generated_from_website 
```

## Run
``` 
python -m monitor.updater
```
