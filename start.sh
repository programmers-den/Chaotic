#!/usr/bin/env sh
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

alias coffee=./js/node_modules/coffeescript/bin/coffee
