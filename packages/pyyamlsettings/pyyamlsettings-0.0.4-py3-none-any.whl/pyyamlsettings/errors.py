'''
Defines errors for the yamlsettings package
'''

class YamlSettingsError(Exception):
    ''' Base-class for all exceptions raised by this package '''


class YamlFilePathTypeError(YamlSettingsError):
    ''' All yaml file paths must be of the type str  '''
    def __init__(self):
        super(YamlFilePathTypeError, self).__init__("All yaml file paths must be of the type str!")


class NotAYamlFileError(YamlSettingsError):
    ''' The file path must end with '.yaml'  '''
    def __init__(self):
        super(NotAYamlFileError, self).__init__("the file path provide must end with '.yaml'!")


class YamlFileMustExistError(YamlSettingsError):
    ''' The file path provided must point to an existing file '''
    def __init__(self):
        super(YamlFileMustExistError, self).__init__("The provided yaml file must exist!")


class AttributeDoesntExistError(YamlSettingsError):
    ''' Raise if the requested attribute doesn't exist in our yaml file '''
    def __init__(self):
        super(AttributeDoesntExistError, self).__init__("Requested yaml attribute does not exist!")
