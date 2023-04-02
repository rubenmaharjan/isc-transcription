import os

def traverse_directory(path):
    if not os.path.exists(path):
        print("Directory does not exist:", path)
        return
    
    # Loop through all the files and folders in the directory
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        
        # If it's a directory, recursively call the function to traverse that directory
        if os.path.isdir(file_path):
            traverse_directory(file_path)
        
        # If it's an audio file
        elif file_path.endswith(('.mp3', '.wav')):
            # Process audio file
            print("Processing audio file:", file_path)