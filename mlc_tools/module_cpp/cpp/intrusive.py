INTRUSIVE_HPP = '''#ifndef __intrusive_ptr__
#define __intrusive_ptr__

#include <assert.h>
#include <memory>

namespace @{namespace}
{
    template <class TRef>
    class intrusive_ptr
    {
    public:
        intrusive_ptr(TRef * ptr = nullptr) : _ptr(nullptr)
        {
            reset(ptr);
        }

        intrusive_ptr(const intrusive_ptr& holder) : _ptr(nullptr)
        {
            reset(holder._ptr);
        }

        template <class OtherPtr>
        intrusive_ptr(intrusive_ptr<OtherPtr> holder) : _ptr(nullptr)
        {
            reset(holder.ptr());
        }

        intrusive_ptr(intrusive_ptr&& holder) : _ptr(nullptr)
        {
            _ptr = holder._ptr;
            holder._ptr = nullptr;
        }

        intrusive_ptr& operator = (const intrusive_ptr& r)
        {
            reset(r._ptr);
            return *this;
        }

        template <typename R>
        intrusive_ptr<TRef>& operator = (intrusive_ptr<R> r)
        {
            reset(r.ptr());
            return *this;
        }

        intrusive_ptr<TRef>& operator = (TRef * r)
        {
            reset(r);
            return *this;
        }

        virtual ~intrusive_ptr()
        {
            reset(nullptr);
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
            assert(_ptr);
            return _ptr;
        }
        const TRef* operator -> ()const
        {
            assert(_ptr);
            return _ptr;
        }

        TRef& operator * ()
        {
            assert(_ptr);
            return *_ptr;
        }
        const TRef& operator * ()const
        {
            assert(_ptr);
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

        void reset(TRef * ptr)
        {
            if(ptr != _ptr)
            {
                if(ptr)
                {
                    ptr->retain();
                }
                if(_ptr)
                {
                    _ptr->release();
                }

                _ptr = ptr;
            }
        }

        bool operator == (TRef * pointer)const
        {
            return _ptr == pointer;
        }

        bool operator != (const TRef * pointer)const
        {
            return _ptr != pointer;
        }

        bool operator != (const intrusive_ptr& holder)const
        {
            return _ptr != holder._ptr;
        }

        template <class Other>
        bool operator != (const intrusive_ptr<Other>& holder)const
        {
            return _ptr != holder.ptr();
        }

        bool operator < (const intrusive_ptr& holder)const
        {
            return _ptr < holder._ptr;
        }

    private:
        TRef * _ptr;
    };

    template<class T, class R>
    intrusive_ptr<T> dynamic_pointer_cast_intrusive(intrusive_ptr<R> pointer)
    {
        intrusive_ptr<T> result;
        T* raw = dynamic_cast<T*>(pointer.ptr());
        result.reset(raw);
        return result;
    }

    template<class Type, class...TArgs>
    inline intrusive_ptr<Type> make_intrusive(TArgs&& ... _Args)
    {
        intrusive_ptr<Type> holder;
        holder.reset(new Type(std::forward<TArgs>(_Args)...));
        holder->release();
        return holder;
    }

}

#endif
'''