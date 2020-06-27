#include <iostream>
#include "sleepy_discord/sleepy_discord.h"
#include "cpr/cpr.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

class cppclient : public SleepyDiscord::DiscordClient {
public:
	using SleepyDiscord::DiscordClient::DiscordClient;
	
	virtual void onReady(std::string* jsonMessage) {
		std::cout << "C++: Ready!" << std::endl;
	};

	void onMessage(SleepyDiscord::Message message) {
		if (message.startsWith("c$test"))
			sendMessage(message.channelID, "C++: Test Sucessful");
	};
};

const char* TOKEN = std::getenv("TOKEN");

int main() {
	cppclient client(TOKEN, 2);
	client.run();
};