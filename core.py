import os

# for linux = /
# for windows = c:\\
class Core:
    def root_path():
        return os.path.abspath(os.sep)

    def os_join(*strings):
        path = Core.root_path()
        for string in strings:
            path = os.path.join(path,string)
        return path

'''
        def greet(*names):
...     for name in names:
...         print("Hello", name)
'''