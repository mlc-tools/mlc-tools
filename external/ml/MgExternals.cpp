#include "core/CommandBase.h"
#include "Factory.h"
#include <sstream>
#include "ml/Generics.h"


intrusive_ptr<mg::CommandBase> createCommand(const pugi::xml_node& xml)
{
	auto type = xml.name();
	auto command = Factory::shared().build<mg::CommandBase>(type);
	if (command != nullptr)
		command->deserialize(xml);
	return command;
}

intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload)
{
	pugi::xml_document doc;
	doc.load(payload.c_str());
	auto root = doc.root().first_child();
	return createCommand(root);
}

std::string getSerializedString(const mg::SerializedObject* object) 
{
	pugi::xml_document doc;
	auto root = doc.append_child(object->getType().c_str());
	object->serialize(root);

	std::stringstream stream;
	pugi::xml_writer_stream writer(stream);
	//doc.save(writer, "\t", pugi::format_no_declaration, pugi::xml_encoding::encoding_utf8);
	doc.save(writer);
	return stream.str();
}

namespace mg
{
	std::string CommandBase::getSerializedString() const
	{
		return ::getSerializedString(this);
	}
}