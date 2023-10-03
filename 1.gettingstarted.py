import os
import sys

sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


import google.generativeai as palm
from google.api_core import client_options as client_options_lib


palm.configure(
    api_key = os.environ['PALM_API_KEY']
)

for m in palm.list_models( ):
    print(f"name: {m.name}")
    print(f"description: {m.description}")
    print(f"generation_methods: {m.supported_generation_methods}")
    print("---------------------------------------------------------------------------\n\n")

models = [m for m in palm.list_models( ) if "generateText" in m.supported_generation_methods]

model_bison = models[0]
print (model_bison)
