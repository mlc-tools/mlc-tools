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
						${ROOT}/generated_cpp/${TYPE}/*.cpp *.h
						)

foreach(FILE ${SRC})
  get_filename_component(PARENT_DIR ${FILE} PATH)

  string(REPLACE "${ROOT}" "" GROUP "${PARENT_DIR}")
  string(REPLACE "/" "\\" GROUP "${GROUP}")

  set(GROUP "${GROUP}")
  source_group("${GROUP}" FILES "${FILE}")
endforeach()


if(WIN32)
	add_definitions(-W1 -std=c++14)
else()
	add_definitions(-Wall -std=c++14)
endif()

add_definitions(-DSERVER=1)
add_definitions(-DCLIENT=2)
add_definitions(-DBUILD_SIDE=${BUILD_SIDE})

add_definitions(-DXML=1)
add_definitions(-DJSON=2)
if(BUILD_XML)
    add_definitions(-DSERIALIZE_FORMAT=XML)
elseif(BUILD_JSON)
    add_definitions(-DSERIALIZE_FORMAT=JSON)
endif(BUILD_XML)


include_directories(
	${ROOT}/generated_cpp/${TYPE}/
	${ROOT}/common/
	${ROOT}/external/
	${ROOT}/external/ml
)

add_executable(${PROJECT_NAME}
	${SRC}
)

target_link_libraries(${PROJECT_NAME})
