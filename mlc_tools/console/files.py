
CMAKE = '''cmake_minimum_required(VERSION 3.13)
SET(ROOT ${CMAKE_SOURCE_DIR})
SET(GEN_DIR "@{gen_dir}")

option(WITH_DATA "Build with data" OFF)

project(@{project_name})

file(GLOB_RECURSE SRC ${GEN_DIR}/*.cpp ${ROOT}/external/*.cpp)

include_directories(${GEN_DIR} ${ROOT}/external)

if(WIN32)
    add_definitions(-W1 -std=c++14)
else()
    add_definitions(-Wall -std=c++14)
endif()

if(WITH_DATA)
    add_definitions(-DWITH_DATA=1)
endif(WITH_DATA)

add_executable(${PROJECT_NAME} ${SRC} ${ROOT}/__main.cpp)
target_link_libraries(${PROJECT_NAME})'''

MAIN_CPP = '''#include "Main.h"
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

PROJECT_YAML = '''
project:
  {name}
'''

HELLO_WORLD_MLC = '''class Main
{
    function void main():static
    {
        print("Hello World!!!");
    }
}
'''