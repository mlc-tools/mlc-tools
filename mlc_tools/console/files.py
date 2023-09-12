
CMAKE = '''cmake_minimum_required(VERSION 3.13)
SET(ROOT ${CMAKE_SOURCE_DIR})
SET(GEN_DIR "@{gen_dir}")

option(WITH_DATA "Build with data" OFF)

project(@{project_name})

file(GLOB_RECURSE SRC ${GEN_DIR}/*.cpp ${ROOT}/external/*.cpp)

include_directories(${GEN_DIR} ${ROOT}/external)

if(WIN32)
    add_definitions(-W1 -std=c++17)
else()
    add_definitions(-Wall -std=c++17)
endif()

if(WITH_DATA)
    add_definitions(-DWITH_DATA=1)
endif(WITH_DATA)

'''

CMAKE_APP = '''add_executable(${PROJECT_NAME} ${SRC} ${ROOT}/main.cpp)
target_link_libraries(${PROJECT_NAME})'''

CMAKE_LIB = '''add_library(${PROJECT_NAME} STATIC ${SRC} ${ROOT}/mg.cpp)
target_link_libraries(${PROJECT_NAME})'''

MAIN_CPP_EXE = '''#include "Main.h"
#include "Registrar.h"

#ifdef WITH_DATA
#   include "DataStorage.h"
#   include <string>
#   include <fstream>
#   include <iostream>
#endif

int main(int argc, char ** args)
{
    mg::register_classes();

#ifdef WITH_DATA
    std::string path = "data/data.@{format}";
    std::fstream stream(path, std::fstream::in);
    if(!stream.is_open())
    {
        std::cout << "Cannot open file: " << path << std::endl;
        exit(-1);
    }
    std::string data((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
    mg::DataStorage::shared().initialize_@{format}(data);
#endif

    mg::Main::main();
    return 0;
}
'''
MAIN_CPP_LIB = '''#include "Registrar.h"

#ifdef WITH_DATA
#   include "DataStorage.h"
#   include <string>
#   include <fstream>
#   include <iostream>
#endif

void initialize(int argc, char ** args)
{
    mg::register_classes();

#ifdef WITH_DATA
    std::string path = "data/data.@{format}";
    std::fstream stream(path, std::fstream::in);
    if(!stream.is_open())
    {
        std::cout << "Cannot open file: " << path << std::endl;
        exit(-1);
    }
    std::string data((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
    mg::DataStorage::shared().initialize_@{format}(data);
#endif
}
'''
MAIN_HPP_LIB = '''#ifndef __mg_initialize_h__
#define __mg_initialize_h__

void initialize(int argc, char ** args);

#endif
'''

PROJECT_YAML = '''
project:
  {name}
  
binary_type:
  {binary_type}
'''

HELLO_WORLD_MLC = '''class Main
{
    function void main():static
    {
        print("Hello World!!!");
    }
}
'''