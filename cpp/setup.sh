#!/bin/bash
bash -c "sudo apt install libcurl-dev openssl-dev cmake"
bash -c "cd lib"
if [[ -f sleepy-discord ]]
then
    bash -c "rm -rf sleepy-discord"
    bash -c "git clone https://github.com/yourWaifu/sleepy-discord.git"
fi

bash -c "cd .."
bash -c "cmake"
