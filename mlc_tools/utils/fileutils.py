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


def get_change_time_of_file(path: str):
    return os.path.getmtime(path) if os.path.isfile(path) else 0
