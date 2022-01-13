#!/bin/bash

port="8080"
db=$(realpath ./data/plates.db)
db_dir=$(dirname $db)
db_file=$(basename $db)
echo "Starting on: http://0.0.0.0:$port"
docker run -d --rm -p "$port:8080" -v $db_dir:/data -e SQLITE_DATABASE="$db_file" coleifer/sqlite-web