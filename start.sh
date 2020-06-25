#!/bin/bash
cd js/
npm install
cd ../py
python3 -m pip install -r requirements.txt
cd ../

while :
do
  ./stop.sh
  if [ -f .env ]
  then
    export $(cat .env | sed 's/#.*//g' | xargs)
  fi

  git pull
  cd js
  bash -c "exec -a chaotic-js ./node_modules/coffeescript/bin/coffee index.coffee" &
  cd ../py
  bash -c "exec -a chaotic-py python3 main.py"
  cd ../
done
