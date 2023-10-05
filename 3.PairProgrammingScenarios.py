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


#prompt_template = """
#I don't think this is the best way to do it in Python, can you help me?
#{question}
#Please explain in detail, what you did to improve it
#"""

#prompt_template = """
#I don't think this code is the best way to do it in Python, can you help me?

#{question}

#Please explore multiple ways of solving the problem, and explain each.
#"""



#prompt_template = """
#I don't think this code is the best way to do it in Python, can you help me?

#{question}

#Please explore multiple ways of solving the problem, 
#and tell me which is the most Pythonic
#"""

# option 1
prompt_template = """
Can you please simplify this code for a linked list in Python?

{question}

Explain in detail what you did to modify it, and why.
"""

question = """
def func_x(array)
  for i in range(len(array)):
    print(array[i])
"""



completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print(completion.result)