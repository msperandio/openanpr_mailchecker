# openanpr_mailchecker
A lightweight license plate recognition system based on openalpr checking alerts mail.

# SETUP
1 - Install python3 with sqlite3 and imaplib

2 - Install and configure opanlpr following the guides at https://github.com/openalpr/openalpr

2 - Run the script: "run.sh"

3 - Run the script: "start_env.sh"

4 - Enter Grafana at port 3000 and install the plugin https://grafana.com/grafana/plugins/frser-sqlite-datasource/

5 - Setup run.sh as a cronjob at the desired rate

# TODO
- alternatives download from ftp or http or local
- autmoatic script to deploy the whole system with cronjob at 12h
- deploy sqlite-web and grafana with nginx (and zm)