Simple using:

'''
cd src
python main.py
'''

configs directory - configs/
out directory - out/
python library src directory - src/


Configured launch:

python src/main.py -o out -i config -incremental yes -t no -side both -f xml
Parameters:
	-o - path to out directory
	-i - path to configs directory
	-incremental - yes/no - rewrite/no rewrite not modified classes
	-side - both/client/server - used for different code
	-t - yes/no - generate tests (not worked no :( )
	-f xml/json - serialization type


Синтаксис:

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

**function int getCurrentType():const

{

    return current_time;

}**

Функция с явным определением. Тело функций не подвергается изменению и в конечный класс помещается "как есть", за исключением простого форматирования.