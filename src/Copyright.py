from os.path import isfile


class Copyright():
    def __init__(self, configs_path):
        self.text = ''

        file = configs_path + 'copyright.txt'
        if isfile(file):
            self.text = open(file).read()
            self.text += '\n'
