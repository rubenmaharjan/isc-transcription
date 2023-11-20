import os
from lxml.etree import ElementTree as ET
import src.utils.helperFunctions as helperFunctions
import logging
from config.DEFAULTS import *

logger = logging.getLogger()

def extract_XML_params(config_file=DEFAULT_XML_PATH):
    """
    Extract parameters from the XML configuration file if path is specified otherwise 
    populate with the default XML path over the default configuration values.

    Parameters:
    - config_file: Path to the XML file.
    """
    config_data = DEFAULT_CONFIGS
    tree, root = None, None
    try:
        tree = ET.parse(config_file)
        root = tree.getroot()
        for child in root:
            if child.tag == "settings":
                for subchild in child:
                    config_data[subchild.tag] = subchild.text
            else:
                config_data[child.tag] = child.text
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
    except Exception as e:
        logger.error(f"Error loading config file: {config_file} - {str(e)}")

    return tree, root, config_data

class TranscriptionConfig:
    """
    A class for reading, editing, deleting, and creating XML configuration files
    for the transcription system.
    """

    def __init__(self):
        """
        Constructor for the TranscriptionConfig class.

        :param file_path: Path to the XML configuration file.
        """
        self.file_path = DEFAULT_XML_PATH
        self.tree, self.root, self.config_data = extract_XML_params(DEFAULT_XML_PATH) # populate the configuration with default values
    
    def set_config_values(self, config_values):
        try:
            self.config_data=config_values;
            return True
        except Exception as e:
            logger.warning('Cannot set configuration values.')
        
    def load_config_values(self):
        """
        Retrieve the value of a configuration key from parsed arguments or default settings.

        Parameters:
        - parsed_args: Configuration arguments received from the command line.
        - key: Argument name used in the command line and the XML configuration.

        Returns:
        - The value of the specified key.
        """
        args = helperFunctions.parse_command_line_args() # parse the command line arguments
        parsed_cmd_args = args if args.audio or args.configxml else self.config_data

        if parsed_cmd_args:
            self.logger.info("Using configuration from the parsed command line arguments.")
            try:
                if parsed_cmd_args.configXML and parsed_cmd_args.configXML is not self.config_data.configXML:
                    parsed_configXML_path = parsed_cmd_args.configXML

                    if not parsed_configXML_path.endswith('.xml'):
                        return logger.critical('Invalid file extension. Please provide an XML configuration file.')

                    self.logger.info("Using configuration from the parsed XML file in the command line.")
                    helperFunctions.validate_configxml(parsed_configXML_path, DEFAULT_SCHEMA_FILE)
                    parsed_config_XML = self.extract_XML_params(parsed_configXML_path)
                    self.set_config_values(parsed_config_XML)

            except AttributeError as e:
                logger.error(f"The 'configXML' attribute not found in the parsed arguments. Please provide a valid configuration file. Error: {e}")

        # If parsed_args is None or the key is not found in parsed_args, try loading from the specified self.file_path
        try:
            self.logger.info("Using configuration from the specified XML file.")
            helperFunctions.validate_configxml(self.file_path, DEFAULT_SCHEMA_FILE)
            _, _, config_data = self.load_config(self.file_path)
            self.set_config_values(config_data)

        except Exception as e:
            logger.warning(f"Using default configuration due to an error loading the configuration from the file: {self.file_path}. Error: {e}")

    def get(self, key):
        """
        Get the value for the specified key in the configuration file.
        """
        try:
            return self.config_data.get(key)
        except Exception as e:
            logger.error(f'Could not find element in configuration file: {e}')
            return None

    def set_param(self, key, value):
        """
        Set the value for the specified key in the configuration file.

        :param key: The name of the key in the format 'parent/child' or 'key' if it has no parent.
        :param value: The new value to assign to the key.
        :return: True if the key's value was successfully updated, False otherwise.
        """
        try:
            parts = key.split("/")
            if len(parts) == 1:
                parent = self.root
            elif len(parts) > 1:
                parent = self.root.find('/'.join(parts[:-1]))

            element = parent.find(parts[-1]) if parent is not None else None
            if element is None:
                element = ET.Element(parts[-1])
                parent.append(element)

            element.text = value
            logger.info(f'Set value of key "{key}" to: {value}')
            return True
        except Exception as e:
            logger.error(f'Error while setting element value: {e}')
            return False

    def get_all(self):
        """
        Get all key-value pairs in the configuration file.
        """
        result = {}
        try:
            for child in self.root:
                if child.tag == "settings":
                    for subchild in child:
                        result[f"{child.tag}/{subchild.tag}"] = subchild.text
                else:
                    result[child.tag] = child.text
            return result
        except Exception as e:
            logger.error(f'Error while getting all key-value pairs in configuration file: {e}')
            return False

    def delete_key(self, key):
        """
        Delete a particular key from the configuration file.

        :param key: The key to delete.
        :return: True if the key was successfully deleted, False otherwise.
        """
        try:
            if '/' in key:
                nested_tags = key.split('/')
                parent = self.root.find('/'.join(nested_tags[:-1]))
                element = parent.find(nested_tags[-1]) if parent is not None else None
            else:
                element = self.root.find(key)

            if element is not None:
                parent.remove(element)
                logger.critical(f'Key: {key} has been deleted.')
                return True

            logger.error(f'No such key: {key}')
            return False
        except Exception as e:
            logger.error(f'Error while deleting key in configuration file: {str(e)}')
            return False

    def create_key(self, key, value):
        """
        Create a new key-value pair in the configuration file.

        :param key: The name of the key in the format 'parent/child' or 'key' if it has no parent
        :param value: The value to assign to the key.
        :return: True if the key-value pair was successfully created, False otherwise.
        """
        try:
            parts = key.split("/")
            if len(parts) == 1:
                parent = self.root
            elif len(parts) > 1:
                parent = self.root.find('/'.join(parts[:-1]))

            element = parent.find(parts[-1]) if parent is not None else None
            if element is None:
                element = ET.Element(parts[-1])
                parent.append(element)

            element.text = value
            logger.info(f'Created key: {key}')
            return True
        except Exception as e:
            logger.error(f"Failed to create key-value pair in configuration file: {e}")
            return False

    def set_settings(self, model=None, verbosity=None):
        """
        Set multiple settings at once.

        :param model: The new value of the model type.
        :param verbosity: The new value of the verbosity setting.
        :return: True if all settings were successfully set, False otherwise.
        """
        try:
            if model is not None:
                self.set_param("model", model)
            if verbosity is not None:
                self.set_param("verbosity", str(verbosity).lower())
            return True
        except Exception as e:
            logger.error(f'Error while setting settings: {e}')
            return False

    def save_changes(self):
        """
        Save any changes made to the XML configuration file.
        """
        try:
            logger.info("Saving configuration file...")
            self.tree.write(self.file_path)
            logger.info("Configuration file saved.")
        except Exception as e:
            logger.error(f'Error while saving configuration file:{e}')

    def delete_file(self):
        """
        Delete the XML configuration file.
        """
        try:
            logger.info("Deleting configuration file...")
            os.remove(self.file_path)
            logger.info("Configuration file deleted.")
        except Exception as e:
            logger.error(f'Error while deleting configuration file: {e}')
