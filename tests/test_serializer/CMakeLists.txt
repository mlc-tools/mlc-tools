cmake_minimum_required(VERSION 3.15)
project(Serializer)

set(CMAKE_CXX_STANDARD 17)

add_executable(Serializer
        main.cpp
        src/Serializer.cpp
        src/Serializer.h
        src/Pimpl.hpp
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
        )