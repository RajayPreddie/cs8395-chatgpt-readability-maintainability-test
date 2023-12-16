import argparse
import os
import json
from constants.linters import LINTER_PROMPTS_MAP, DEFAULT
from constants import config
from constants.constants import ID_KEY

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
        json_objects[json_object[ID_KEY]] = json_object
        # Close the file
        file.close()
  # Return the list of JSON objects
  return json_objects


def createArgs():
  parser = argparse.ArgumentParser(description=config.ARGUMENT_PARSER_DESCRIPTION)
  parser.add_argument(config.ARGUMENT_PARSER_GENERATE_RESPONSES_ARGUMENT, action=config.ARGUMENT_PARSER_GENERATE_RESPONSES_ACTION, help=config.ARGUMENT_PARSER_GENERATE_RESPONSES_HELP_MESSAGE)

  # Updated argument for linters/tools
  parser.add_argument(config.ARGUMENT_PARSER_LINTERS_ARGUMENT, nargs=config.ARGUMENT_PARSER_LINTERS_N_ARGS, choices=config.ARGUMENT_PARSER_LINTERS_CHOICES,
                      default=[DEFAULT],
                      help=config.ARGUMENT_PARSER_LINTERS_HELP_MESSAGE)
  parser.add_argument("--model", type=str, default="gpt-4", help="The model to use for generating responses.")

  args = parser.parse_args()

  # Usage example
  if config.ARGUMENT_PARSER_LINTERS_ALL_LINTERS in args.linters:
      args.linters = LINTER_PROMPTS_MAP.keys()
  return args