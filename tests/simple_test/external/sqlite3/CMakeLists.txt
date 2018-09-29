project(sqlite3)
cmake_minimum_required(VERSION 3.8)

set(ROOT ${CMAKE_CURRENT_SOURCE_DIR})
add_definitions(-w -O3)

#file(GLOB SRC "*.c")
#add_library(sqlite3 ${SRC})
add_library(sqlite3 "sqlite3.c")
