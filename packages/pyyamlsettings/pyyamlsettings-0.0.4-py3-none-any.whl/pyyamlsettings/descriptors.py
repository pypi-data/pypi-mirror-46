'''
Defines descriptors for the yamlsettings package
'''

import os
from weakref import WeakKeyDictionary
from . import errors


class YamlFilePath(object):
    ''' A descriptor defining a yaml file path. These must:
        -> be of the type str
        -> point to a file that exists
        -> end with the file extension '.yaml'
    '''
    def __init__(self, default=None):
        self.default = default
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        # the path must be a string
        if not isinstance(value, str):
            raise errors.YamlFilePathTypeError

        # end with '.yaml'
        if not value.endswith(".yaml"):
            raise errors.NotAYamlFileError

        # and point to an existing file
        if not os.path.isfile(value):
            raise errors.YamlFileMustExistError
        self.data[instance] = value
