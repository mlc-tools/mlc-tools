#include "TestSerializationCommandSequence.h"
#include "CommandSequence.h"
#include "../../../out/RequestAuthorize.h"
#include "../../../out/RequestCreateTower.h"
#include "../../../out/RequestStartLevel.h"


bool TestSerializationCommandSequence::execute()
{
	CommandSequence sequence;
	auto auth = std::make_shared<mg::RequestAuthorize>();
	auto create = std::make_shared<mg::RequestCreateTower>();
	auto start = std::make_shared<mg::RequestStartLevel>();
	auth->user = 123;
	auth->auth_key = "123";
	create->name = "tower";
	create->position = cocos2d::Point( 123, 456 );
	sequence._list.push_back( auth );
	sequence._list.push_back( create );
	sequence._list.push_back( start );
	
	auto str = sequence.getSerializedString();
	std::cout << std::endl << str;
	Json::Value json;
	Json::Reader reader;
	reader.parse( str, json );
	auto command = std::dynamic_pointer_cast<CommandSequence> (createCommand( json ));
	if( !command )
		return false;
	if( command->_list.size() != 3 )
		return false;
	if( !std::dynamic_pointer_cast<mg::RequestAuthorize>(command->_list[0]) )
		return false;
	if( !std::dynamic_pointer_cast<mg::RequestCreateTower>(command->_list[1]) )
		return false;
	if( !std::dynamic_pointer_cast<mg::RequestStartLevel>(command->_list[2]) )
		return false;

	if( !(*auth == *std::dynamic_pointer_cast<mg::RequestAuthorize>(command->_list[0])) )
		return false;
	if( !(*create == *std::dynamic_pointer_cast<mg::RequestCreateTower>(command->_list[1])) )
		return false;
	if( !(*start == *std::dynamic_pointer_cast<mg::RequestStartLevel>(command->_list[2])) )
		return false;
	return true;

}
