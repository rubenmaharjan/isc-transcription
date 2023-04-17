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
        # print('constructing TranscriptionConfig: file_path', file_path)
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def get(self, key):
        """
        Get the value for the specified key in the configuration file.

        """
        element = self.root.find(key)
        try:
            logger.info(f'{element}')
            return element.text
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
                # If the key has no parent, update the text attribute of the root element
                self.root.text = value
                logger.info(f'Set value of root element to: {value}')
            elif len(parts) > 1:
                # Traverse the tree to find the element with the specified key
                parent = self.root
                for part in parts[:-1]:
                    # Find the child element with the specified tag name
                    child = parent.find(part)
                    if child is None:
                        # If the child element doesn't exist, return False
                        logger.error(f"No such key: {key}")
                        return False
                    # Update the parent element to be the child element
                    parent = child
                # Update the text attribute of the element with the specified key
                element = parent.find(parts[-1])
                if element is None:
                    # If the element doesn't exist, create a new one
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

        :return: A dictionary containing all key-value pairs in the configuration file.
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
            logger.error(
                f'Error while getting all key-value pairs in configuration file: {e}')
            return False

    def delete_key(self, key):
        """
        Delete a particular key from the configuration file.

        :param key: The key to delete.
        :return: True if the key was successfully deleted, False otherwise.
        """
        try:
            if '/' in key:
                # Split the key into a list of nested tags
                nested_tags = key.split('/')
                # Find the parent element of the key
                parent = self.root.find('/'.join(nested_tags[:-1]))
                # Find the element to be deleted
                element = parent.find(nested_tags[-1])
                # Remove the element
                parent.remove(element)
            else:
                # Find the element to be deleted
                element = self.root.find(key)
                # Remove the element
                self.root.remove(element)
            logger.critical(f'Key: {key} has been deleted.')
            return True
        except Exception as e:
            logger.error(
                f'Error while deleting key in configuration file: {str(e)}')
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
                # Create a new element with the specified key and value
                element = ET.Element(key)
                element.text = value
                # Append the new element to the root element of the tree
                self.root.append(element)
                logger.info(f'Created element: {element}')
            elif len(parts) > 1:
                # Traverse the tree to find the parent element of the new key
                parent = self.root
                for part in parts[:-1]:
                    # Find the child element with the specified tag name
                    child = parent.find(part)
                    if child is None:
                        # If the child element doesn't exist, create a new one
                        child = ET.Element(part)
                        # Append the new child element to the parent element
                        parent.append(child)
                    # Update the parent element to be the child element
                    parent = child
                # Create a new element with the specified key and value
                element = ET.Element(parts[-1])
                element.text = value
                # Append the new element to the parent element
                parent.append(element)
                logger.info(f'Created key: {key}')
            return True
        except Exception as e:
            logger.error(
                f"Failed to create key-value pair in configuration file: {e}")
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
