#!/usr/bin/env bash
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

cd js
./node_modules/coffeescript/bin/coffee index.coffee
