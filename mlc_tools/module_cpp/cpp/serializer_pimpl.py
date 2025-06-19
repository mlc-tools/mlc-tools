SERIALIZER_PIMPL = '''
#ifndef __mg_Pimpl_h__
#define __mg_Pimpl_h__

#include <array>

namespace mg{
template <class T, size_t size>
class Pimpl
{
public:
    Pimpl()
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        new (_data.data()) T;
    }
    Pimpl(const Pimpl& rhs)
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        new (_data.data()) T;
        *data() = *rhs.data();
    }
    Pimpl(Pimpl&& rhs) noexcept
    : _data(std::move(rhs._data))
    {
        static_assert(size == sizeof(T), "Check size pimpl");
    }
    ~Pimpl()
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        auto ptr = data();
        ptr->~T();
    }
    Pimpl& operator=(const T& data_)
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        *data() = data_;
        return *this;
    }

    T* operator ->()
    {
        return data();
    }
    const T* operator ->() const
    {
        return data();
    }

    T& operator *()
    {
        return *data();
    }
    const T& operator *() const
    {
        return *data();
    }
private:
    T* data()
    {
        return reinterpret_cast<T*>(_data.data());
    }
    const T* data()const
    {
        return reinterpret_cast<const T*>(_data.data());
    }
private:
    std::array<unsigned char, size> _data;
};
}

#endif /* __mg_Pimpl_h__ */
'''