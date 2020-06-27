cmake_minimum_required (VERSION 3.6)
project(cpp)

add_executable(cpp main.cpp)

add_subdirectory(lib/sleepy-discord)
target_link_libraries(cpp sleepy-discord)
