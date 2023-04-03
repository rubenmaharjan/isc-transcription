# main class for configuration file
from TranscriptionConfig import TranscriptionConfig
import os  # to get current working directory

# create a TranscriptionConfig object and read the XML file
path1 = os.getcwd()
# print("Tpath1: ", path1)
path = os.path.join(path1, "src/config_file/mock_data/config.xml")

# print("Path:",path)
config = TranscriptionConfig(path)

# get the value for the 'model' key
model = config.get("settings/model")
print("Model: ", model)

# set the value for the 'verbosity' key
config.set("settings/verbosity", "false")

# save the changes to the XML file
config.save_changes()

# read the XML file again to verify the changes
config = TranscriptionConfig(path)
verbosity = config.get("settings/verbosity")
print("Verbosity: ", verbosity)
