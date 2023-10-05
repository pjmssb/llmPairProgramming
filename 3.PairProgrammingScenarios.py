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
#prompt_template = """
#Can you please simplify this code for a linked list in Python? You are an expert on Pythonic code.

#{question}

#Please, comment each line in detail. Explain in detail what you did to modify it, and why.
#"""

#prompt_template = """
#Can you please create test cases in code for this Python code?

#{question}

#Explain in detail what these test cases are designed to achieve.
#"""


#prompt_template = """
#Can you please make this code more efficient?

#{question}

#Explain in detail what you changed and why.
#"""

prompt_template = """
Can you please help me to debug this code?

{question}

Explain in detail what you found and why it was a bug.
"""



#question = """
#def func_x(array)
#  for i in range(len(array)):
#    print(array[i])
#"""

# I deliberately introduced a bug into this code! Let's see if the LLM can find it.
# Note -- the model can't see this comment -- but the bug is in the
# print function. There's a circumstance where nodes can be null, and trying
# to print them would give a null error.
question = """
class Node:
   def __init__(self, data):
      self.data = data
      self.next = None
      self.prev = None

class doubly_linked_list:
   def __init__(self):
      self.head = None

# Adding data elements
   def push(self, NewVal):
      NewNode = Node(NewVal)
      NewNode.next = self.head
      if self.head is not None:
         self.head.prev = NewNode
      self.head = NewNode

# Print the Doubly Linked list in order
   def listprint(self, node):
       print(node.data),
       last = node
       node = node.next

dllist = doubly_linked_list()
dllist.push(12)
dllist.push(8)
dllist.push(62)
dllist.listprint(dllist.head)

"""



completion = generate_text(
    prompt = prompt_template.format(question=question),
    temperature = 0.0
)
print(completion.result)