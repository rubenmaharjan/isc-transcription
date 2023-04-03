import xml.etree.ElementTree as ET


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
        if element is not None:
            return element.text
        else:
            return None

    def set(self, key, value):
        """
        Set the value for the specified key in the configuration file.

        """
        element = self.root.find(key)
        if element is not None:
            element.text = value
            return True
        else:
            return False

    def get_all(self):
        """
        Get all key-value pairs in the configuration file.

        :return: A dictionary containing all key-value pairs in the configuration file.
        """
        result = {}
        for child in self.root:
            if child.tag == "settings":
                for subchild in child:
                    result[f"{child.tag}/{subchild.tag}"] = subchild.text
            else:
                result[child.tag] = child.text
        return result

    def delete_key(self, key):
        """
        Delete a particular key from the configuration file.

        :param key: The key to delete.
        :return: True if the key was successfully deleted, False otherwise.
        """
        element = self.root.find(key)
        if element is not None:
            parent = self.root.find('.'.join(key.split('/')[:-1]))
            parent.remove(element)
            return True
        else:
            return False

    def create_key(self, key, value):
        """
        Create a new key-value pair in the configuration file.

        :param key: The name of the key in the format 'parent/child' or 'key' if it has no parent 
        """
        parts = key.split("/")
        if len(parts) == 1:
            element = ET.Element(key)
            element.text = value
            self.root.append(element)
        elif len(parts) == 2:
            parent, child = parts
            for element in self.root.findall(parent):
                if element.tag == parent:
                    if parent.find(child) is None:
                        subelement = ET.SubElement(element, child)
                        subelement.text = value
                        break
                    break

    def set_settings(self, model=None, verbosity=None):
        """
        Set multiple settings at once.

        :param model: The new value of the model type.
        :param verbosity: The new value of the verbosity setting.
        :return: True if all settings were successfully set, False otherwise.
        """
        success = True
        if model is not None:
            success &= self.set("settings/model", model)
        if verbosity is not None:
            success &= self.set("settings/verbosity", str(verbosity).lower())
        return success

    def save_changes(self):
        """
        Save any changes made to the XML configuration file.

        """
        self.tree.write(self.file_path)

    def delete_file(self):
        """
        Delete the XML configuration file.

        """
        import os
        os.remove(self.file_path)
