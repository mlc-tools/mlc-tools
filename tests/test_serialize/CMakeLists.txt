cmake_minimum_required(VERSION 3.6.2)

SET(ROOT ${CMAKE_SOURCE_DIR})
SET(EXTERNAL ${CMAKE_SOURCE_DIR}/../simple_test/external)

project(step_2)

file(GLOB_RECURSE SRC 
						${EXTERNAL}/pugixml/*.cpp
						${EXTERNAL}/jsoncpp/*.cpp
						${ROOT}/generated_cpp/*.cpp
						)

add_definitions(-w -std=c++14)

include_directories(
	${ROOT}/generated_cpp/
	${EXTERNAL}/
	${EXTERNAL}/ml
)

add_executable(${PROJECT_NAME} 
	${SRC}
	${ROOT}/step_2.cpp
)

target_link_libraries(${PROJECT_NAME})

install (TARGETS ${PROJECT_NAME} DESTINATION ${ROOT})