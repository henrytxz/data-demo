#!/usr/bin/env bash

available_arguments="
\tupdate: Pull Docker image from the Artifact Registry
\tdbt <run, test, --select, etc>: Runs dbt with the provided dbt sub-command\n
To learn more about dbt, do \"./rundbt.sh dbt\" in your Terminal."

help="Argument '$1' is invalid.\n\n$available_arguments"

target_image=us-docker.pkg.dev/henrytxz/data-demo/data-demo-dbt:latest

if [ $# -eq 0 ]; then
  printf "The ./rundbt.sh script requires a minimum of 1 argument.\n\nAvailale arguments: $available_arguments\n"
elif [ $# -eq 1 ] && [ "$1" == "update" ]; then
  docker pull $target_image
elif [ "$1" == "dbt" ] && [ $# -gt 1 ]; then
  # User wants to do something with dbt and provided argument or sub-command, so let's run it.
  docker run --rm \
  -t \
  -e DBT_DEV_PROJECT="$DBT_DEV_PROJECT" \
  -e PATH_GCP_KEYFILE=/root/.dbt/dbt-user.json \
  -p 8080:8080 \
  -v "$HOME"/.dbt/:/root/.dbt \
  -v "$DATA_DEMO_HOME"/dbt:/dbt \
  $target_image \
  "$@"
elif [ "$1" == "dbt" ] && [ $# -eq 1 ]; then
  # User wants to do something with dbt but didn't provide an argument nor sub-command.
  # Let's show the dbt man page.
  docker run --rm $target_image dbt
else
  # User did something wrong, display help message.
  printf "%s" "$help"
fi
