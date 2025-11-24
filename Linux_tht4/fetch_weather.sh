#!/bin/bash
echo "Cron käynnistyi $(date)" >> cron.log
cd /home/ubuntu/cron_Tht4
source venv/bin/activate
python fetch_weather.py
