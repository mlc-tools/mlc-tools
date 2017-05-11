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

file(GLOB_RECURSE COMMON_SRC ${ROOT}/common/*.cpp)
file(GLOB_RECURSE ML_SRC ${ROOT}/external/ml/*.cpp)
file(GLOB_RECURSE PUGIXML_SRC ${ROOT}/external/pugixml/*.cpp)
file(GLOB_RECURSE JSONCPP_SRC ${ROOT}/external/jsoncpp/*.cpp)
file(GLOB_RECURSE GENERATED_SRC ${ROOT}/generated/${TYPE}/*.cpp)

file(GLOB_RECURSE COMMON_HEADERS ${ROOT}/common/*.h)
file(GLOB_RECURSE ML_HEADERS ${ROOT}/external/ml/*.h)
file(GLOB_RECURSE PUGIXML_HEADERS ${ROOT}/external/pugixml/*.h)
file(GLOB_RECURSE JSONCPP_HEADERS ${ROOT}/external/jsoncpp/*.h)
file(GLOB_RECURSE GENERATED_HEADERS ${ROOT}/generated/${TYPE}/*.h)

SOURCE_GROUP("generated" FILES ${GENERATED_SRC} ${GENERATED_HEADERS})
SOURCE_GROUP("ml" FILES ${ML_SRC} ${ML_HEADERS})
SOURCE_GROUP("jsoncpp" FILES ${JSONCPP_SRC} ${JSONCPP_HEADERS})
SOURCE_GROUP("pugixml" FILES ${PUGIXML_SRC} ${PUGIXML_HEADERS})
SOURCE_GROUP("tests" FILES ${COMMON_SRC} ${COMMON_HEADERS})

add_definitions(-w -std=c++14)
add_definitions(-DSERVER=1)
add_definitions(-DCLIENT=2)
add_definitions(-DBUILD_SIDE=${BUILD_SIDE})

include_directories(
	${ROOT}/generated/${TYPE}/
	${ROOT}/common/
	${ROOT}/external/
	${ROOT}/external/ml
)

add_executable(${PROJECT_NAME} 
	${COMMON_SRC} ${COMMON_HEADERS} 
	${ML_SRC} ${ML_HEADERS} 
	${PUGIXML_SRC} ${PUGIXML_HEADERS} 
	${JSONCPP_SRC} ${JSONCPP_HEADERS} 
	${GENERATED_SRC} ${GENERATED_HEADERS}
)

target_link_libraries(${PROJECT_NAME})
