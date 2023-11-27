
import os
import json
from collections import defaultdict
from openai import OpenAI
from constants.keywords import KEY_WORDS


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def create_problem_descriptions(num_problems=1):
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
    chatgpt_prompt = f"{prompt} Use the following keywords to solve a problem with Python: {','.join(problem_description['keywords'])}. Remember to only respond with the raw code for the Python program. Generate a Python program that uses a list and return only the raw code. If you have explanations or comments, include them in the code as comments.\n"
   
     
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

    code = chat_completion.choices[0].message.content.strip('```').lstrip('python\n')
    if "python\n" == code[:7]:
      code = code[7:]
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
    print(linter)
    if linter == 'default':
      prompts.append("Act as a Python developer and create a Python program. "
    "Ensure your code is clean and readable. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")
    elif linter == 'flake8':
      prompts.append("Act as a Python developer and create a Python program that adheres to the flake8 coding standard. "
    "Here's an example snippet:\n\n"
    "# Example Snippet for Flake8\n"
    "def find_max(numbers):\n"
    "    \"\"\"Find the maximum number in a list.\"\"\"\n"
    "    return max(numbers) if numbers else None\n\n"
    "Ensure your code is clean, readable, and adheres to flake8 standards. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")
    elif linter == 'pylint':
      prompts.append(    "Act as a Python developer and write a Python program that strictly adheres to the pylint coding standard. "
    "Here's an example snippet compliant with pylint:\n\n"
    "\"\"\"Module for demonstrating pylint adherence.\n\n"
    "This module provides an example function formatted to comply with pylint standards.\n"
    "\"\"\"\n\n"
    "def calculate_sum(a, b):\n"
    "    \"\"\"Calculate and return the sum of two numbers.\"\"\"\n"
    "    return a + b\n"
    "\n"
    "Focus on clean, readable code following the style of the provided snippet. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface."
)
    elif linter == 'black':
      prompts.append(    "Act as a Python developer and write a Python program that strictly adheres to the Black coding style. "
    "Here's an example snippet formatted using Black:\n\n"
    "def format_name(first_name, last_name):\n"
    "    formatted_first_name = first_name.strip().title()\n"
    "    formatted_last_name = last_name.strip().title()\n"
    "    return f\"{formatted_first_name} {formatted_last_name}\"\n\n"
    "Ensure the code is formatted according to Black's uncompromising style. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface."
)
    elif linter == 'radon':
      prompts.append(    "Act as a Python developer and write a Python program with a focus on maintainable and low-complexity code as measured by radon. "
    "Here's a more complex example snippet with low cyclomatic complexity:\n\n"
    "# Example Snippet for Radon\n"
    "def fibonacci(n):\n"
    "    \"\"\"Return the nth Fibonacci number.\"\"\"\n"
    "    if n <= 1:\n"
    "        return n\n"
    "    return fibonacci(n - 1) + fibonacci(n - 2)\n\n"
    "def main():\n"
    "    for i in range(10):\n"
    "        print(fibonacci(i))\n\n"
    "if __name__ == \"__main__\":\n"
    "    main()\n\n"
    "Strive for a simple and clear code structure, minimizing cyclomatic complexity. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")
    elif linter == 'pydoc':
      prompts.append(    "Act as a Python developer and write a Python program that strictly adheres to the pydocstyle standard for docstrings. "
    "Include a module-level docstring as per pydocstyle guidelines. Here's an example snippet:\n\n"
    "\"\"\"Module for demonstrating pydocstyle adherence.\n\n"
    "This module provides examples of how to write docstrings that conform to pydocstyle standards.\n"
    "\"\"\"\n\n"
    "def add_numbers(x, y):\n"
    "    \"\"\"Add two numbers and return the result.\n\n"
    "    :param x: The first number to add.\n"
    "    :param y: The second number to add.\n"
    "    :return: The sum of x and y.\n"
    "    \"\"\"\n"
    "    return x + y\n\n"
    "Focus on comprehensive and compliant docstring documentation. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")
  return prompts

