//
// Created by Vladimir Tolmachev on 2020-02-21.
//

#ifndef __mg_SERIALIZERCOMMON_H__
#define __mg_SERIALIZERCOMMON_H__

#include <type_traits>
#include "../TestEnum.h"

template <class T>
struct is_attribute {
    constexpr static bool value = (std::is_same<int, T>::value ||
                                  std::is_same<bool, T>::value ||
                                  std::is_same<float, T>::value ||
                                  std::is_same<std::string, T>::value) &&
                                  !std::is_base_of<mg::BaseEnum, T>::value;
    constexpr bool operator()() {
        return value;
    }
};

template <class T>
struct is_enum {
    constexpr static bool value = std::is_base_of<mg::BaseEnum, T>::value;
    constexpr bool operator()() {
        return value;
    }
};

template <class T>
struct is_object {
    constexpr static bool value = !is_attribute<T>::value && !is_enum<T>::value;
    constexpr bool operator()() {
        return value;
    }
};

struct default_value {
    template<class T> static typename std::enable_if<std::is_same<int, T>::value, int>::type
    value() { return 0; }

    template<class T> static typename std::enable_if<std::is_same<bool, T>::value, bool>::type
    value() { return false; }

    template<class T> static typename std::enable_if<std::is_same<float, T>::value, float>::type
    value() { return 0.f; }

    template<class T> static typename std::enable_if<std::is_same<std::string, T>::value, std::string>::type
    value() { return std::string(); }
};

#endif //SERIALIZER_SERIALIZERCOMMON_H
