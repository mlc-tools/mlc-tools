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

add_executable(Serializer
        main.cpp
        src/serialize/SerializerXml.cpp
        src/serialize/SerializerXml.h
        src/serialize/SerializerJson.cpp
        src/serialize/SerializerJson.h
        src/serialize/Pimpl.h
        src/FooObject.h
        src/FooObject.cpp
        third/pugixml/pugiconfig.hpp
        third/pugixml/pugixml.hpp
        third/pugixml/pugixml.cpp
        third/jsoncpp/json_reader.cpp
        third/jsoncpp/json_value.cpp
        third/jsoncpp/json_writer.cpp
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
        gen/data/DataUnit.cpp
        gen/data/VisualUnit.cpp
        gen/mg_Factory.h
        gen/BaseEnum.h
        )
