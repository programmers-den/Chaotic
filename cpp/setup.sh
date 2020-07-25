#!/bin/bash
sudo apt install libcurl-dev openssl-dev cmake
cd lib
if [[ -f sleepy-discord ]]
then
    rm -rf sleepy-discord
    git clone https://github.com/yourWaifu/sleepy-discord.git
fi

cd ..
cmake out/build/
