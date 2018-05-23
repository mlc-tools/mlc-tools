

#include <fstream>
#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include "generated_cpp/TestData.h"
#include "generated_cpp/config.h"

int main()
{
#if MG_SERIALIZE_FORMAT == MG_XML
	pugi::xml_document doc;
	doc.load_file("data.php.xml");
	auto root = doc.root().first_child();

	auto data = mg::make_intrusive<mg::TestData>();
	data->deserialize(root);

	pugi::xml_document doc2;
	auto root2 = doc2.root().append_child("data");
	data->serialize(root2);

	doc2.save_file("data.cpp.xml");
#else
	Json::Value json;
	Json::Reader reader;
	std::fstream fs("data.php.json", std::fstream::in);
	std::string buffer((std::istreambuf_iterator<char>(fs)),
					   (std::istreambuf_iterator<char>()));
	reader.parse(buffer, json);

	auto data = mg::make_intrusive<mg::TestData>();
	data->deserialize(json);

	Json::Value json2;
	data->serialize(json2);

	Json::StreamWriterBuilder wbuilder;
	wbuilder["indentation"] = " ";
	auto string = Json::writeString(wbuilder, json2);

	std::fstream fso("data.cpp.json", std::fstream::out);
	fso << string;
#endif

	return 0;
}
