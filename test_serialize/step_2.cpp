

#include <fstream>
#include "pugixml/pugixml.hpp"
#include "generated_cpp/xml/TestData.h"

int main()
{
	pugi::xml_document doc;
	doc.load_file("data.php.xml");
	auto root = doc.root().first_child();

	auto data = make_intrusive<mg::TestData>();
	data->deserialize(root);

	pugi::xml_document doc2;
	auto root2 = doc2.root().append_child("data");
	data->serialize(root2);

	doc2.save_file("data.cpp.xml");


	return 0;
}