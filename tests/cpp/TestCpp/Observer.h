/******************************************************************************/
/*
 * Copyright 2014-2015 Vladimir Tolmachev
 *
 * Author: Vladimir Tolmachev
 * Project: ml
 * e-mail: tolm_vl@hotmail.com
 * If you received the code is not the author, please contact me
 */
/******************************************************************************/

#ifndef __Observer_h__
#define __Observer_h__
#include <functional>
#include <vector>
#include <assert.h>
#include "IntrusivePtr.h"
#include <map>
#include <set>
#include <list>

template <class Function>
class Observer
{
public:
	Observer()
		: _locks(0)
		, _functions()
		, _functionsOnAdd()
		, _functionsOnRemove()
	{}

	~Observer(void)
	{}

	void add( void* object, const Function & function )
	{
		add( getTag( object ), function );
	}
	void add( void* object, int addindex, const Function & function )
	{
		add( getTag( object, addindex ), function );
	}

	bool operator ==(const Observer& rhs)const
	{
		return false;
	}

protected:
	void add(int tag, const Function & function)
	{
		assert(function);
		if( _locks )
			_functionsOnAdd[tag] = function;
		else
			_functions[tag] = function;
	}
	void remove(int tag)
	{
		auto iter = _functions.find(tag);
		if (iter != _functions.end())
		{
			if( _locks )
				_functionsOnRemove.insert(tag);
			else
				_functions.erase(iter);
		}
	}
public:
	void remove( void* object )
	{
		auto tag = getTag( object );
		remove( tag );
	}
	void remove( void* object, int addindex )
	{
		auto tag = getTag( object, addindex );
		remove( tag );
	}

	void lockEvents()
	{
		++_locks;
		assert(_locks >= 0);
	}

	void unlockEvents()
	{
		--_locks;
		assert(_locks >= 0);
	};

	size_t getListenersSize()const
	{
		return
			_functions.size() +
			_functionsOnAdd.size() -
			_functionsOnRemove.size();
	}


	void pushevent()
	{
		if( _locks == 0 )
		{
			++_locks;
			for( auto& func : _functions )
			{
				call( func.first, func.second );
			}
			--_locks;
		}
		prepare();
	}

	template<class A0>void pushevent(A0 a0)
	{
		if( _locks == 0 )
		{
			++_locks;
			for( auto& func : _functions )
			{
				call( func.first, func.second, a0 );
			}
			--_locks;
		}
		prepare();
	}

	template<class A0, class A1>void pushevent(A0 a0, A1 a1)
	{
		if( _locks == 0 )
		{
			++_locks;
			for( auto& func : _functions )
			{
				call( func.first, func.second, a0, a1 );
			}
			--_locks;
		}
		prepare();
	}

	template<class A0, class A1, class A2>void pushevent(A0 a0, A1 a1, A2 a2)
	{
		if( _locks == 0 )
		{
			++_locks;
			for( auto& func : _functions )
			{
				call( func.first, func.second, a0, a1, a2 );
			}
			--_locks;
		}
		prepare();
	}

	/*
	* push event with return value
	*/

	template< class TResult, class A0> std::list<TResult> pushevent_result(A0 a0)
	{
		std::list<TResult> result;
		if (_locks == 0)
		{
			++_locks;
			for (auto& func : _functions)
			{
				if (_functionsOnRemove.find(func.first) == _functionsOnRemove.end())
				{
					auto r = func.second(a0);
					result.push_back(r);
				}
			}
			--_locks;
		}
		prepare();
		return result;
	}

protected:
	int getTag( void* object )
	{
		auto tag = reinterpret_cast<long>(object);
		return tag;
	}
	int getTag( void* object, int addindex )
	{
		int tag = getTag(object) + addindex;
		return tag;
	}

	template <class F> void call(int id, const F& f)
	{ if (_functionsOnRemove.find(id) == _functionsOnRemove.end()) f(); }

	template <class F, class A0> void call(int id, const F& f, A0 a0)
	{ if (_functionsOnRemove.find(id) == _functionsOnRemove.end()) f(a0); }

	template <class F, class A0, class A1> void call(int id, const F& f, A0 a0, A1 a1)
	{ if (_functionsOnRemove.find(id) == _functionsOnRemove.end()) f(a0, a1); }

	template <class F, class A0, class A1, class A2> void call( int id, const F& f, A0 a0, A1 a1, A2 a2 )
	{ if (_functionsOnRemove.find(id) == _functionsOnRemove.end()) f(a0, a1, a2); }

	void prepare()
	{
		for (auto func : _functionsOnAdd)
			add(func.first, func.second);
		for (auto func : _functionsOnRemove)
			remove(func);
		_functionsOnAdd.clear();
		_functionsOnRemove.clear();
	}
private:
	int _locks;
	std::map<int, Function > _functions;
	std::map<int, Function > _functionsOnAdd;
	std::set<int> _functionsOnRemove;
};

#endif
