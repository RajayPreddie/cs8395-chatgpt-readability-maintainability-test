
import os
import subprocess
import tempfile
from collections import defaultdict
from constants import constants
from constants import linters

# Function to save the code to a temporary file
def save_code_to_temp_file(code):
  # Create a temporary file
  with tempfile.NamedTemporaryFile(delete=False, suffix=constants.PYTHON_FILE_SUFFIX) as tmp:
    tmp.write(code.encode(constants.UTF_ENCODING))
    return tmp.name
# Function to run a linting tool and capture its output
def run_linting_tool(tool_name, file_name, *args):
  # Create a command to run the linting tool
  command = [tool_name, file_name] + list(args)
  result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  return result.stdout, result.stderr
def parse_radon_output(output):
  # Create a dictionary to store the violations
  radon_data = defaultdict(int)
  code_block_type_frequency = defaultdict(int)
  number_of_lines = 0
  # Iterate through each line of the output
  for line in output.strip().split('\n'):
    # Check if the line is not empty
      if line:
        # Check if the line is a proper flake8 violation
        if not (line.startswith(constants.TEMP_FILE_NAME_START)):
          line = line.strip()
          # Get the violation type
          code_block_type = line[0]
          score = line[-2]
          if code_block_type == constants.CLASS_CODE_BLOCK_TYPE_NICKNAME:
            code_block_type_frequency[constants.CLASS_CODE_BLOCK_TYPE] += 1
            radon_data[constants.CLASS_CODE_BLOCK_TYPE] += int(score)
         
          elif code_block_type == constants.METHOD_CODE_BLOCK_TYPE_NICKNAME:
            code_block_type_frequency[constants.METHOD_CODE_BLOCK_TYPE] += 1
            radon_data[constants.METHOD_CODE_BLOCK_TYPE] += int(score)
    
          elif code_block_type == constants.FUNCTION_CODE_BLOCK_TYPE_NICKNAME:
            code_block_type_frequency[constants.FUNCTION_CODE_BLOCK_TYPE] += 1
            radon_data[constants.FUNCTION_CODE_BLOCK_TYPE] += int(score)
          radon_data[constants.OVERALL_SCORE_KEY] += int(score)
          number_of_lines += 1
        
  if constants.OVERALL_SCORE_KEY in radon_data:
    radon_data[constants.OVERALL_SCORE_KEY] = radon_data[constants.OVERALL_SCORE_KEY] / number_of_lines
  if constants.CLASS_CODE_BLOCK_TYPE in radon_data:
    radon_data[constants.CLASS_CODE_BLOCK_TYPE] /= code_block_type_frequency[constants.CLASS_CODE_BLOCK_TYPE]

  if constants.METHOD_CODE_BLOCK_TYPE in radon_data:
    radon_data[constants.METHOD_CODE_BLOCK_TYPE] /= code_block_type_frequency[constants.METHOD_CODE_BLOCK_TYPE]

  if constants.FUNCTION_CODE_BLOCK_TYPE in radon_data:
    radon_data[constants.FUNCTION_CODE_BLOCK_TYPE] /= code_block_type_frequency[constants.FUNCTION_CODE_BLOCK_TYPE]
  return radon_data
def update_violations_data(violations, most_frequent_violation, most_frequent_violation_count, violation_type):
  # Update the violation count
  violations[constants.VIOLATIONS_KEY][violation_type] += 1
  # Update the most frequent violation
  most_frequent_violation = most_frequent_violation if most_frequent_violation_count > violations[constants.VIOLATIONS_KEY][violation_type] else violation_type
  # Update the most frequent violation count
  most_frequent_violation_count = most_frequent_violation_count if most_frequent_violation_count > violations[constants.VIOLATIONS_KEY][violation_type] else violations[constants.VIOLATIONS_KEY][violation_type]
  # Update the total number of violations
  violations[constants.TOTAL_VIOLATIONS_KEY] += 1 
  return (violations, most_frequent_violation, most_frequent_violation_count)
# Function to parse and count the violations for flake8 and pylint
def parse_violations(lint_type, output, number_of_lines_in_code):
  # TODO: add in 
  # Create a dictionary to store the violations
  violations = {constants.VIOLATIONS_KEY: defaultdict(int), constants.TOTAL_VIOLATIONS_KEY: 0, constants.MOST_FREQUENT_VIOLATION_KEY: {constants.VIOLATION_TYPE_KEY: "", constants.FREQUENCY_KEY: 0}, constants.NUMBER_OF_LINES_IN_CODE_KEY: number_of_lines_in_code}
  most_frequent_violation = ""
  most_frequent_violation_count = 0
  # Iterate through each line of the output

  for line in output.strip().split('\n'):
    # Check if the line is not empty
    if line:
      violation_type = None
      # Check if the line is a proper flake8 violation
      if lint_type == linters.FLAKE8 and not (line.split(':')[-1].startswith(constants.FLAKE_8_PARSE_BRACE) or len(line.split(':')[-1].strip()) <= 1):
        # Get the violation type
        violation_type = line.split(':')[-1].strip()
      # Check if the line is a proper pylint violation
      elif lint_type == linters.PYLINT:
        # Get the violation type
        violation_type = line.split(':')[-1].strip()
        # Check if the line is pylint violation
        if (violation_type.startswith(constants.PYLINT_PARSE_STAR) or violation_type.startswith(constants.PYLINT_PARSE_YOUR_CODE_HAS_BEEN_RATED_AT) or violation_type.startswith(constants.PYLINT_PARSE_MINUS)):
          violation_type = None
      elif lint_type == linters.PYDOCSTYLE and not line.startswith(constants.TEMP_FILE_NAME_START):
        violation_type = line.strip()
        
      if violation_type:
        violations,most_frequent_violation, most_frequent_violation_count = update_violations_data(violations, most_frequent_violation, most_frequent_violation_count, violation_type)
  # Update the most frequent violation
  violations[constants.MOST_FREQUENT_VIOLATION_KEY][constants.VIOLATION_TYPE_KEY] = most_frequent_violation
  # Update the most frequent violation count
  violations[constants.MOST_FREQUENT_VIOLATION_KEY][constants.FREQUENCY_KEY] = most_frequent_violation_count
  return violations

# Main function to run all linting tools
def run_all_linters(code):
  # Save the code to a temporary file
  tmp_filename = save_code_to_temp_file(code)
  # Create a dictionary to store the results
  number_of_lines_in_code = count_lines(code)
  results = {}
  # flake8
  flake8_output, _ = run_linting_tool(linters.FLAKE8, tmp_filename)
  # Parse the flake8 output
  results[linters.FLAKE8] = parse_violations(linters.FLAKE8, flake8_output, number_of_lines_in_code)
  
  
  # pylint
  pylint_output, _ = run_linting_tool(linters.PYLINT, constants.PYLINT_COMMAND_LINE_ARGS[constants.PYLINT_OUTPUT_FORMAT_TEXT_ARG], tmp_filename)
  # Parse the pylint output
  results[linters.PYLINT] = parse_violations(linters.PYLINT, pylint_output, number_of_lines_in_code)

  # black
  _, black_output= run_linting_tool(linters.BLACK, constants.BLACK_COMMAND_LINE_ARGS[constants.BLACK_CHECK_ARG], tmp_filename)
  # Parse the black output
  results[linters.BLACK] = {constants.VIOLATIONS_KEY: {} if constants.BLACK_WOULD_REFORMAT not in black_output else {constants.BLACK_NON_COMPLIANT_KEY: 1} ,
                      constants.TOTAL_VIOLATIONS_KEY: 1 if constants.BLACK_WOULD_REFORMAT in black_output else 0,
                      constants.MOST_FREQUENT_VIOLATION_KEY: {constants.VIOLATION_TYPE_KEY: constants.BLACK_WOULD_REFORMAT ,
                      constants.FREQUENCY_KEY: 1 } if constants.BLACK_WOULD_REFORMAT in black_output else {}}
  # take a similar approach to what the Black parsing
  # Running Radon (for Cyclomatic Complexity, etc.)
  radon_output, _ = run_linting_tool(linters.RADON, constants.RADON_COMMAND_LINE_ARGS[constants.RADON_CLASS_COMPLEXITY_ARG], constants.RADON_COMMAND_LINE_ARGS[constants.RADON_SHOW_ARG] ,tmp_filename)
  results[linters.RADON] = parse_radon_output(radon_output)
  
  pydoc_output, _ = run_linting_tool(linters.PYDOCSTYLE, tmp_filename)
  results[linters.PYDOCSTYLE] = parse_violations(linters.PYDOCSTYLE, pydoc_output, number_of_lines_in_code)
  # remove the temporary file
  os.remove(tmp_filename)
 
  return results

def getLinterResultsForProblems(prompt_solutions):
  linter_results_for_prompt_solutions = {}
  # Iterate through each prompt solution
  for id, prompt_solution in prompt_solutions.items():
    # Run linters on the code string
    lint_results = run_all_linters(prompt_solution[constants.CODE_KEY])
    # Add the prompt solution to the dictionary
    linter_results_for_prompt_solutions[id] = lint_results
  return linter_results_for_prompt_solutions
def count_lines(code_str):
    # Split the string into lines
    lines = code_str.splitlines()
    return len(lines)
