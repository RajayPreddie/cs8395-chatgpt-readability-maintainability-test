
import os
import json
from collections import defaultdict
from openai import OpenAI
from constants.keywords import KEY_WORDS


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# Function to create 100 unique problem descriptions
def create_problem_descriptions(num_problems=100):
  # Create a list to store the problem descriptions
  problem_descriptions = []
  index = 0
  # Iterate through the number of problems
  while index < num_problems:
      # Create a list to store the keywords
      cur_keywords = []
      cur_keyword =  KEY_WORDS[index % len(KEY_WORDS)]
      cur_keywords.append(cur_keyword)
      
      # Create a problem difficulty
      problem_difficulty = "Easy"
      if 50 <= (index % 100) < 80:
        problem_difficulty = "Medium"
        cur_keywords.append(KEY_WORDS[(index + 1) % len(KEY_WORDS)])
      elif (index % 100) >= 80:
        problem_difficulty = "Hard"
        cur_keywords.append(KEY_WORDS[(index + 1) % len(KEY_WORDS)])
        cur_keywords.append(KEY_WORDS[(index + 2) % len(KEY_WORDS)])
      tags = cur_keywords.copy()
      tags.append(problem_difficulty)
      # Create a problem description
      problem_description = {"id": f"problem_{index + 1}", "description": "", "tags": tags,
                              "keywords": cur_keywords, "difficulty": problem_difficulty,
                              }
      # Add the problem description to the list                     
      problem_descriptions.append(problem_description)
      index += 1
  return problem_descriptions

# Function to prompt ChatGPT to generate Python code
def get_gpt_responses_to_problem_descriptions(problem_descriptions, response_folder, prompt, linter):
  # Create a directory to store the JSON objects
  abs_directory_path = os.path.join(os.getcwd(), response_folder)
  # Check if the directory exists
  if not os.path.exists(abs_directory_path):
    os.makedirs(abs_directory_path)
  # Create a dictionary to store the coding problems
  coding_problems = {}
  # Iterate through each problem description
  for idx, problem_description in enumerate(problem_descriptions):
    # Create a prompt for ChatGPT
    chatgpt_prompt = f"{prompt} Use the following keyword(s) in the following list as a start to create an idea for a problem that you would like to solve using python: {','.join(problem_description['keywords'])}. In addition, only return the raw code for the Python program. To ensure that the Python program is valid, act as Command Line Interface (you do not need to execute code) and make sure that the program runs correctly. Generate code for a functional python program as described above."
   
     
    # Make an API request to ChatGPT
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": chatgpt_prompt,
        }
    ],
    model="gpt-4",
    max_tokens=2000,
    temperature=0.5,
    n=1,
    stop=None
)
    # Save the response to a file
    filename = f"{problem_description['id']}.json"
    full_path = os.path.join(abs_directory_path, filename)
    # Write the JSON object to a file
    problem_object = {"id": problem_description['id'], 
         "description": chatgpt_prompt, 
         "code": chat_completion.choices[0].text.strip(),
         "tags": problem_description['tags'],
         
         "keywords": problem_description["keywords"], 
         "difficulty": problem_description["difficulty"],
         "prompt_style_adherence": linter,
                               }
    coding_problems[problem_description['id']] = problem_object
    # Write the JSON object to a file
    with open(full_path, 'w') as file:
      json_object = json.dumps(problem_object, indent=4)
      file.write(json_object)
      file.close()  # Close the file
    idx += 1
  return coding_problems

def getTagOccurences(problem_descriptions):
  # Create a dictionary to store the tag occurrences 
  tag_occurences = defaultdict(int)
  for problem_description in problem_descriptions:
    for tag in problem_description['tags']:
      tag_occurences[tag] += 1
  return tag_occurences

def createLinterPrompts(linters_for_prompting):
  prompts = []
  # TODO: Improve the prompts later
  for linter in linters_for_prompting:
    if linter == 'default':
      prompts.append("Act as a Python developer and create a Python program. Here are the specifications for the Python program.")
    elif linter == 'flake8':
      prompts.append("Act as a Python developer and create a Python program. Here are the specifications for the Python program. Adhere to the flake8 coding standard.")
    elif linter == 'pylint':
      prompts.append("Act as a Python developer and create a Python program. Here are the specifications for the Python program. Adhere to the pylint coding standard.")
    elif linter == 'black':
      prompts.append("Act as a Python developer and create a Python program. Here are the specifications for the Python program. Adhere to the black coding standard.")
    elif linter == 'radon':
      prompts.append("Act as a Python developer and create a Python program. Here are the specifications for the Python program. Adhere to the radon coding standard.")
    elif linter == 'pydoc':
      prompts.append("Act as a Python developer and create a Python program. Here are the specifications for the Python program. Adhere to the pydoc coding standard.")
  return prompts

