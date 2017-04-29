import os
import hashlib
from os.path import isfile, join, isdir
import tempfile


def _get_files_list(path, prefix):
    try:
        list = os.listdir(path)
        listFiles = []
        for i in list:
            if isdir(path + i):
                result = _get_files_list(path + i + '/', prefix + i + '/')
                for r in result:
                    listFiles.append(r)
            if isfile(path + i):
                listFiles.append(prefix + i)
        return listFiles
    except IOError:
        return []


def get_files_list(path):
    return _get_files_list(path, '')


def create_dir_for_file(file):
    dir = file
    k = dir.rindex('/')
    dir = dir[:k]
    if not os.path.exists(dir):
        os.makedirs(dir)


def remove(file):
    if os.path.exists(file):
        os.remove(file)


def load_dict(path):
    dictionary = {}
    try:
        file = open(path)
        for line in file:
            str = line.strip()
            args = str.split(' ')
            if len(args) == 2:
                key = str.split(' ')[0]
                value = str.split(' ')[1]
                dictionary[key] = value
        return dictionary
    except IOError:
        return dictionary


def save_dict(path, dict):
    try:
        dictionary = load_dict(path)
        for key in dict:
            dictionary[key] = dict[key]
        file = open(path, 'w')
        for key in dictionary:
            value = dictionary[key]
            str = key + ' ' + dictionary[key] + "\n"
            file.write(str)
    except IOError:
        return False
    return True


def write(path, buffer):
    rewrite = True
    if os.path.exists(path):
        rewrite = open(path).read() != buffer
    if rewrite:
        create_dir_for_file(path)
        open(path, 'w').write(buffer)
    return rewrite


_cache_file = tempfile.gettempdir() + '/bin/cache.tmp'


def isFileChanges(file):
    dict = load_dict(_cache_file)
    if file in dict:
        cache = dict[file]

        m = hashlib.md5()
        m.update(open(file).read())
        return not cache == str(m.hexdigest())
    return True


def saveMd5ToCache(file):
    create_dir_for_file(_cache_file)
    m = hashlib.md5()
    m.update(open(file).read())
    save_dict(_cache_file, {file: m.hexdigest()})
