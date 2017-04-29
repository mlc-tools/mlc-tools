from WriterPython import WriterPython
from WriterPython import SERIALIZATION
from WriterPython import DESERIALIZATION
from Object import Object
from Class import Class


class WriterPySerializationJson(WriterPython):
    def __init__(self, outDirectory, parser, generateTests, configsDirectory):
        WriterPython.__init__(self, outDirectory, parser, generateTests, configsDirectory)

    def create_serialization_patterns(self):
        self.simple_types = ["int", "float", "bool", "string", "cc.point"]

        self.serialize_formats = []
        self.serialize_formats.append({})
        self.serialize_formats.append({})
        
        self.serialize_formats[SERIALIZATION]['simple'] = []
        self.serialize_formats[SERIALIZATION]['simple'].append( 'if {4}{0} != {2}: dictionary["{0}"] = {4}{0}' )
        self.serialize_formats[SERIALIZATION]['simple'].append( 'dictionary["{0}"] = {4}{0}' )
        self.serialize_formats[DESERIALIZATION]['simple'] = []
        self.serialize_formats[DESERIALIZATION]['simple'].append( 'if "{0}" in dictionary: {4}{0} = dictionary["{0}"]' )
        self.serialize_formats[DESERIALIZATION]['simple'].append( '{4}{0} = dictionary["{0}"]' )

        self.serialize_formats[SERIALIZATION]['pointer'] = []
        self.serialize_formats[SERIALIZATION]['pointer'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[SERIALIZATION]['pointer'].append( '''
        if {4}{0}:
            dictionary['{0}'] = {3}
            dictionary['{0}'][{4}{0}.get_type()] = {3}
            {4}{0}.serialize(dictionary['{0}'][{4}{0}.get_type()])''' )
        self.serialize_formats[DESERIALIZATION]['pointer'] = []
        self.serialize_formats[DESERIALIZATION]['pointer'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[DESERIALIZATION]['pointer'].append( '''
        if '{0}' in dictionary:
            for key, value in dictionary['{0}'].iteritems():
                {4}{0} = Factory.Factory.build( key );
                {4}{0}.deserialize( value ) 
                break''')

        self.serialize_formats[SERIALIZATION]['list<simple>'] = []
        self.serialize_formats[SERIALIZATION]['list<simple>'].append( '''
        arr_{0} = []
        for obj in {4}{0}:
            arr_{0}.append(obj)
        dictionary['{0}'] = arr_{0}
''' )
        self.serialize_formats[SERIALIZATION]['list<simple>'].append( self.serialize_formats[SERIALIZATION]['list<simple>'][0] )
        self.serialize_formats[DESERIALIZATION]['list<simple>'] = []
        self.serialize_formats[DESERIALIZATION]['list<simple>'].append( '''
        arr_{0} = dictionary['{0}']
        for obj in arr_{0}:
            {4}{0}.append(obj)
''' )
        self.serialize_formats[DESERIALIZATION]['list<simple>'].append( self.serialize_formats[DESERIALIZATION]['list<simple>'][0] )

        self.serialize_formats[SERIALIZATION]['list<serialized>'] = []
        self.serialize_formats[SERIALIZATION]['list<serialized>'].append( '''
        arr_{0} = []
        for obj in {4}{0}:
            dict = {3}
            obj.serialize(dict)
            arr_{0}.append(dict)
        dictionary['{0}'] = arr_{0}
''' )
        self.serialize_formats[SERIALIZATION]['list<serialized>'].append( self.serialize_formats[SERIALIZATION]['list<serialized>'][0] )
        self.serialize_formats[DESERIALIZATION]['list<serialized>'] = []
        self.serialize_formats[DESERIALIZATION]['list<serialized>'].append( '''
        arr_{0} = dictionary['{0}']
        for dict in arr_{0}:
            obj = {1}()
            obj.deserialize(dict)
            {4}{0}.append(obj)
''' )
        self.serialize_formats[DESERIALIZATION]['list<serialized>'].append( self.serialize_formats[DESERIALIZATION]['list<serialized>'][0] )

        self.serialize_formats[SERIALIZATION]['serialized'] = []
        self.serialize_formats[SERIALIZATION]['serialized'].append( '''if {4}{0} != None: 
            dict = {3}
            {4}{0}.serialize(dict)
            dictionary["{0}"] = dict
''' )
        self.serialize_formats[SERIALIZATION]['serialized'].append( self.serialize_formats[SERIALIZATION]['serialized'][0] )
        self.serialize_formats[DESERIALIZATION]['serialized'] = []
        self.serialize_formats[DESERIALIZATION]['serialized'].append( '''
        if '{0}' in dictionary:
            {4}{0} = {1}()
            {4}{0}.deserialize(dictionary['{0}'])''' )
        self.serialize_formats[DESERIALIZATION]['serialized'].append( self.serialize_formats[DESERIALIZATION]['serialized'][0] )

        self.serialize_formats[SERIALIZATION]['pointer_list'] = []
        self.serialize_formats[SERIALIZATION]['pointer_list'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[SERIALIZATION]['pointer_list'].append( '''
        dictionary['{0}'] = []
        arr = dictionary['{0}']
        for t in {4}{0}:
            arr.append({3})
            arr[-1][t.get_type()] = {3}
            t.serialize(arr[-1][t.get_type()])    ''' )
        self.serialize_formats[DESERIALIZATION]['pointer_list'] = []
        self.serialize_formats[DESERIALIZATION]['pointer_list'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[DESERIALIZATION]['pointer_list'].append( '''
        arr = dictionary['{0}']
        size = len(arr)
        for index in xrange(size):
            for key, value in arr[index].iteritems():
                obj = Factory.Factory.build( key )
                {4}{0}.append(obj)
                {4}{0}[-1].deserialize( arr[index][key] )
                break ''' )

    def getSerialiationFunctionArgs(self):
        return '(self, dictionary)'

    def getPatternFile(self):
        return '''import json
import Factory
{3}

class {0}:
    def __init__(self):
{4}
{1}
        return

    def get_type(self):
        return self.__type__

{2}    
'''
    def getPatternFactoryFile(self):
        return '''import json
{0}

class Factory:
    def __init__(self):
        return

    @staticmethod
    def build(type):
{1}
        return None

    @staticmethod
    def create_command(string):
        dictionary = json.loads(string)
        type = dictionary["command"]["type"]
        command = Factory.build(type)
        if command != None:
            command.deserialize(dictionary)
        return command
'''
    def getPatternSerializationMap(self):
        return '''
        dict_cach = dictionary
        arr = []
        dictionary['{0}'] = arr
        for key, value in self.{0}.iteritems():
            arr.append({3})
            dictionary = arr[-1]
{1}
{2}
        dictionary = dict_cach
'''    

    def getPatternDeserializationMap(self):
        return '''
        dict_cach = dictionary
        arr = dictionary['{0}']
        for dict in arr:
            key = dict['key']
            type = key
            dictionary = dict
{2}
            self.{0}[type] = _value
        dictionary = dict_cach
'''