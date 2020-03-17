cmake_minimum_required(VERSION 3.6.2)

option(BUILD_XML "Build the xml test" OFF)
option(BUILD_JSON "Build the json test" OFF)

SET(ROOT ${CMAKE_SOURCE_DIR})

if(BUILD_XML)
    set(TYPE xml)
elseif(BUILD_JSON)
    set(TYPE json)
endif(BUILD_XML)

project(test_mlc_${TYPE})

file(GLOB_RECURSE SRC
                        ${ROOT}/generated_cpp/${TYPE}/*.cpp
                        ${ROOT}/generated_cpp/${TYPE}/*.h
                        ${ROOT}/../simple_test/external/pugixml/*.cpp
                        ${ROOT}/../simple_test/external/pugixml/*.h
                        ${ROOT}/../simple_test/external/jsoncpp/*.cpp
                        ${ROOT}/../simple_test/external/jsoncpp/*.h
                        ${ROOT}/lib/cpp/*.cpp
                        ${ROOT}/lib/cpp/*.h
)

if(WIN32)
    add_definitions(-W1 -std=c++17)
else()
    add_definitions(-Wall -std=c++17)
endif()

include_directories(
    ${ROOT}/generated_cpp/${TYPE}/
	${ROOT}/generated_cpp/${TYPE}/tests/
    ${ROOT}/../simple_test/external/
	${ROOT}/lib/cpp/
    /usr/local/include
)
link_directories(
    /usr/local/lib/
)

add_executable(${PROJECT_NAME}
	${SRC}
    ${ROOT}/main.cpp
)

target_link_libraries(${PROJECT_NAME})
