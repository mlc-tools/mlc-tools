from os.path import isfile


class Copyright:

    def __init__(self, configs_path):
        self.text = ''

        filename = configs_path + 'copyright.txt'
        if isfile(filename):
            self.text = open(filename).read()
            self.text = self.text.strip()
            if self.text:
                self.text += '\n'
