#include <iostream>
#include "sleepy_discord/sleepy_discord.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>

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
typedef websocketpp::client<websocketpp::config::asio_client> client;

int main() {
	cppclient bot(TOKEN, 2);
	bot.run();

	client c;

	std::string uri = "ws://127.0.0.1:9010";
	c.init_asio();
	websocketpp::lib::error_code ec;
	client::connection_ptr con = c.get_connection(uri, ec);
	if (ec) {
		std::cout << "Failed to connect to the websocket" << std::endl;
	}

	c.connect(con);
	c.run();
};