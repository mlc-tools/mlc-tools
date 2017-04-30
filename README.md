[![Build status](https://ci.appveyor.com/api/projects/status/t5sp7poff0ygygw5/branch/master?svg=true)](https://ci.appveyor.com/project/Volodar/tools-mlc/branch/master)

### Simple using: ###


```
#!shell
cd src
python main.py
```

Configs directory - *configs/*

Out directory - *out/*

Python library src directory - *src/*


### Configured launch: ###

```
#!shell
python src/main.py -o out -i config -incremental yes -t no -side both -f xml
```

**Parameters:**

	-o - path to out directory

	-i - path to configs directory

	-incremental - yes/no - rewrite/no rewrite not modified classes

	-side - both/client/server - used for different code

	-f xml/json - serialization type


### Синтаксис: ###

```
#!cpp
class core/CommandBase<SerializedObject>
{
	int user_id:key = 0
	int current_time = 0
	function string getSerializedString():external:const;
	function int getCurrentType():const
	{
	    return current_time;
	}
}
```

**class** - служебное слово, указывает, что начинается описание класса

**core/** - модуль. Используется только для группировки классов по папкам

**CommandBase** - имя класса

**<SerializedObject>** - наследуемый класс. Множественное наследование не поддерживается.

**{ ... }** - тело класса или функции-метода

**int user_id:key** = 0  -  поле класса user_id целочисленного типа.

                        Модификатор ':key' указывает на постоянный инкремент этого поля при сохдании новых объектов класса

**int current_time** = 0 - целочисленное поле класса с инициализацией нолем

**function string getSerializedString():external:const** - метод класса:

                        function - служебное слово, указывает, что начинается описание метода

                        string - возвращаемый тип

                        getSerializedString - имя метода

                        :external - модификатор указывает, что у метода есть внешнее определение

                        :const - модификатор указывает на константность метода

```
#!cpp
function int getCurrentType():const
{
    return current_time;
}
```

Функция с явным определением. Тело функций не подвергается изменению и в конечный класс помещается "как есть", за исключением простого форматирования.