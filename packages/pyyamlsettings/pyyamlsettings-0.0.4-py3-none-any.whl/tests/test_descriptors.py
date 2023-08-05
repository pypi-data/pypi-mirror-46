'''
Test that our descriptors are operating correctly
'''
import pytest
from pyyamlsettings import descriptors, errors

class TestDescriptors(object):
    ''' There is only the one descriptor to test: YamlFilePath '''
    yaml_file_path = descriptors.YamlFilePath()

    def test_must_be_string(self):
        ''' the path passed must be of the type string '''
        with pytest.raises(errors.YamlFilePathTypeError):
            self.yaml_file_path = 42

    def test_must_be_yaml(self):
        ''' the file path must end with '.yaml' '''
        with pytest.raises(errors.NotAYamlFileError):
            self.yaml_file_path = "doesnt_end_with_yaml.txt"

    def test_file_must_exist(self):
        ''' the file path must point to an existing file '''
        with pytest.raises(errors.YamlFileMustExistError):
            self.yaml_file_path = "file_doesnt_exist.yaml"
        