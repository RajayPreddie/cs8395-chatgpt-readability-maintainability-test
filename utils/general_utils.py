import argparse
import os
import json
from constants.linters import LINTER_PROMPTS_MAP
# Extract JSON from a directory
def extract_json_from_directory(abs_directory_path):
  # Create a list to store the JSON objects
  json_objects= {}
  # Iterate through each file in the directory
  for filename in os.listdir(abs_directory_path):
    # Get the absolute path of the file
    file_path = os.path.join(abs_directory_path, filename)
    # Check if it's a file
    if os.path.isfile(file_path):
      # Open the file and extract the JSON object
      with open(file_path, 'r') as file:
        # Read the file
        data = file.read()
        # Convert the JSON object to a Python dictionary
        json_object = json.loads(data)
        json_objects[json_object["id"]] = json_object
        # Close the file
        file.close()
  # Return the list of JSON objects
  return json_objects


def createArgs():
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
      args.linters = LINTER_PROMPTS_MAP.keys()
  return args