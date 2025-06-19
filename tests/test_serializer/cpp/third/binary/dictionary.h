//
//  BinaryFormat.hpp
//  Serializer
//
//  Created by Vladimir Tolmachev on 17.06.2025.
//

#ifndef binary_dictionary_h
#define binary_dictionary_h

#include <string>
#include <map>

namespace mg
{

class Data;

class Dictionary
{
public:
    Dictionary();
    
    void write(Data& data) const;
    void read(const Data& data);
    
    void add(const std::string& key, size_t size);
    bool has(const std::string& key) const;
    std::pair<size_t, size_t> get(const std::string& key) const;
    std::unordered_map<std::string, std::pair<size_t, size_t>> get_all() const { return _keys; };
private:
    std::unordered_map<std::string, std::pair<size_t, size_t>> _keys; /* key-> [offset, size] */
    size_t _offset;
};


}
#endif /* BinaryFormat_hpp */

