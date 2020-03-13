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
#include "config.h"



#if SUPPORT_XML_PROTOCOL

//mg::intrusive_ptr<mg::CommandBase> createCommand(const pugi::xml_node& xml)
//{
//	auto type = xml.name();
//	auto command = mg::Factory::shared().build<mg::CommandBase>(type);
//	if (command != nullptr)
//		command->deserialize_xml(xml);
//	return command;
//}
//
//mg::intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload)
//{
//	pugi::xml_document doc;
//	doc.load(payload.c_str());
//	auto root = doc.root().first_child();
//	return createCommand(root);
//}
//
//#elif SUPPORT_JSON_PROTOCOL
//
//mg::intrusive_ptr<mg::CommandBase> createCommand(const Json::Value& json)
//{
//	auto type = json.getMemberNames()[0];
//	auto command = mg::Factory::shared().build<mg::CommandBase>(type);
//	if (command != nullptr)
//		command->deserialize_json(json[type]);
//	return command;
//}
//
//mg::intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload)
//{
//	Json::Value json;
//	Json::Reader reader;
//	reader.parse(payload, json);
//	return createCommand(json);
//}

#endif
