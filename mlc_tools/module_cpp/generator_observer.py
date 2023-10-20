from ..core.class_ import Class


PREDEFINED = '''
#ifndef __@{namespace}_@{name}_h__
#define __@{namespace}_@{name}_h__
#include <assert.h>
#include <functional>
#include <set>
#include <thread>
#include <unordered_map>
#include "intrusive_ptr.h"

namespace @{namespace}
{
    class ObservableBase{
    public:
        virtual ~ObservableBase() = default;
        virtual void remove(void* object) = 0;
        virtual void remove(int object) = 0;
    };
    
    
    template<class R> class Observable;

    template<class R, class... A>
    class Observable<R(A...)> : public ObservableBase
    {
    public:
        Observable()
        : _threadId(std::this_thread::get_id())
        , _lock_counter(0)
        {
        }

        template<class T, class M, class... P>
        typename std::enable_if<std::is_member_function_pointer<M>::value>::type
        add(T object, M method, P&&... placeholders)
        {
            auto tag = get_tag(object);
            auto ptr = get_raw_pointer(object);
            if(is_locked())
                _listeners_to_add[tag] = std::bind(method, ptr, std::forward<P>(placeholders)...);
            else
                _listeners[tag] = std::bind(method, ptr, std::forward<P>(placeholders)...);
        }

        template<class T, class F>
        typename std::enable_if<!std::is_member_function_pointer<F>::value || std::is_function<F>::value>::type
        add(T object, F lambda)
        {
            auto tag = get_tag(object);
            if(is_locked())
                _listeners_to_add[tag] = lambda;
            else
                _listeners[tag] = lambda;
        }

        template<class ...T>
        void notify(T&&... args)
        {
            if(!is_locked())
            {
                lock();
                for(auto p : _listeners)
                {
                    if(_listeners_to_remove.count(p.first) == 0)
                        p.second(std::forward<T>(args)...);
                }
                unlock();
            }
        }

        virtual void remove(void* object) override
        {
            remove(get_tag(object));
        }
        virtual void remove(int object) override
        {
            remove(get_tag(object));
        }

    private:
        template<class T> long get_tag(intrusive_ptr<T> t)
        {
            return reinterpret_cast<long>(t.ptr());
        }
        template<class T> typename std::enable_if<std::is_pointer<T>::value, long>::type get_tag(T t)
        {
            return reinterpret_cast<long>(t);
        }
        template<class T> typename std::enable_if<std::is_integral<T>::value, long>::type get_tag(T t)
        {
            return static_cast<long>(t);
        }
        
        template<class T> T* get_raw_pointer(intrusive_ptr<T> t)
        {
            return t.ptr();
        }
        template<class T> typename std::enable_if<std::is_pointer<T>::value, T>::type get_raw_pointer(T t)
        {
            return t;
        }

        void remove(long tag)
        {
            auto iter = _listeners.find( tag );
            if( iter != _listeners.end() )
            {
                if(_lock_counter)
                    _listeners_to_remove.insert(tag);
                else
                    _listeners.erase( iter );
            }
        }
        bool is_locked() const
        {
            assert(_threadId == std::this_thread::get_id());
            return _lock_counter != 0;
        }

        void lock()
        {
            assert(_threadId == std::this_thread::get_id());
            ++_lock_counter;
        }

        void unlock()
        {
            assert(_threadId == std::this_thread::get_id());
            --_lock_counter;
            assert(_lock_counter >= 0);
            if(!is_locked())
            {
                _listeners.insert(_listeners_to_add.begin(), _listeners_to_add.end());
                for( auto func : _listeners_to_remove )
                {
                    remove(func);
                }
                _listeners_to_add.clear();
                _listeners_to_remove.clear();
            }
        }
    private:
        std::thread::id _threadId;
        int _lock_counter;
        std::unordered_map<long, std::function<R(A...)>> _listeners;
        std::unordered_map<long, std::function<R(A...)>> _listeners_to_add;
        std::set<long> _listeners_to_remove;
    };
}


#endif
'''


class GeneratorObserver(object):

    def __init__(self):
        pass

    @staticmethod
    def get_mock():
        cls = Class()
        cls.name = GeneratorObserver.get_observable_name()
        cls.type = 'class'
        cls.auto_generated = False
        return cls

    @staticmethod
    def get_observable_name():
        return 'Observable'

    @staticmethod
    def generate(model):
        text = PREDEFINED
        filename = GeneratorObserver.get_observable_name() + '.h'
        text = text.replace('@{namespace}', 'mg')
        text = text.replace('@{name}', GeneratorObserver.get_observable_name())

        mock = GeneratorObserver.get_mock()
        model.add_file(mock, filename, text)
        model.add_class(mock)
