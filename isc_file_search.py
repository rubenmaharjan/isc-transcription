import os

class IscFileSearch:
    def __init__(self, path):
        self.path = path
        
    def traverse_directory(self):
        """
        Recursively traverses a directory and returns a list of file paths for all
        files that end with .mp3 or .wav.
        """
        if not os.path.exists(self.path):
            print("Directory does not exist:", self.path)
            return []

        file_paths = []
        
        for file_name in os.listdir(self.path):
            file_path = os.path.join(self.path, file_name)
            
            if os.path.isdir(file_path):
                subdir = IscFileSearch(file_path)
                file_paths.extend(subdir.traverse_directory())
                
            elif os.path.isfile(file_path):
                if file_path.lower().endswith(('.mp3', '.wav')):
                    file_paths.append(file_path)
                
        return file_paths
    
    def get_file(self):
        """
        Returns the path of the first file found in the directory that ends with .mp3 or .wav.
        """
        if not os.path.exists(self.path):
            print("Directory does not exist:", self.path)
            return None
        
        for file_name in os.listdir(self.path):
            file_path = os.path.join(self.path, file_name)
            
            if os.path.isfile(file_path) and file_path.lower().endswith(('.mp3', '.wav')):
                return file_path
            
        print("No files found in directory:", self.path)
        return None
    
    def delete_file(self, file_path):
        """
        Deletes a file at the specified path.
        """
        if not os.path.exists(file_path):
            print("File does not exist:", file_path)
            return
        
        os.remove(file_path)
        print("File deleted:", file_path)
    
    def rename_file(self, old_name, new_name):
        """
        Renames a file in the directory from old_name to new_name.
        """
        old_path = os.path.join(self.path, old_name)
        new_path = os.path.join(self.path, new_name)
        
        if not os.path.exists(old_path):
            print("File does not exist:", old_path)
            return
        
        os.rename(old_path, new_path)
        print("File renamed from", old_name, "to", new_name)
    
    def get_file_properties(self, file_path):
        """
        Returns a dictionary of properties for the file at the specified path, including
        file name, file size, creation time, modified time, and access time.
        """
        if not os.path.exists(file_path):
            print("File does not exist:", file_path)
            return None
        
        file_stats = os.stat(file_path)
        
        properties = {
            "file_name": os.path.basename(file_path),
            "file_size": file_stats.st_size,
            "creation_time": file_stats.st_ctime,
            "modified_time": file_stats.st_mtime,
            "access_time": file_stats.st_atime,
        }
        
        return properties