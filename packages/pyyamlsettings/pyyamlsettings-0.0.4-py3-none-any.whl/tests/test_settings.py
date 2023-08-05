'''
Here we test several aspects of our YamlSettings class
'''
import os
import pytest
from pyyamlsettings import YamlSettings, errors


class TestYamlSettings(object):
    ''' this class should read / query yaml files and only create
        one instance per file read '''

    def setup_method(self, method):
        ''' create common resources for our tests '''
        dir_path = self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.yaml_file1_path = os.path.join(dir_path, "test_yaml_file1.yaml")
        self.yaml_file2_path = os.path.join(dir_path, "test_yaml_file2.yaml")
        self.settingsObj = YamlSettings(self.yaml_file1_path)

    def teardown_method(self, method):
        ''' and delete them at the end of each run '''
        del self.dir_path
        del self.yaml_file1_path
        del self.yaml_file2_path

    def test_is_flyweight(self):
        ''' test that this is implemented as a Flyweight pattern '''
        obj1A = YamlSettings(self.yaml_file1_path)
        obj1B = YamlSettings(self.yaml_file1_path)
        obj2A = YamlSettings(self.yaml_file2_path)
        obj2B = YamlSettings(self.yaml_file2_path)
        assert id(obj1A) == id(obj1B)
        assert id(obj2A) == id(obj2B)

    def test_file_read(self):
        ''' test that the settings file has been read correctly
            and we have data in a dictionary
        '''
        assert isinstance(self.settingsObj._settings_dict, dict)

    def test_settings_query_no_args(self):
        ''' test the querying of our yaml data with no args (returns all) '''
        result = self.settingsObj.get() # should return the entire dict
        assert result == self.settingsObj._settings_dict

    def test_settings_query_with_args(self):
        ''' we should be able to select attributes with the get_data method '''
        with pytest.raises(errors.AttributeDoesntExistError):
            self.settingsObj.get("not_an_attribute")

        assert self.settingsObj.get_data("att1") == 42
        assert self.settingsObj.get_data("att2") == "This is a string"
        assert self.settingsObj.get_data("level1", "a") == 1
        assert self.settingsObj.get_data("level1", "b") == 2
        assert self.settingsObj.get_data("level1", "level2", "a") == 3
        assert self.settingsObj.get_data("level1", "level2", "b") == 4
        assert self.settingsObj.get_data("level1", "level2", "level3", "a") == 5
        assert self.settingsObj.get_data("level1", "level2", "level3", "b") == 6

    def test_settings_wrong_query(self):
        ''' check that querying the wrong keys / parameters throws an error '''
        with pytest.raises(errors.AttributeDoesntExistError):
            # should be a level2 between 1 and 3
            self.settingsObj.get_data("level1", "level3", "a")

        with pytest.raises(errors.AttributeDoesntExistError):
            # missed specifying level1 first
            self.settingsObj.get_data("level2", "a")

        with pytest.raises(errors.AttributeDoesntExistError):
            # an attribute at level2 that doesnt exist
            self.settingsObj.get_data("level1", "level2", "not_an_attribute")

    def test_settings_not_dict(self):
        ''' when we drill down to a value in a yaml file (say and int of float)
            the user might think there's a dictionary at this location.
            attempts to get key / value pairs in this scenario must throw and error
        '''
        with pytest.raises(errors.AttributeDoesntExistError):
            self.settingsObj.get_data("att1", "level1")
