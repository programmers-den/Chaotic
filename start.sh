#!/usr/bin/env bash
while :
do
  pkill -f chaotic-js
  if [ -f .env ]
  then
    export $(cat .env | sed 's/#.*//g' | xargs)
  fi

  git pull
  cd js
  bash -c "exec -a chaotic-js ./node_modules/coffeescript/bin/coffee index.coffee"
  sleep 3600
done
