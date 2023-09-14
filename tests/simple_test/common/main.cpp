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
#include "TestEnum.h"
#include "tests/Side.h"
#include "tests/enum.h"
#include "tests/TestSerializeAllTypes.h"
#include <iostream>
#include "DataStorage.h"
#include <fstream>
#include "config.h"
#include "mg_Factory.h"
#include "AllTests.h"
#include "tests/Logger.h"
#include "tests/RunAllTests.h"
#include "Registrar.h"
#include "SerializerCommon.h"
#include "Observable.h"


class ListenerAuto
{
public:
    std::vector<mg::ObservableBase*> observers;

    virtual ~ListenerAuto()
    {
        for(auto observer : this->observers)
        {
            observer->remove(this);
        }
    }

    template<class R, class... A, class T, class M, class... P> typename std::enable_if<std::is_member_function_pointer<M>::value>::type
    listen(mg::Observable<R(A...)>& observer, T object, M method, P&&... placeholders)
    {
        observers.push_back(&observer);
        observer.add(object, method, std::forward<P>(placeholders)...);
    }

    template<class R, class... A, class F> typename std::enable_if<!std::is_member_function_pointer<F>::value || std::is_function<F>::value>::type
    listen(mg::Observable<R(A...)>& observer, F lambda)
    {
        observers.push_back(&observer);
        observer.add(this, lambda);
    }
};


extern mg::intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload);
std::string root = "../../";
void initialize_data_storage()
{
#if SUPPORT_XML_PROTOCOL
	std::fstream stream(root + "assets/data.xml", std::ios::in);
    std::cout << "SERIALIZE_FORMAT == XML\n";
	std::string str((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
	mg::DataStorage::shared().initialize_xml(str);
#elif SUPPORT_JSON_PROTOCOL
	std::fstream stream(root + "assets/data.json", std::ios::in);
    std::cout << "SERIALIZE_FORMAT == JSON\n";
	std::string str((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
	mg::DataStorage::shared().initialize_json(str);
#endif
}


class Logger : public mg::Logger
{
public:
    virtual void message(const std::string& message) override
    {
        std::cout << message << std::endl;
    }
};


int main(int argc, char ** args)
{
    static_assert(mg::is_attribute<int>::value);
    static_assert(mg::is_attribute<float>::value);
    static_assert(mg::is_attribute<bool>::value);
    static_assert(mg::is_attribute<std::string>::value);
    static_assert(mg::is_enum<mg::TestEnum>::value);
    static_assert(!mg::is_attribute<mg::TestEnum>::value);

    static_assert(mg::is_data<const mg::DataUnit*>::value);
    static_assert(mg::is_data<mg::DataUnit const*>::value);
    static_assert(!mg::is_data<mg::DataUnit*>::value);
    static_assert(!mg::is_data<mg::DataUnit* const>::value);
    static_assert(!mg::is_data<const mg::TestEnum*>::value);

    static_assert(mg::is_serializable<mg::DataUnit>::value);
    static_assert(!mg::is_serializable<mg::TestEnum>::value);
    static_assert(!mg::is_serializable<int>::value);
    static_assert(!mg::is_serializable<std::string>::value);
    static_assert(!mg::is_serializable<mg::intrusive_ptr<mg::DataUnit>>::value);

    static_assert(mg::is_intrusive<mg::intrusive_ptr<mg::DataUnit>>::value);
    static_assert(!mg::is_intrusive<mg::DataUnit>::value);
    static_assert(!mg::is_intrusive<mg::DataUnit*>::value);
    static_assert(!mg::is_intrusive<const mg::DataUnit*>::value);

    static_assert(mg::is_not_serialize_to_attribute<std::vector<int>>::value);
    static_assert(mg::is_not_serialize_to_attribute<std::map<int, mg::DataUnit>>::value);
    static_assert(mg::is_not_serialize_to_attribute<mg::DataUnit>::value);
    static_assert(mg::is_not_serialize_to_attribute<mg::intrusive_ptr<mg::DataUnit>>::value);
    static_assert(!mg::is_not_serialize_to_attribute<int>::value);
    static_assert(!mg::is_not_serialize_to_attribute<const mg::DataUnit*>::value);
    static_assert(!mg::is_not_serialize_to_attribute<mg::TestEnum>::value);

    static_assert(std::is_same<mg::DataUnit, mg::data_type<const mg::DataUnit*>::type>::value);
    
    
    if(argc > 1)
    {
        root = args[1];
    }
    mg::register_classes();

	auto result = true;
	initialize_data_storage();

	Logger logger;

	result = test_enum();
    result = test_side();
    result = test_all_types(&logger);
	result = mg::AllTests::run(&logger) && result;

    mg::RunAllTests test;
    test.initialize(&logger);
    result = result && test.execute();

	std::cout << "Execute results = " << (result ? "Ok" : "Fail") << std::endl;

    int count = 0;
	mg::Observable<void()> observer;
	{
	    ListenerAuto listener;
	    listener.listen(observer, [&count](){
	        std::cout << "Nice" << std::endl;
	        ++count;
	    });
	    observer.notify();
	}
	observer.notify();
	assert(count == 1);

	return result ? 0 : -1;
}
