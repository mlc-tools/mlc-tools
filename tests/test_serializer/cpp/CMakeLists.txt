cmake_minimum_required(VERSION 3.1)
project(Serializer)

set(CMAKE_CXX_STANDARD 17)

SET(SIMPLE_TEST_GEN ${CMAKE_SOURCE_DIR}/../simple_test)

include_directories(
        ${CMAKE_SOURCE_DIR}
        ${CMAKE_SOURCE_DIR}/gen
        ${CMAKE_SOURCE_DIR}/src/serialize/
        ${CMAKE_SOURCE_DIR}/third/
)

add_definitions(-Wall -Wno-overloaded-virtual -Wnon-virtual-dtor -Wsign-promo -Wduplicate-enum -Werror)

set(SRC
        main.cpp
        tests.h
        src/serialize/SerializerXml.cpp
        src/serialize/SerializerXml.h
        src/serialize/SerializerBinary.cpp
        src/serialize/SerializerBinary.h
        src/serialize/Pimpl.h
        src/FooObject.h
        src/FooObject.cpp
        third/pugixml/pugiconfig.hpp
        third/pugixml/pugixml.hpp
        third/pugixml/pugixml.cpp
        third/jsoncpp/json_reader.cpp
        third/jsoncpp/json_value.cpp
        third/jsoncpp/json_writer.cpp

        third/binary/dictionary.h
        third/binary/data.h
        third/binary/dictionary.cpp
        third/binary/binary_chunk.h
        third/binary/binary.cpp
        third/binary/binary.h
        third/binary/data.cpp
        third/binary/binary_chunk.cpp

        src/xml.h
        gen/AllTypesChildren.h
        gen/AllTypes.cpp
        gen/AllTypes.h
        gen/AllTypesChildren.cpp
        gen/TestEnum.cpp
        gen/TestEnum.h
        gen/mg_extensions.cpp
        gen/DataStorage.cpp
        gen/DataStorage.h
        gen/data/DataUnit.h
        gen/data/DataUnit.cpp
        gen/data/VisualUnit.h
        gen/data/VisualUnit.cpp
        gen/mg_Factory.h
        gen/BaseEnum.h
)

foreach(FILE ${SRC})
  get_filename_component(PARENT_DIR ${FILE} PATH)

  string(REPLACE "${CMAKE_SOURCE_DIR}" "" GROUP "${PARENT_DIR}")
  string(REPLACE "/" "\\" GROUP "${GROUP}")
  string(REPLACE ".." "" GROUP "${GROUP}")

  set(GROUP "${GROUP}")
  source_group("${GROUP}" FILES "${FILE}")
endforeach()

add_executable(Serializer ${SRC})
