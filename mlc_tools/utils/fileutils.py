import os
import hashlib
import tempfile


def _get_files_list(path, prefix):
    try:
        files = os.listdir(path)
        result_files = []
        for i in files:
            if os.path.isdir(path + i):
                result = _get_files_list(path + i + '/', prefix + i + '/')
                for filename in result:
                    result_files.append(filename)
            if os.path.isfile(path + i):
                result_files.append(prefix + i)
        return result_files
    except IOError:
        return []
    except OSError as exception:
        print('Exception in [_get_files_list]:', exception, path, prefix)
        return []


def get_files_list(path):
    return _get_files_list(path, '')


def create_dir_for_file(filename):
    path = filename
    k = path.rindex('/')
    path = path[:k]
    if not os.path.exists(path):
        os.makedirs(path)


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def normalize_path(path, append_slash=True):
    path = path.replace('\\', '/')
    if append_slash and path and not path.endswith('/'):
        path += '/'
    return path


def load_dict(path):
    dictionary = {}
    try:
        file_ = open(path)
        for line in file_:
            string = line.strip()
            args = string.split(' ')
            if len(args) == 2:
                key = string.split(' ')[0]
                value = string.split(' ')[1]
                dictionary[key] = value
        return dictionary
    except IOError:
        return dictionary


def save_dict(path, dict_):
    try:
        dictionary = load_dict(path)
        for key in dict_:
            dictionary[key] = dict_[key]
        with open(path, 'w') as stream:
            for key in dictionary:
                string = key + ' ' + dictionary[key] + '\n'
                stream.write(string)
    except IOError:
        return False
    return True


def write(path, content):
    rewrite = True
    if os.path.exists(path):
        with open(path) as stream:
            rewrite = stream.read() != content
    if rewrite:
        create_dir_for_file(path)
        with open(path, 'w') as stream:
            stream.write(content)
            return True, stream
    return False, None


__CACHE_FILES = tempfile.gettempdir() + '/bin/cache.tmp'


def file_has_changes(path):
    dictionary = load_dict(__CACHE_FILES)
    if path in dictionary:
        cache = dictionary[path]

        md5 = hashlib.md5()
        md5.update(open(path).read())
        return not cache == str(md5.hexdigest())
    return True


def save_md5_to_cache(path):
    create_dir_for_file(__CACHE_FILES)
    md5 = hashlib.md5()
    md5.update(open(path).read())
    save_dict(__CACHE_FILES, {path: md5.hexdigest()})
