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

#ifndef __Intrusive_Ptr__
#define __Intrusive_Ptr__

#include <assert.h>

namespace mg
{
	class SerializedObject;
}

void __IntrusivePtr__retain( mg::SerializedObject* ptr );
void __IntrusivePtr__release( mg::SerializedObject* ptr );

template <class TRef>
class IntrusivePtr
{
public:
	IntrusivePtr( TRef * ptr = nullptr ) : _ptr( nullptr )
	{
		reset( ptr );
	}

	IntrusivePtr( const IntrusivePtr & holder ) : _ptr( nullptr )
	{
		reset( holder._ptr );
	}

	template <class OtherPtr>
	IntrusivePtr( IntrusivePtr<OtherPtr> holder ) : _ptr( nullptr )
	{
		reset( holder.ptr() );
	}

	IntrusivePtr( IntrusivePtr && holder ) : _ptr( nullptr )
	{
		_ptr = holder._ptr;
		holder._ptr = nullptr;
	}

	IntrusivePtr& operator = (const IntrusivePtr& r)
	{
		reset( r._ptr );
		return *this;
	}

	template <typename R>
	IntrusivePtr<TRef>& operator = (IntrusivePtr<R> r)
	{
		reset( r.ptr() );
		return *this;
	}

	IntrusivePtr<TRef>& operator = (TRef * r)
	{
		reset( r );
		return *this;
	}

	virtual ~IntrusivePtr()
	{
		reset( nullptr );
	}

	TRef* ptr()
	{
		return _ptr;
	}

	const TRef* ptr()const
	{
		return _ptr;
	}

	TRef* operator -> ()
	{
		assert( _ptr );
		return _ptr;
	}
	const TRef* operator -> ()const
	{
		assert( _ptr );
		return _ptr;
	}

	TRef& operator * ()
	{
		assert( _ptr );
		return *_ptr;
	}
	const TRef& operator * ()const
	{
		assert( _ptr );
		return *_ptr;
	}

	operator TRef* ()
	{
		return _ptr;
	}
	operator const TRef* ()const
	{
		return _ptr;
	}

	void reset( TRef * ptr )
	{
		if( ptr != _ptr )
		{
			if( ptr )
				__IntrusivePtr__retain( ptr );
			if( _ptr )
				__IntrusivePtr__release( _ptr );
			_ptr = ptr;
		}
	}

	bool operator == (const IntrusivePtr & holder)const
	{
		return _ptr == holder._ptr;
	}

	bool operator == (const TRef * pointer)const
	{
		return _ptr == pointer;
	}

	template <class Other>
	bool operator == (const IntrusivePtr<Other> & holder)const
	{
		return _ptr == holder.ptr();
	}

	bool operator != (const TRef * pointer)const
	{
		return _ptr != pointer;
	}

	bool operator != (const IntrusivePtr & holder)const
	{
		return _ptr != holder._ptr;
	}

	template <class Other>
	bool operator != (const IntrusivePtr<Other> & holder)const
	{
		return _ptr != holder.ptr();
	}

	bool operator < (const IntrusivePtr & holder)const
	{
		return _ptr < holder._ptr;
	}

private:
	TRef * _ptr;
};

template<class Type, class...TArgs>
inline IntrusivePtr<Type> make_intrusive( TArgs && ... _Args )
{
	IntrusivePtr<Type> holder;
	Type * ptr( nullptr );
	ptr = new Type( std::forward<TArgs>( _Args )... );
	if( ptr )
	{
		holder.reset( ptr );
		ptr->release();
	}

	return holder;
}

template<class T, class R>
IntrusivePtr<T> dynamic_pointer_cast_intrusive( IntrusivePtr<R> pointer )
{
	IntrusivePtr<T> result;
	T* raw = dynamic_cast<T*>(pointer.ptr());
	result.reset( raw );
	return result;
}

#endif
