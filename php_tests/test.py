import os
path = os.path.dirname(os.path.abspath(__file__))

print 'run tests:'
os.system('php {}/{}'.format(path, 'test.php'))