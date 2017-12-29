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
						${ROOT}/common/*.cpp *.h
						${ROOT}/external/ml/*.cpp *.h
						${ROOT}/external/pugixml/*.cpp *.h
						${ROOT}/external/jsoncpp/*.cpp *.h
						${ROOT}/generated/${TYPE}/*.cpp *.h
						)

foreach(FILE ${SRC}) 
  get_filename_component(PARENT_DIR ${FILE} PATH)

  string(REPLACE "${ROOT}" "" GROUP "${PARENT_DIR}")
  string(REPLACE "/" "\\" GROUP "${GROUP}")

  set(GROUP "${GROUP}")
  source_group("${GROUP}" FILES "${FILE}")
endforeach()


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
	${SRC}
)

target_link_libraries(${PROJECT_NAME})
