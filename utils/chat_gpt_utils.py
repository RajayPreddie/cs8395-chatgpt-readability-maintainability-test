import os
import json
import re
from collections import defaultdict
from openai import OpenAI
from constants.keywords import KEY_WORDS
from constants.prompts import ADDITIONAL_PROMPT_SPECIFICATIONS
from constants.linters import LINTER_PROMPTS_MAP



client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
def create_problem_descriptions(num_problems=5):
    problem_descriptions = []

    # Define ratios
    easy_ratio, medium_ratio = 0.5, 0.3
    num_easy = int(num_problems * easy_ratio)
    num_medium = int(num_problems * medium_ratio)
    num_hard = num_problems - num_easy - num_medium

    for index in range(num_problems):
        cur_keywords = [KEY_WORDS[index % len(KEY_WORDS)]]

        if index < num_easy:
            problem_difficulty = "Easy"
        elif index < num_easy + num_medium:
            problem_difficulty = "Medium"
            cur_keywords.append(KEY_WORDS[(index + 1) % len(KEY_WORDS)])
        else:
            problem_difficulty = "Hard"
            cur_keywords.extend([KEY_WORDS[(index + 1) % len(KEY_WORDS)], KEY_WORDS[(index + 2) % len(KEY_WORDS)]])

        tags = cur_keywords.copy()
        tags.append(problem_difficulty)

        problem_description = {
            "id": f"problem_{index + 1}",
            "description": "",
            "tags": tags,
            "keywords": cur_keywords,
            "difficulty": problem_difficulty
        }

        problem_descriptions.append(problem_description)

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
    chatgpt_prompt = f"{prompt} Use the following keyword(s) to solve a problem with Python: {','.join(problem_description['keywords'])}.{ADDITIONAL_PROMPT_SPECIFICATIONS}\n"
   
     
    # Make an API request to ChatGPT
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": chatgpt_prompt,
        }
    ],
    model="gpt-4-1106-preview",
    max_tokens=2000,
    temperature=0.5,
    n=1,
    stop=None
)
    
    code = chat_completion.choices[0].message.content
    # Define a regular expression pattern to match code blocks
    pattern = r'```python(.*?)```'
    # Find the first code block in the input string
    match = re.search(pattern, code, re.DOTALL)
    
    # Extract the inner part of ```python...```
    if match:
      code = match.group(1)  #
    # Save the response to a file
    filename = f"{problem_description['id']}.json"
    full_path = os.path.join(abs_directory_path, filename)
    # Write the JSON object to a file
    problem_object = {"id": problem_description['id'], 
         "description": chatgpt_prompt, 
         "code": code,
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
    if linter in LINTER_PROMPTS_MAP:
      prompts.append(LINTER_PROMPTS_MAP[linter])
  return prompts

