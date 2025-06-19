//
//  BinaryFormat.cpp
//  Serializer
//
//  Created by Vladimir Tolmachev on 17.06.2025.
//

#include "data.h"
#include <cassert>

namespace mg{

Data::Data()
: _data()
, _iter_read(0)
{
    _data.reserve(1024);
}

Data::Data(Data&& data)
: _data(std::move(data._data))
,_iter_read(data._iter_read)
{
    
}

Data::Data(const Data& data)
: _data(data._data)
, _iter_read(data._iter_read)
{
    
}

Data::Data(const std::vector<unsigned char>& blob)
: _data(blob)
, _iter_read(0)
{
}

Data& Data::operator=(const Data& data)
{
    _data = data._data;
    _iter_read = data._iter_read;
    return *this;
}

void Data::set_data(const std::vector<unsigned char>& data)
{
    _data = data;
    _iter_read = 0;
}

std::vector<unsigned char> Data::get_data() const
{
    return _data;
}

void Data::set_offset(size_t offset) const
{
    assert(offset < _data.size());
    _iter_read = offset;
}

Data::data_type Data::read_type(size_t offset) const
{
    assert(offset + sizeof(data_type) < _data.size());
    data_type type_read;
    memcpy(&type_read, &_data.at(offset), sizeof(data_type));
    return type_read;
}

}
