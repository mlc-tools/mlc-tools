from .Class import Class


cpp = '''
#ifndef __@{namespace}_@{name}_h__
#define __@{namespace}_@{name}_h__
#include <assert.h>
#include <functional>
#include <map>
#include <set>

namespace @{namespace}
{
    template<class R, class ...A>
    class @{name}
    {
    public:
        @{name}()
        : _lock_counter(0)
        {
        }

        template<class T, class M, class ...P>
        void add(T* object, M method, P&&... placeholders)
        {
            auto tag = reinterpret_cast<long>(object);
            if(is_locked())
            {
                _listeners_to_add[tag] = std::bind(method, object, std::forward<P>(placeholders)...);
            }
            else
            {
                _listeners[tag] = std::bind(method, object, std::forward<P>(placeholders)...);
            }
        }

        template<class T, class F>
        void add_lambda(T* object, F lambda)
        {
            auto tag = reinterpret_cast<long>(object);
            if(is_locked())
            {
                _listeners_to_add[tag] = lambda;
            }
            else
            {
                _listeners[tag] = lambda;
            }
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
                    {
                        p.second(std::forward<T>(args)...);
                    }
                }
                unlock();
            }
        }

        template<class T>
        void remove(T* object)
        {
            auto tag = reinterpret_cast<long>(object);
            remove(tag);
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
    private:
        bool is_locked() const
        {
            return _lock_counter != 0;
        }

        void lock()
        {
            ++_lock_counter;
        }

        void unlock()
        {
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
        int _lock_counter;
        std::map<long, std::function<R(A...)>> _listeners;
        std::map<long, std::function<R(A...)>> _listeners_to_add;
        std::set<long> _listeners_to_remove;
    };
}


#endif
'''

python = '''
class @{name}:

    def __init__(self):
        self._listeners = {}
        self._add = {}
        self._remove = []
        self._locked = 0

    def _is_locked(self):
        return self._locked != 0

    def _lock(self):
        self._locked += 1

    def _unlock(self):
        self._locked -= 1
        if not self._is_locked():
            for object in self._add:
                self._listeners[object] = self._add[object]
            for object in self._remove:
                del self._listeners[object]
            self._add = {}
            self._remove = []

    def _call(self, object, func, *args):
        def isclass(obj):
            return str(type(obj)) == "<type 'instance'>"

        if isclass(object):
            func(object, *args)
        else:
            func(*args)

    def add(self, object, functor):
        if self._is_locked():
            if object in self._remove:
                self._remove.remove(object)
            else:
                self._add[object] = functor
        else:
            self._listeners[object] = functor

    def remove(self, object):
        if self._is_locked():
            self._remove.append(object)
        else:
            del self._listeners[object]

    def notify(self, *args):
        self._lock()
        for object in self._listeners:
            if object not in self._remove:
                self._call(object, self._listeners[object], *args)
        self._unlock()
'''

php = '''<?php
//TODO
?>
'''


class ObserverPatterGenerator:

    @staticmethod
    def get_observable_name():
        return 'Observable'

    @staticmethod
    def get_mock():
        cls = Class()
        cls.name = ObserverPatterGenerator.get_observable_name()
        cls.type = 'class'
        cls.auto_generated = False
        return cls

    @staticmethod
    def generate(language, writer):
        dictionary = {
            'cpp': cpp,
            'py': python,
            'php': php,
        }
        files = {
            'cpp': ObserverPatterGenerator.get_observable_name() + '.h',
            'py': ObserverPatterGenerator.get_observable_name() + '.py',
            'php': ObserverPatterGenerator.get_observable_name() + '.php',
        }
        text = dictionary[language]
        filename = files[language]
        if language == 'cpp':
            text = text.replace('@{namespace}', writer.namespace)
        text = text.replace('@{name}', ObserverPatterGenerator.get_observable_name())
        writer.save_file(filename, text)
