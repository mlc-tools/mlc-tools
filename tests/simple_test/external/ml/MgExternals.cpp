/******************************************************************************/
/*
* Copyright 2014-2017 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/

#include "core/CommandBase.h"
#include "mg_Factory.h"
#include <sstream>
#include "mg_config.h"



#if MG_SERIALIZE_FORMAT == MG_XML

mg::intrusive_ptr<mg::CommandBase> createCommand(const pugi::xml_node& xml)
{
	auto type = xml.name();
	auto command = mg::Factory::shared().build<mg::CommandBase>(type);
	if (command != nullptr)
		command->deserialize(xml);
	return command;
}

mg::intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload)
{
	pugi::xml_document doc;
	doc.load(payload.c_str());
	auto root = doc.root().first_child();
	return createCommand(root);
}

std::string getSerializedString(const mg::SerializedObject* object)
{
	pugi::xml_document doc;
	auto root = doc.append_child(object->get_type().c_str());
	object->serialize(root);

	std::stringstream stream;
	pugi::xml_writer_stream writer(stream);
	//doc.save(writer, "\t", pugi::format_no_declaration, pugi::xml_encoding::encoding_utf8);
	doc.save(writer);
	return stream.str();
}

void deserialize(mg::SerializedObject* object, const std::string& payload)
{
	pugi::xml_document doc;
	doc.load(payload.c_str());
	object->deserialize(doc.root().first_child());
}

#elif MG_SERIALIZE_FORMAT == MG_JSON

mg::intrusive_ptr<mg::CommandBase> createCommand(const Json::Value& json)
{
	auto type = json.getMemberNames()[0];
	auto command = mg::Factory::shared().build<mg::CommandBase>(type);
	if (command != nullptr)
		command->deserialize(json[type]);
	return command;
}

mg::intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload)
{
	Json::Value json;
	Json::Reader reader;
	reader.parse(payload, json);
	return createCommand(json);
}

std::string getSerializedString(const mg::SerializedObject* object)
{
	Json::Value json;
	object->serialize(json[object->get_type()]);

	Json::StreamWriterBuilder wbuilder;
	wbuilder["indentation"] = "";
	auto string = Json::writeString(wbuilder, json);

	return string;
}

void deserialize(mg::SerializedObject* object, const std::string& payload)
{
	Json::Value json;
	Json::Reader reader;
	reader.parse(payload, json);
	object->deserialize(json[object->get_type()]);
}
#endif

namespace mg
{
	std::string CommandBase::getSerializedString() const
	{
		return ::getSerializedString(this);
	}
}
