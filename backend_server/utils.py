import os
from my_settings import *
# Copy and paste your OpenAI API Key
openai_api_key = openai_key
# Put your name
key_owner = "WH"

fs_storage = "storage"
fs_temp_storage = "temp_storage"


is_ubuntu_server = os.getenv('IS_UBUNTU_SERVER', False)
if is_ubuntu_server:
    fs_storage = "/home/ubuntu/BE_server/backend_server/storage"
    game_storage = "/home/ubuntu/BE_server/backend_server/pickles"
else:
    fs_storage = "./storage" #TODO:storage 유저별 분리..
    game_storage = "./pickles"       

# Verbose 
debug = True