cmake_minimum_required(VERSION 3.6.2)

SET(ROOT ${CMAKE_SOURCE_DIR})
set(THIRD_PARTY_DIR ${ROOT}/../../third_party)

project(step_2)

file(GLOB_RECURSE SRC
						${THIRD_PARTY_DIR}/pugixml/*.cpp
						${THIRD_PARTY_DIR}/jsoncpp/*.cpp
						${ROOT}/generated_cpp/*.cpp
						)

if(WIN32)
	add_definitions(-W1 -std=c++14)
else()
	add_definitions(-Wall -std=c++14)
endif()

include_directories(
	${ROOT}/generated_cpp/
	${THIRD_PARTY_DIR}/
	${EXTERNAL}/ml
)

add_executable(${PROJECT_NAME}
	${SRC}
	${ROOT}/step_2.cpp
)

target_link_libraries(${PROJECT_NAME})

install (TARGETS ${PROJECT_NAME} DESTINATION ${ROOT})