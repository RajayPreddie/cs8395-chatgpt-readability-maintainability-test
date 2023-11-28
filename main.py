from collections import defaultdict
from openai import OpenAI
import json
import os
import subprocess
import argparse
import tempfile
import re
from classes.linter_data import LinterData
from utils.linting_utils import getLinterResultsForProblems
from utils.chat_gpt_utils import get_gpt_responses_to_problem_descriptions, createLinterPrompts, create_problem_descriptions
from utils.general_utils import extract_json_from_directory
from constants.linters import LINTER_NAMES

# TODO: Argument Parsing
# TODO: In the general output.json, only show the most important results across the different problem descriptions.

parser = argparse.ArgumentParser(description='Get ChatGPT responses and write to files.')
parser.add_argument('--generate_responses', action='store_true', help='Generate python programs using ChatGPT.')

# Updated argument for linters/tools
parser.add_argument('--linters', nargs='*', choices=['flake8', 'pylint', 'black', 'radon', 'pydocstyle', 'default', 'all'],
                    default=['default'],
                    help='Specify which linter/tool prompts to regenerate. '
                         'Options include flake8, pylint, black, radon, pydocstyle, default, or all. '
                         '"default" uses the default prompt. If not specified, defaults to "default".')

args = parser.parse_args()

# Usage example
if 'all' in args.linters:
    args.linters = ['default','flake8', 'pylint', 'black', 'radon', 'pydocstyle']

# Create problem descriptions
problem_descriptions = create_problem_descriptions()

linters_for_prompting = args.linters
prompts = createLinterPrompts(linters_for_prompting=linters_for_prompting)

def getPromptSolutions(response_folder, problem_descriptions, prompt, linter, args):
  # Prompt Chat GPT to generate the Python Interpreter output
  abs_directory_path = os.path.join(os.getcwd(), response_folder)
  # If the path already exists, then there is no need to reprompt ChatGPT
  prompt_solutions = {}
  # Check if the directory exists
  if not os.path.exists(abs_directory_path) or args.generate_responses:
    # Prompt Chat GPT to generate the Python Interpreter output
      if not os.path.exists(abs_directory_path):
        os.makedirs(abs_directory_path)
      prompt_solutions = get_gpt_responses_to_problem_descriptions(problem_descriptions, response_folder, prompt, linter)
  else:
      # Extract the prompt solutions from the directory
      prompt_solutions = extract_json_from_directory(abs_directory_path)
  return prompt_solutions

def createOverallResultsForProblems(linter_results_for_prompt_solutions, prompt_solutions, linting_results_directory_path):

  # Create a dictionary to store the overall results
  overall_results = {linter: LinterData(linter) for linter in LINTER_NAMES}
  # Iterate through each prompt solution
  for problem_id, current_problem_linter_results in linter_results_for_prompt_solutions.items():
    # Save the results to a file
    filename = f"{problem_id}.json"
    # Create a directory to store the JSON objects
    full_path = os.path.join(linting_results_directory_path, filename)
    # Write the prompt solution to a file
    with open(full_path, 'w') as file:
      # Convert the JSON object to a string
      json_object = json.dumps(
    current_problem_linter_results, indent=4)
      # Write the string to the file
      file.write(json_object)
      # Close the file
      file.close()
    # Iterate through each linter
    for linter, problem_result in current_problem_linter_results.items():
      
      overall_results[linter].overall.update_linter_data(problem_result)
      for tag in prompt_solutions[problem_id]['tags']:
          # number_of_python_programs_with_tag = count_tag_occurrences[tag]
          overall_results[linter].by_tag[tag].update_linter_data(problem_result)
  return overall_results
def saveResultsToFile(overall_results, linter_name):
    # Save the results to a file
  output_folder = f"output_{linter_name}"
  # Create a directory to store the JSON objects
  output_fullpath = os.path.join(os.getcwd(), output_folder)
  output_directory_path = os.path.join(os.getcwd(), output_fullpath)
  # Check if the directory exists
  if not os.path.exists(output_directory_path):
    os.makedirs(output_directory_path)
    
  output_filename = f"output_{linter_name}.json"
  output_filename_fullpath = os.path.join(output_directory_path, output_filename)
  # Convert overall_results to a dictionary format
  results_dict = {linter: data.to_dict() for linter, data in overall_results.items()}
  # Calculate the average number of violations per file across all linters. This is the output metric to integrate with cs8395/testing-suite
  results_dict["output"] = (results_dict["flake8"]["overall"]["average_violations_per_file"] + results_dict["pylint"]["overall"]["average_violations_per_file"] + results_dict["black"]["overall"]["average_violations_per_file"]) / 3
  # Write the prompt solution to a file
  with open(output_filename_fullpath, 'w') as file:
    # Convert the JSON object to a string
    json_object = json.dumps(
  results_dict, indent=4)
    # Write the string to the file
    file.write(json_object)
    # Close the file
    file.close()
for prompt, linter_name in zip(prompts, linters_for_prompting):

  response_folder = f"gpt_responses_{linter_name}"
  linter_results_folder = f"linter_results_{linter_name}"

  prompt_solutions = getPromptSolutions(response_folder=response_folder, problem_descriptions=problem_descriptions, prompt=prompt, linter=linter_name, args = args)
  
  # Create a directory to store the linting results
  linting_results_directory_path = os.path.join(os.getcwd(), linter_results_folder)
  # Check if the directory exists
  if not os.path.exists(linting_results_directory_path):
    os.makedirs(linting_results_directory_path)
  # Create a dictionary to store the results
  linter_results_for_prompt_solutions = getLinterResultsForProblems(prompt_solutions=prompt_solutions)
  overall_results = createOverallResultsForProblems(linter_results_for_prompt_solutions=linter_results_for_prompt_solutions, prompt_solutions=prompt_solutions, linting_results_directory_path=linting_results_directory_path)
  
  saveResultsToFile(overall_results=overall_results, linter_name=linter_name)


        
'''
Sources:
 https://stackoverflow.com/questions/56875810/new-pull-request-when-one-is-already-opened
 https://chat.openai.com/share/a12f646a-e29d-431c-8d7c-14ea042871e6
https://chat.openai.com/share/9e7df102-375e-43b5-b78f-e893c0a8fc35
 https://chat.openai.com/share/87f5573e-f6ee-478a-84c1-b1ed9b7f7efe
 https://chat.openai.com/share/7fe234a8-26bb-43d3-aedb-87aadc4eeb97
 https://chat.openai.com/share/d5be1d9c-e72f-4691-94a8-010fcf043850
 https://chat.openai.com/share/5fd503e2-c833-4ac1-b4e1-f47b92be678d
 https://chat.openai.com/share/56829880-fc4f-4a9d-8bda-ea17fed2087d
 https://chat.openai.com/share/308e2057-b531-4f82-a329-2f751db0735b
 https://chat.openai.com/share/49117405-6e08-45ec-8a25-e383880bff14
 https://chat.openai.com/share/3bdb1313-fa4f-4071-8f66-df525420190f
 https://chat.openai.com/share/dbe58fe2-9a0d-45b8-a1ef-1eb4edc78484
'''