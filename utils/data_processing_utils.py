import os
import json
from tqdm import tqdm
from classes.linter_data import LinterData
from constants.linters import LINTER_NAMES
from utils.general_utils import createArgs, extract_json_from_directory
from utils.chat_gpt_utils import get_gpt_responses_to_problem_descriptions, createLinterPrompts, create_problem_descriptions
from utils.linting_utils import getLinterResultsForProblems

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

def saveResultsToFile(results, linter_name):
    # Save the results to a file
  output_folder = f"data/outputs/output_{linter_name}"
  # Create a directory to store the JSON objects
  output_fullpath = os.path.join(os.getcwd(), output_folder)
  output_directory_path = os.path.join(os.getcwd(), output_fullpath)
  # Check if the directory exists
  if not os.path.exists(output_directory_path):
    os.makedirs(output_directory_path)
    
  output_filename = f"output_{linter_name}.json"
  output_filename_fullpath = os.path.join(output_directory_path, output_filename)
  # Convert overall_results to a dictionary format
  results["output"] = results["radon"]["overall"]["average_file_score"]
  # Write the prompt solution to a file
  with open(output_filename_fullpath, 'w') as file:
    # Convert the JSON object to a string
    json_object = json.dumps(
  results, indent=4)
    # Write the string to the file
    file.write(json_object)
    # Close the file
    file.close()
    
def run_data_processing():
  args = createArgs()
  problem_descriptions = create_problem_descriptions()
  linters_for_prompting = args.linters
  prompts = createLinterPrompts(linters_for_prompting=linters_for_prompting)
  all_linters_overall_output_json = {
      "name": "ChatGPT Code Readability and Maintainability Tester",
      "tags": [],
      "output": 0.0,
  }
  for prompt, linter_name in tqdm(zip(prompts, linters_for_prompting), total=len(prompts), colour='green', desc="Overall Results"):

    response_folder = f"data/gpt_responses/gpt_responses_{linter_name}"
    linter_results_folder = f"data/linter_results/linter_results_{linter_name}"

    prompt_solutions = getPromptSolutions(response_folder=response_folder, problem_descriptions=problem_descriptions, prompt=prompt, linter=linter_name, args = args)
    
    # Create a directory to store the linting results
    linting_results_directory_path = os.path.join(os.getcwd(), linter_results_folder)
    # Check if the directory exists
    if not os.path.exists(linting_results_directory_path):
      os.makedirs(linting_results_directory_path)
    # Create a dictionary to store the results
    linter_results_for_prompt_solutions = getLinterResultsForProblems(prompt_solutions=prompt_solutions)
    linter_overall_results = createOverallResultsForProblems(linter_results_for_prompt_solutions=linter_results_for_prompt_solutions, prompt_solutions=prompt_solutions, linting_results_directory_path=linting_results_directory_path)
    linter_results= {linter: data.to_dict() for linter, data in linter_overall_results.items()}
    all_linters_overall_output_json[f"{linter_name}_output"] = linter_results["radon"]["overall"]["average_file_score"]
    all_linters_overall_output_json["output"] += linter_results["radon"]["overall"]["average_file_score"] / len(linters_for_prompting)
    saveResultsToFile(results=linter_results, linter_name=linter_name)
  all_linters_overall_output_json_path = os.path.join(os.getcwd(), "output.json")
  with open(all_linters_overall_output_json_path, 'w') as file:
      # Convert the JSON object to a string
      json_object = json.dumps(
    all_linters_overall_output_json, indent=4)
      # Write the string to the file
      file.write(json_object)
      # Close the file
      file.close()
    