#pragma once
#include <vector>
#include "jsoncpp/json.h"
#include "SerializedObject.h"
#include <iostream>
#include <string>

class TestCase : public mg::SerializedObject
{
public:
	virtual bool execute() = 0;
};

class TestSerialization : public TestCase
{
public:
	virtual bool execute()override
	{
		bool result = true;
		build();
		for( auto test : _tests )
		{
			result = result && test->run();
		}
		return result;
	}

private:
	void build();

	class Test
	{
	public:
		virtual bool run() = 0;
	};
	template <class T>
	class TestT : public Test
	{
	public:
		virtual bool run() override
		{
			auto one = T::__create_instance__();
			auto two = T();
			
			Json::Value json;
			one.serialize( json );
			two.deserialize( json );

			Json::StreamWriterBuilder wbuilder;
			//wbuilder["indentation"] = "";
			auto string = Json::writeString( wbuilder, json );

			std::cout << std::endl << string;
			return one == two;
		}
	};
	std::vector<Test*> _tests;
};

