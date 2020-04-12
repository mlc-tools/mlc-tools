

def add(var, filename):
    text = open(filename).read()
    text = text.replace('tests.test_serializer.py.gen', '')
    text = text.replace('tests.test_serializer.py', '')
    return '\n\n{} = """{}"""'.format(var, text)


content = ''
content += add('META', 'Meta.py')
content += add('DATA_WRAPPER', 'gen/DataWrapper.py')
content += add('INTRUSIVE', 'gen/IntrusivePtr.py')
content += add('SERIALIZER_XML', 'SerializerXml.py')
content += add('DESERIALIZER_XML', 'DeserializerXml.py')
content += add('SERIALIZER_JSON', 'SerializerJson.py')
content += add('DESERIALIZER_JSON', 'DeserializerJson.py')
open('../../../mlc_tools/module_python/constants_serializers.py', 'w').write(content)
