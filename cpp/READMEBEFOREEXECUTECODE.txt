Please create folder named "lib"

For window users: (Install OpenSSL before build, else err)
	mkdir lib
	cd cpp/lib
	git clone https://github.com/yourWaifu/sleepy-discord.git
	cd ../

NOTE: Windows Users MUST have cmake-gui or Visual Studio
	User Using CMAKE-GUI:
		Select Source As cpp/
		Create folder cpp/build and delete cpp/out
		Browse Build As cpp/build

	User Using Visual Studio:
		Open CMakeLists.txt and generate the confg
		Goto Build -> Build All

For Linux/MacOS users:
	mkdir lib
	cd cpp/lib
	sudo apt install libssl-dev libcurl-dev
	git clone https://github.com/yourWaifu/sleepy-discord.git
	cd ../
	cmake
OR:
	sudo chmod +x setup.sh
	./setup.sh

Installing OpenSSL On Windows:
	https://slproweb.com/download/Win64OpenSSL-1_1_1g.exe

NOTE: Before building the lib, remember to install OpenSSL first!

Visit https://yourwaifu.dev/sleepy-discord/setup.html for requirements of
the lib.
