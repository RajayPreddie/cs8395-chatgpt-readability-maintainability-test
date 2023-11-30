import os
import json
import re
from collections import defaultdict
from constants import constants
from constants import config
from constants.keywords import KEY_WORDS
from constants.prompts import ADDITIONAL_PROMPT_SPECIFICATIONS
from constants.linters import LINTER_PROMPTS_MAP



def create_problem_descriptions(num_problems=20):
    problem_descriptions = []


   
    num_easy = int(num_problems * constants.NUMBER_OF_EASY_PROBLEMS_RATIO)
    num_medium = int(num_problems *  constants.NUMBER_OF_MEDIUM_PROBLEMS_RATIO)
    
    for index in range(num_problems):
        cur_keywords = [KEY_WORDS[index % len(KEY_WORDS)]]

        if index < num_easy:
            problem_difficulty = constants.PROBLEM_DIFFICULTY_EASY
        elif index < num_easy + num_medium:
            problem_difficulty = constants.PROBLEM_DIFFICULTY_MEDIUM
            cur_keywords.append(KEY_WORDS[(index + 1) % len(KEY_WORDS)])
        else:
            problem_difficulty = constants.PROBLEM_DIFFICULTY_HARD
            cur_keywords.extend([KEY_WORDS[(index + 1) % len(KEY_WORDS)], KEY_WORDS[(index + 2) % len(KEY_WORDS)]])

        tags = cur_keywords.copy()
        tags.append(problem_difficulty)

        problem_description = {
            constants.ID_KEY: f"{constants.PROBLEM}_{index + 1}",
            constants.DESCRIPTION_KEY: "",
            constants.TAGS_KEY: tags,
            constants.KEYWORDS_KEY: cur_keywords,
            constants.DIFFICULTY_KEY: problem_difficulty
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
    chatgpt_prompt = f"{prompt} {constants.USE_THE_FOLLOWING_KEYWORDS} {','.join(problem_description[constants.KEYWORDS_KEY])}.{ADDITIONAL_PROMPT_SPECIFICATIONS}\n"
   
     
    # Make an API request to ChatGPT
    chat_completion = config.OPENAI_API_CLIENT.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": chatgpt_prompt,
        }
    ],
    model=config.OPENAI_API_CHAT_GPT_MODEL,
    max_tokens= config.OPENAI_API_MAX_TOKENS,
    temperature=config.OPENAI_API_TEMPERATURE,
    n=config.OPENAI_API_N,
    stop=config.OPENAI_API_STOP
)
    
    code = chat_completion.choices[0].message.content
    # Find the first code block in the input string
    match = re.search(constants.FILTER_MARKDOWN_CODE_REGEX, code, re.DOTALL)
    
    # Extract the inner part of ```python...```
    if match:
      code = match.group(constants.FILTER_MARKDOWN_CODE_MATCH_GROUP)  #
    # Save the response to a file
    filename = f"{problem_description[constants.ID_KEY]}{constants.DOT_JSON}"
    full_path = os.path.join(abs_directory_path, filename)
    # Write the JSON object to a file
    problem_object = {constants.ID_KEY: problem_description[constants.ID_KEY], 
         constants.DESCRIPTION_KEY: chatgpt_prompt, 
         constants.CODE_KEY: code,
         constants.TAGS_KEY: problem_description[constants.TAGS_KEY],
         
         constants.KEYWORDS_KEY: problem_description[constants.KEYWORDS_KEY], 
         constants.DIFFICULTY_KEY: problem_description[constants.DIFFICULTY_KEY],
         constants.PROMPT_STYLE_ADHERENCE_KEY: linter,
                               }
    coding_problems[problem_description[constants.ID_KEY]] = problem_object
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
    for tag in problem_description[constants.TAGS_KEY]:
      tag_occurences[tag] += 1
  return tag_occurences

def createLinterPrompts(linters_for_prompting):
  prompts = []
  # TODO: Improve the prompts later
  for linter in linters_for_prompting:
    if linter in LINTER_PROMPTS_MAP:
      prompts.append(LINTER_PROMPTS_MAP[linter])
  return prompts

