import os


def create_package(path):
    if not os.path.exists(path):
        os.makedirs(path)
    create_module(path)


def create_module(path, name='__init__', content=''):
    file = os.path.join(path, f'{name}.py')
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(content)
