cmake_minimum_required(VERSION 3.6.2)

option(BUILD_XML "Build the xml test" OFF)
option(BUILD_JSON "Build the json test" OFF)

if(BUILD_XML)
    set(TYPE xml)
elseif(BUILD_JSON)
    set(TYPE json)
endif(BUILD_XML)

project(test_mlc_${TYPE})

SET(ROOT ${CMAKE_SOURCE_DIR})

file(GLOB_RECURSE GENERATED ${ROOT}/generated/${TYPE}/*.cpp)
file(GLOB_RECURSE EXTERNAL ${ROOT}/external/*.cpp)
file(GLOB_RECURSE SRC ${ROOT}/common/*.cpp)

add_definitions(-Wall -O2 -std=c++14)

include_directories(
	${ROOT}/generated/${TYPE}/
	${ROOT}/common/
	${ROOT}/external/
	${ROOT}/external/ml
)
add_executable(${PROJECT_NAME} ${SRC} ${EXTERNAL} ${GENERATED})
target_link_libraries(${PROJECT_NAME})
