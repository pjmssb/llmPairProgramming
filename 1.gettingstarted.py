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


from google.api_core import retry
import json
@retry.Retry()  
def generate_text(prompt, model=model_bison, temperature=0.2):
    """
    Generate text using a model.
    """
    return palm.generate_text(prompt=prompt, model=model, temperature=temperature)

prompt = "Write code Python for a Windows PC to encrypt a string with a quantum resistant algorithm ."

completion = generate_text(prompt)
print(completion.result)