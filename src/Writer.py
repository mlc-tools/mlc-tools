import fileutils


def add_dict(inDict, toDict):
    for key in toDict:
        if key in inDict:
            inDict[key] += toDict[key]
        else:
            inDict[key] = toDict[key]
    return inDict


class Writer:

    def __init__(self, parser, serialize_format):
        self.parser = parser
        self.created_files = []
        self.simple_types = parser.simple_types
        self.serialize_format = serialize_format
        self.serialize_protocol = self.parser.serialize_protocol
        self.files = {}

    def generate(self):
        self.write_classes(self.parser.classes, 0)

    def write_object(self, object_, flags):
        return {flags: ""}

    def write_class(self, class_, flags):
        return {flags: ""}

    def write_function(self, function, flags):
        return {flags: ""}

    def write_objects(self, objects, flags):
        out = {flags: '\n'}
        for object_ in objects:
            out = add_dict(out, self.write_object(object_, flags))
        return out

    def write_classes(self, classes, flags):
        for class_ in classes:
            dictionary = self.write_class(class_, flags)
            filepath = self._get_filename_of_class(class_)
            self.files[filepath] = dictionary[flags]

    def write_functions(self, functions, flags):
        out = ''
        for function in functions:
            out += self.write_function(function, flags)
        return out

    def prepare_file(self, body):
        return body

    def save_file(self, filename, string):
        string = self.parser.copyright_text + self.prepare_file(string)
        filename = self.out_directory + filename
        self.created_files.append(filename)
        exist = fileutils.isfile(filename)
        if fileutils.write(filename, string):
            msg = 'create:' if not exist else 'rewrited'
            print msg, filename

    def remove_non_actual_files(self):
        if not fileutils.isdir(self.out_directory):
            return
        files = fileutils.get_files_list(self.out_directory)
        for filename in files:
            if self.out_directory + filename not in self.created_files:
                if not filename.endswith('.pyc'):
                    print 'remove', filename
                fileutils.remove(self.out_directory + filename)

    def save_generated_classes(self, out_directory):
        self.out_directory = out_directory
        for file in self.files:
            self.save_file(file, self.files[file])

    def save_config_file(self):
        pattern = '#ifndef __mg_Config_h__\n#define __mg_Config_h__\n\n{}\n\n#endif //#ifndef __mg_Config_h__'
        configs = list()
        configs.append('#define MG_JSON 1')
        configs.append('#define MG_XML 2')
        configs.append('\n#define MG_SERIALIZE_FORMAT MG_' + self.serialize_format.upper())
        self.save_file('config.h', pattern.format('\n'.join(configs)))

    def _get_filename_of_class(self, class_):
        return class_.name

    def create_data_storage(self):
        pass
