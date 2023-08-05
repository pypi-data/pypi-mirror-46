import os


def create_package(path):
    if not os.path.exists(path):
        os.makedirs(path)
    create_module(path)


def create_module(path, name=None, content=None):
    name = name if name is not None else '__init__'
    file = os.path.join(path, f'{name}.py')
    content = content if content is not None else ''
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(content)
