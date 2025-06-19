SERIALIZER_COMMON = '''#ifndef __mg_SERIALIZERCOMMON_H__
#define __mg_SERIALIZERCOMMON_H__

#include <type_traits>
#include "BaseEnum.h"
#include "intrusive_ptr.h"

namespace mg
{
class SerializerXml;
class DeserializerXml;
class SerializerJson;
class DeserializerJson;

template<class T>
struct is_attribute
{
    constexpr static bool value = (std::is_same<int, T>::value ||
                                   std::is_same<unsigned int, T>::value ||
                                   std::is_same<int64_t, T>::value ||
                                   std::is_same<uint64_t, T>::value ||
                                   std::is_same<bool, T>::value ||
                                   std::is_same<float, T>::value ||
                                   std::is_same<double, T>::value ||
                                   std::is_same<std::string, T>::value) &&
                                  !std::is_base_of<BaseEnum, T>::value;

    constexpr bool operator()() {
        return value;
    }
};

template<class T>
struct is_enum
{
    constexpr static bool value = std::is_base_of<BaseEnum, T>::value;

    constexpr bool operator()() {
        return value;
    }
};

template<typename, typename T>
struct has_serialize {
    static_assert( std::integral_constant<T, false>::value, "Second template parameter needs to be of function type.");
};
template<typename C, typename Ret, typename... Args>
struct has_serialize<C, Ret(Args...)> {
private:
    template<typename T>
    static constexpr auto check_xml(T*) -> typename std::is_same< decltype( std::declval<T>().serialize_xml( std::declval<Args>()... ) ),Ret>::type;
    template<typename>
    static constexpr std::false_type check_xml(...);
    typedef decltype(check_xml<C>(0)) type_xml;

    template<typename T>
    static constexpr auto check_json(T*) -> typename std::is_same< decltype( std::declval<T>().serialize_json( std::declval<Args>()... ) ),Ret>::type;
    template<typename>
    static constexpr std::false_type check_json(...);
    typedef decltype(check_json<C>(0)) type_json;
public:
    static constexpr bool value_xml = type_xml::value;
    static constexpr bool value_json = type_json::value;
};
template <class T>
struct is_serializable{
    constexpr static bool value =
            has_serialize<T, void(SerializerXml&)>::value_xml ||
            has_serialize<T, void(SerializerJson&)>::value_json;
    constexpr bool operator()() {
        return value;
    }
};

template<class T> struct is_data : std::false_type {};
template<class T> struct is_data<const T*> {
    constexpr static bool value = !is_enum<T>::value && !is_attribute<T>::value && is_serializable<T>::value;
};
template <class T> struct data_type {};
template <class T> struct data_type<const T*>{
    typedef T type;
};


template<class T> struct is_intrusive : std::false_type {};
template<class T> struct is_intrusive<intrusive_ptr<T>> {
    constexpr static bool value = is_serializable<T>::value;
};

template<class T> struct is_not_serialize_to_attribute {
    constexpr static bool value =
            !is_enum<T>::value &&
            !is_attribute<T>::value &&
            !is_data<T>::value;
};

struct default_value
{
    template<class T>
    static typename std::enable_if<std::is_same<int, T>::value, int>::type
    value() { return 0; }

    template<class T>
    static typename std::enable_if<std::is_same<unsigned int, T>::value, unsigned int>::type
    value() { return 0; }

    template<class T>
    static typename std::enable_if<std::is_same<int64_t, T>::value, int64_t>::type
    value() { return 0ull; }

    template<class T>
    static typename std::enable_if<std::is_same<uint64_t, T>::value, uint64_t>::type
    value() { return 0ll; }

    template<class T>
    static typename std::enable_if<std::is_same<bool, T>::value, bool>::type
    value() { return false; }

    template<class T>
    static typename std::enable_if<std::is_same<float, T>::value, float>::type
    value() { return 0.f; }

    template<class T>
    static typename std::enable_if<std::is_same<double, T>::value, double>::type
    value() { return 0.0; }

    template<class T>
    static typename std::enable_if<std::is_same<std::string, T>::value, std::string>::type
    value() { return std::string(); }
};

}

#endif //SERIALIZER_SERIALIZERCOMMON_H
'''