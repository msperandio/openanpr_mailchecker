#!/bin/bash

port="8080"
db=$(realpath ./data/plates.db)
db_dir=$(dirname $db)
db_file=$(basename $db)
echo "Starting sqlite-web on: http://0.0.0.0:$port"
docker run -d --rm -p "$port:8080" -v $db_dir:/data -e SQLITE_DATABASE="$db_file" --name=sqlite-web coleifer/sqlite-web

ID=$(id -u)
portg="3000"
echo "Starting grafana on port: $portg"
docker run -d --user $ID --volume "$PWD/data:/var/lib/grafana" -e "GF_LOG_MODE=console file" --name=grafana -p "$portg:3000" grafana/grafana-enterprise
