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

models = [m for m in palm.list_models( ) if "generateText" in m.supported_generation_methods]

model_bison = models[0]
print (model_bison)

from google.api_core import retry
@retry.Retry()
def generate_text(prompt, 
                  model=model_bison, 
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)