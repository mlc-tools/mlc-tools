

#include <fstream>
#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include "generated_cpp/TestData.h"
#include "generated_cpp/SerializerXml.h"
#include "generated_cpp/SerializerJson.h"

int main()
{
    if(true)
    {
        pugi::xml_document doc;
        doc.load_file("data.php.xml");
        auto root = doc.root().first_child();

        auto data = mg::make_intrusive<mg::TestData>();
        mg::DeserializerXml deserializer(root);
        data->deserialize_xml(deserializer);

        pugi::xml_document doc2;
        auto root2 = doc2.root().append_child("data");
        mg::SerializerXml serializer(root2);
        data->serialize_xml(serializer);

        doc2.save_file("data.cpp.xml");
	}
	else
	{
        Json::Value json;
        Json::Reader reader;
        std::fstream fs("data.php.json", std::fstream::in);
        std::string buffer((std::istreambuf_iterator<char>(fs)),
                           (std::istreambuf_iterator<char>()));
        reader.parse(buffer, json);

        auto data = mg::make_intrusive<mg::TestData>();

        mg::DeserializerJson deserializer(json);
        data->deserialize_json(deserializer);

        Json::Value json2;
        mg::SerializerJson serializer(json2);
        data->serialize_json(serializer);

        Json::StreamWriterBuilder wbuilder;
        wbuilder["indentation"] = " ";
        auto string = Json::writeString(wbuilder, json2);

        std::fstream fso("data.cpp.json", std::fstream::out);
        fso << string;
    }

	return 0;
}
