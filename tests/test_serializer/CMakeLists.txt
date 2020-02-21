cmake_minimum_required(VERSION 3.1)
project(Serializer)

set(CMAKE_CXX_STANDARD 17)

add_executable(Serializer
        main.cpp
        src/serialize/SerializerXml.cpp
        src/serialize/SerializerXml.h
        src/serialize/SerializerJson.cpp
        src/serialize/SerializerJson.h
        src/serialize/Pimpl.hpp
        src/FooObject.h
        src/FooObject.cpp
        src/AllTypesChildren.h
        src/AllTypes.cpp
        src/AllTypes.h
        src/AllTypesChildren.cpp
        src/TestEnum.cpp
        src/TestEnum.h
        src/mg_extensions.cpp
        third/pugixml/pugiconfig.hpp
        third/pugixml/pugixml.hpp
        third/pugixml/pugixml.cpp
        third/jsoncpp/json_reader.cpp
        third/jsoncpp/json_value.cpp
        third/jsoncpp/json_writer.cpp
        )