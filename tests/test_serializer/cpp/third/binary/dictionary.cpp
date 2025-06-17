//
//  BinaryFormat.cpp
//  Serializer
//
//  Created by Vladimir Tolmachev on 17.06.2025.
//

#include "dictionary.h"
#include "data.h"
#include <cassert>

namespace mg {

Dictionary::Dictionary()
: _offset(0)
{
}

void Dictionary::add(const std::string& key, size_t size)
{
    assert(!has(key));
    _keys[key] = {_offset, size};
    _offset += size;
}
bool Dictionary::has(const std::string& key) const
{
    return _keys.count(key) > 0;
}
std::pair<size_t, size_t> Dictionary::get(const std::string& key) const
{
    return _keys.at(key);
}

void Dictionary::write(Data& data) const
{
    data.write<uint64_t>(_keys.size());
    for(auto&& [key, pair] : _keys){
        data.write<std::string>(key);
        data.write<uint64_t>(pair.first); // offset
        data.write<uint64_t>(pair.second); // size
    }
}

void Dictionary::read(const Data& data)
{
    _keys.clear();
    auto size = data.read<uint64_t>();
    for(size_t i=0; i<size; ++i){
        auto key = data.read<std::string>();
        auto offset = data.read<uint64_t>();
        auto size = data.read<uint64_t>();
        _keys[key] = {offset, size};
    }
}
}
