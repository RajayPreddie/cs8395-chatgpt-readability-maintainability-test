
import os
import subprocess
import tempfile
from collections import defaultdict

# Function to save the code to a temporary file
def save_code_to_temp_file(code):
  # Create a temporary file
  with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
    tmp.write(code.encode('utf-8'))
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
        if not (line.startswith('/var')):
          line = line.strip()
          # Get the violation type
          code_block_type = line[0]
          score = line[-2]
          if code_block_type == "C":
            code_block_type_frequency["class_complexity"] += 1
            radon_data['class_complexity'] += int(score)
         
          elif code_block_type == "M":
            code_block_type_frequency["method_complexity"] += 1
            radon_data['method_complexity'] += int(score)
    
          elif code_block_type == "F":
            code_block_type_frequency["function_complexity"] += 1
            radon_data['function_complexity'] += int(score)
          radon_data['overall_score'] += int(score)
          number_of_lines += 1
        
  if "overall_score" in radon_data:
    radon_data['overall_score'] = radon_data['overall_score'] / number_of_lines
  if "class_complexity" in radon_data:
    radon_data['class_complexity'] /= code_block_type_frequency["class_complexity"]

  if "method_complexity" in radon_data:
    radon_data['method_complexity'] /= code_block_type_frequency["method_complexity"]

  if "function_complexity" in radon_data:
    radon_data['function_complexity'] /= code_block_type_frequency["function_complexity"]
  return radon_data
def update_violations_data(violations, most_frequent_violation, most_frequent_violation_count, violation_type):
  # Update the violation count
  violations["violations"][violation_type] += 1
  # Update the most frequent violation
  most_frequent_violation = most_frequent_violation if most_frequent_violation_count > violations["violations"][violation_type] else violation_type
  # Update the most frequent violation count
  most_frequent_violation_count = most_frequent_violation_count if most_frequent_violation_count > violations["violations"][violation_type] else violations["violations"][violation_type]
  # Update the total number of violations
  violations["total_violations"] += 1 
  return (violations, most_frequent_violation, most_frequent_violation_count)
# Function to parse and count the violations for flake8 and pylint
def parse_violations(lint_type, output, number_of_lines_in_code):
  # TODO: add in 
  # Create a dictionary to store the violations
  violations = {"violations": defaultdict(int), "total_violations": 0, "most_frequent_violation": {"violation_type": "", "frequency": 0}, "number_of_lines_in_code": number_of_lines_in_code}
  most_frequent_violation = ""
  most_frequent_violation_count = 0
  # Iterate through each line of the output
  for line in output.strip().split('\n'):
    # Check if the line is not empty
    if line:
      violation_type = None
      # Check if the line is a proper flake8 violation
      if lint_type == 'flake8' and not (line.split(':')[-1].startswith('{') or len(line.split(':')[-1].strip()) <= 1):
        # Get the violation type
        violation_type = line.split(':')[-1].strip()
      # Check if the line is a proper pylint violation
      elif lint_type == 'pylint':
        # Get the violation type
        violation_type = line.split(':')[-1].strip()
        # Check if the line is pylint violation
        if (violation_type.startswith('*') or violation_type.startswith('Your code has been rated at') or violation_type.startswith('-')):
          violation_type = None
      elif lint_type == "pydocstyle" and not line.startswith('/var'):
        violation_type = line.strip()
        
      if violation_type:
        violations,most_frequent_violation, most_frequent_violation_count = update_violations_data(violations, most_frequent_violation, most_frequent_violation_count, violation_type)
  # Update the most frequent violation
  violations["most_frequent_violation"]["violation_type"] = most_frequent_violation
  # Update the most frequent violation count
  violations["most_frequent_violation"]["frequency"] = most_frequent_violation_count
  return violations

# Main function to run all linting tools
def run_all_linters(code):
  # Save the code to a temporary file
  tmp_filename = save_code_to_temp_file(code)
  # Create a dictionary to store the results
  number_of_lines_in_code = count_lines(code)
  results = {}
  # flake8
  flake8_output, _ = run_linting_tool('flake8', tmp_filename)
  # Parse the flake8 output
  results['flake8'] = parse_violations('flake8', flake8_output, number_of_lines_in_code)
  
  
  # pylint
  pylint_output, _ = run_linting_tool('pylint', '--output-format=text', tmp_filename)
  # Parse the pylint output
  results['pylint'] = parse_violations('pylint', pylint_output, number_of_lines_in_code)

  # black
  _, black_output= run_linting_tool('black', '--check', tmp_filename)
  # Parse the black output
  results['black'] = {"violations": {} if 'would reformat' not in black_output else {"Non-compliant": 1} ,
                      "total_violations": 1 if 'would reformat' in black_output else 0,
                      "most_frequent_violation": {"violation_type": "would reformat" ,
                      "frequency": 1 } if 'would reformat' in black_output else {}}
  # take a similar approach to what the Black parsing
  # Running Radon (for Cyclomatic Complexity, etc.)
  radon_output, _ = run_linting_tool('radon', "cc","-s",tmp_filename)
  results['radon'] = parse_radon_output(radon_output)
  
  pydoc_output, _ = run_linting_tool('pydocstyle', tmp_filename)
  results["pydocstyle"] = parse_violations("pydocstyle", pydoc_output, number_of_lines_in_code)
  # remove the temporary file
  os.remove(tmp_filename)
 
  return results

def getLinterResultsForProblems(prompt_solutions):
  linter_results_for_prompt_solutions = {}
  # Iterate through each prompt solution
  for id, prompt_solution in prompt_solutions.items():
    # Run linters on the code string
    lint_results = run_all_linters(prompt_solution['code'])
    # Add the prompt solution to the dictionary
    linter_results_for_prompt_solutions[id] = lint_results
  return linter_results_for_prompt_solutions
def count_lines(code_str):
    # Split the string into lines
    lines = code_str.splitlines()
    return len(lines)
