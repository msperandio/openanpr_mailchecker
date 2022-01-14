# openanpr_mailchecker
A lightweight license plate recognition system based on openalpr checking alerts mail.

![dashboard_1](https://user-images.githubusercontent.com/5609877/149509811-e7f813a1-1b00-4f6a-a2bf-1bae4f45cc9f.png)

# SETUP
1 - Install python3 with sqlite3 and imaplib

2 - Install and configure opanlpr following the guides at https://github.com/openalpr/openalpr

2 - Run the script: "run.sh"

3 - Run the script: "start_env.sh"

4 - Enter Grafana at port 3000 and install the plugin https://grafana.com/grafana/plugins/frser-sqlite-datasource/

5 - Setup run.sh as a cronjob at the desired rate

# TODO
- send mail alerts with new or unknown plates
- mail folder and addresses configurable from file or DB
- alternatives download from ftp or http
- autmoatic script to deploy the whole system with cronjob at 12h
- deploy sqlite-web and grafana with nginx (and zm)
