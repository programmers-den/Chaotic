#!/usr/bin/env bash
while :
do
  pkill -f chaotic-js
  pkill -f chaotic-py
  if [ -f .env ]
  then
    export $(cat .env | sed 's/#.*//g' | xargs)
  fi

  git pull
  cd js
  bash -c "exec -a chaotic-js ./node_modules/coffeescript/bin/coffee index.coffee"
  cd ../py
  bash -c "exec -a chaotic-py python3 main.py"
  cd ../
  sleep 3600
done
