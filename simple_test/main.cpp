#include "core/CommandBase.h"
#include "IntrusivePtr.h"
#include <iostream>

extern intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload);

int main()
{
	int test_user_id = 123;
	int test_time = 1231235245;

	auto command = make_intrusive<mg::CommandBase>();
	command->user_id = test_user_id;
	command->current_time = test_time;
	auto buffer = command->getSerializedString();
	auto deserialized = createCommand(buffer);

	std::cout << "serialized string:" << std::endl;
	std::cout << buffer << std::endl;

	auto result = true;
	result = result && deserialized->user_id == command->user_id;
	result = result && deserialized->current_time == command->current_time;

	std::cout << "Execute results = " << (result ? "Ok" : "Fail") << std::endl;

	return result ? 0 : -1;
}