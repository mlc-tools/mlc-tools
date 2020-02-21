//
//  Pimpl.hpp
//  FastPimpl
//
//  Created by Vladimir Tolmachev on 12/01/2020.
//  Copyright © 2020 Vladimir Tolmachev. All rights reserved.
//

#ifndef fast_pimpl_hpp
#define fast_pimpl_hpp

#include <stdio.h>
#include <array>
#include <vector>
#include <iostream>

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

#endif /* fast_pimpl_hpp */
