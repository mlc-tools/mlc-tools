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
    template<class R> class Observable;

    template<class R, class... A>
    class Observable<R(A...)>
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
            if(is_locked())
                _listeners_to_add[tag] = std::bind(method, object, std::forward<P>(placeholders)...);
            else
                _listeners[tag] = std::bind(method, object, std::forward<P>(placeholders)...);
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

        template<class T>
        void remove(T* object)
        {
            remove(get_tag(object));
        }

    private:
        template<class T> typename std::enable_if<std::is_pointer<T>::value, long>::type get_tag(T t)
        {
            return reinterpret_cast<long>(t);
        }
        template<class T> typename std::enable_if<std::is_integral<T>::value, long>::type get_tag(T t)
        {
            return static_cast<long>(t);
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
class Observable{
    private $listeners = array();
    private $objects = array();

    public function add($object, $callback){
        array_push($this->listeners, $callback);
        array_push($this->objects, $object);
    }
    public function remove($object){
        $index = array_search($object, $this->objects);
        if($index !== false){
            unset($this->listeners[$index]);
            unset($this->objects[$index]);
        }
    }
    public function notify(...$arg){
        foreach($this->listeners as $listener){
            $listener(...$arg);
        }
    }
};
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
