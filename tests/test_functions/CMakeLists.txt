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
                        ${ROOT}/generated_cpp/${TYPE}/*.cpp *.h
                        ${ROOT}/../simple_test/external/pugixml/*.cpp *.h
                        ${ROOT}/../simple_test/external/jsoncpp/*.cpp *.h
                        ${ROOT}/main.cpp

)

if(WIN32)
	add_definitions(-w -std=c++14)
else()
	add_definitions(-Wall -std=c++14)
endif()

include_directories(
	${ROOT}/generated_cpp/${TYPE}/
	${ROOT}/../simple_test/external/
)

add_executable(${PROJECT_NAME}
	${SRC}
)

target_link_libraries(${PROJECT_NAME})
