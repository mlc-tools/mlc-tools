cmake_minimum_required(VERSION 3.6.2)

project(mlc)

SET(ROOT ${CMAKE_SOURCE_DIR}/..)

include_directories(
	${ROOT}/out/
	${ROOT}/external/
	${ROOT}/external/ml
)

file(GLOB_RECURSE SRC ${ROOT}/out/*.cpp)
file(GLOB_RECURSE JSON ${ROOT}/external/pugixml/*.cpp)
file(GLOB_RECURSE XML ${ROOT}/external/jsoncpp/*.cpp)
file(GLOB_RECURSE ML ${ROOT}/external/ml/*.cpp)

add_definitions(-Wall -O2 -std=c++14)
add_executable(${PROJECT_NAME} ${SRC} ${XML} ${JSON} ${ML})
target_link_libraries(${PROJECT_NAME})
install (TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)