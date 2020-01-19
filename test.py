import importlib
if __name__ == "__main__":
    module = importlib.import_module('tests.application')
    for attr in dir(module):
        if attr.startswith('__'):
            continue
        fn = getattr(module, attr)
        print(fn)