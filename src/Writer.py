import fileutils


def add_dict(inDict, toDict):
    for key in toDict:
        if key in inDict:
            inDict[key] += toDict[key]
        else:
            inDict[key] = toDict[key]
    return inDict


class Writer:
    def __init__(self, outDirectory, parser):
        self.parser = parser
        self.buffers = {}
        self.out_directory = outDirectory
        self.created_files = []

        self.buffers = add_dict(self.buffers, self.write_classes(parser.classes, 0))
        return

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
        out = {flags: '\n'}
        for class_ in classes:
            dictionary = self.write_class(class_, flags)
            self.save_file(self._get_filename_of_class(class_), dictionary[flags])
            out = add_dict(out, dictionary)
        return out

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

    def save_config_file(self, content):
        pattern = '#ifndef __mg_Config_h__\n#define __mg_Config_h__\n\n{}\n\n#endif //#ifndef __mg_Config_h__'
        configs = list()
        configs.append('#define MG_JSON 1')
        configs.append('#define MG_XML 2')
        configs.append('\n#define MG_SERIALIZE_FORMAT MG_' + content.upper())
        self.save_file('config.h', pattern.format('\n'.join(configs)))

    def _get_filename_of_class(self, class_):
        return class_.name

    def create_data_storage(self):
        pass
