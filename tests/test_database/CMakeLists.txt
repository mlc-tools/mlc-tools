cmake_minimum_required(VERSION 3.6.2)

option(BUILD_XML "Build the xml test" OFF)
option(BUILD_JSON "Build the json test" OFF)

SET(ROOT ${CMAKE_SOURCE_DIR})
set(THIRD_PARTY_DIR ${ROOT}/../../third_party)

if(BUILD_XML)
    set(TYPE xml)
elseif(BUILD_JSON)
    set(TYPE json)
endif(BUILD_XML)

project(test_mlc_${TYPE})

file(GLOB_RECURSE SRC
                        ${ROOT}/generated_cpp/${TYPE}/*.cpp
                        ${ROOT}/generated_cpp/${TYPE}/*.h
                        ${THIRD_PARTY_DIR}/pugixml/*.cpp
                        ${THIRD_PARTY_DIR}/pugixml/*.h
                        ${THIRD_PARTY_DIR}/jsoncpp/*.cpp
                        ${THIRD_PARTY_DIR}/jsoncpp/*.h
                        ${ROOT}/lib/cpp/*.cpp
                        ${ROOT}/lib/cpp/*.h
)

if(WIN32)
    add_definitions(-W1 -std=c++14)
else()
    add_definitions(-Wall -std=c++14)
endif()

include_directories(
    ${ROOT}/generated_cpp/${TYPE}/
	${ROOT}/generated_cpp/${TYPE}/tests/
    ${THIRD_PARTY_DIR}/
	${ROOT}/lib/cpp/
    /usr/local/include
)
link_directories(
    /usr/local/lib/
    ${THIRD_PARTY_DIR}/sqlite3/bin/osx
)

add_executable(${PROJECT_NAME}
	${SRC}
    ${ROOT}/main.cpp
)

target_link_libraries(${PROJECT_NAME} pqxx pq sqlite3)
