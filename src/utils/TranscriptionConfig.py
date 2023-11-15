import xml.etree.ElementTree as ET
import logging
import os

logger = logging.getLogger()


class TranscriptionConfig:
    """
    A class for reading, editing, deleting, and creating XML configuration files
    for the transcription system.
    """

    def __init__(self, file_path):
        """
        Constructor for the TranscriptionConfig class.

        :param file_path: Path to the XML configuration file.
        """
        self.file_path = file_path
        self.tree, self.root, self.config_data = self.load_config(file_path)

    def load_config(self, config_file):
        config_data = {}
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
        except ET.ParseError:
            logger.error(f"Error parsing config file: {config_file}")
        except Exception as e:
            logger.error(f"Error loading config file: {config_file} - {str(e)}")

        return tree, root, config_data

    def get(self, key):
        """
        Get the value for the specified key in the configuration file.
        """
        try:
            return self.config_data.get(key)
        except Exception as e:
            logger.error(f'Could not find element in configuration file: {e}')
            return None

    def set(self, key, value):
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
                self.set("settings/model", model)
            if verbosity is not None:
                self.set("settings/verbosity", str(verbosity).lower())
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
