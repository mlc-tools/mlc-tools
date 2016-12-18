#pragma once
#include <vector>
#include "RapidJsonNode.h"
#include <iostream>

class TestCase
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
			
			RapidJsonNode json;
			one.serialize( json );
			two.deserialize( json );

			std::string string;
			json.toString( string );
			std::cout << std::endl << string;
			return one == two;
		}
	};
	std::vector<Test*> _tests;
};

