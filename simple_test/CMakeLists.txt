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

file(GLOB_RECURSE SRC ${ROOT}/common/*.cpp)
file(GLOB_RECURSE ML ${ROOT}/external/ml/*.cpp)
file(GLOB_RECURSE PUGIXML ${ROOT}/external/pugixml/*.cpp)
file(GLOB_RECURSE JSONCPP ${ROOT}/external/jsoncpp/*.cpp)
file(GLOB_RECURSE GENERATED ${ROOT}/generated/${TYPE}/*.cpp)

SOURCE_GROUP("generated" FILES ${GENERATED})
SOURCE_GROUP("ml" FILES ${ML})
SOURCE_GROUP("jsoncpp" FILES ${JSONCPP})
SOURCE_GROUP("pugixml" FILES ${PUGIXML})
SOURCE_GROUP("tests" FILES ${SRC})

add_definitions(-w -std=c++14)

include_directories(
	${ROOT}/generated/${TYPE}/
	${ROOT}/common/
	${ROOT}/external/
	${ROOT}/external/ml
)

add_executable(${PROJECT_NAME} ${SRC} ${ML} ${PUGIXML} ${JSONCPP} ${GENERATED})
target_link_libraries(${PROJECT_NAME})
