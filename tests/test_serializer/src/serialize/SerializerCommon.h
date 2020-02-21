//
// Created by Vladimir Tolmachev on 2020-02-21.
//

#ifndef SERIALIZER_SERIALIZERCOMMON_H
#define SERIALIZER_SERIALIZERCOMMON_H

#include <type_traits>

template <class T>
struct is_attribute {
    constexpr static bool value = std::is_same<int, T>::value ||
                                  std::is_same<bool, T>::value ||
                                  std::is_same<float, T>::value ||
                                  std::is_same<std::string, T>::value;
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
