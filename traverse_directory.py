import os
import stat
import time


def traverse_directory(directory, extension):
    """
    Recursively walk a directory tree and print information about files with a given extension.

    Args:
        directory (str): The root directory to start walking from.
        extension (str): The file extension to filter files by.

    Returns:
        None
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    filepath = os.path.join(root, file)
                    try:
                        # Get file stats
                        stats = os.stat(filepath)
                        size = stats.st_size
                        create_time = time.ctime(stats.st_ctime)
                        access_time = time.ctime(stats.st_atime)
                        modify_time = time.ctime(stats.st_mtime)

                        # Print file information
                        print(f"File: {filepath}")
                        print(f"\tSize: {size} bytes")
                        print(f"\tLast accessed: {access_time}")
                        print(f"\tLast modified: {modify_time}\n")
                    except Exception as e:
                        print(f"Error getting information for {filepath}: {e}")
    except Exception as e:
        print(f"Error walking directory {directory}: {e}")
