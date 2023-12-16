from openai import OpenAI
from constants.linters import LINTER_NAMES
import os

OPENAI_API_CHAT_GPT_MODEL = "gpt-4-1106-preview"
OPENAI_API_KEY = "OPENAI_API_KEY"
OPENAI_API_CLIENT = OpenAI(api_key=os.environ[OPENAI_API_KEY])
OPENAI_API_MAX_TOKENS = 2000
OPENAI_API_TEMPERATURE = 0.5
OPENAI_API_N = 1
OPENAI_API_STOP = None
DATA_FOLDER = "data"
RESPONSE_FOLDER = "gpt_responses"
RESPONSE_FILE = RESPONSE_FOLDER
LINTER_RESULTS_FOLDER = "linter_results"
LINTER_RESULTS_FILE = LINTER_RESULTS_FOLDER
OUTPUT_FILE = "output"
OUTPUT_KEY = OUTPUT_FILE
OUTPUT_FOLDER = OUTPUT_FILE + "s"
OVERALL_OUTPUT_NAME_KEY = "name"
PROJECT_NAME = "ChatGPT Code Readability and Maintainability Tester"

# Arg Parsing
ARGUMENT_PARSER_DESCRIPTION = "Specify whether you want to generate python programs using ChatGPT and which linter/tool prompts to run."
ARGUMENT_PARSER_GENERATE_RESPONSES_ARGUMENT = "--generate_responses"
ARGUMENT_PARSER_GENERATE_RESPONSES_HELP_MESSAGE = "Including this tag will generate responses from ChatGPT."
ARGUMENT_PARSER_GENERATE_RESPONSES_ACTION = "store_true"
ARGUMENT_PARSER_LINTERS_ARGUMENT = "--linters"
ARGUMENT_PARSER_LINTERS_ALL_LINTERS = "all"
ARGUMENT_PARSER_LINTERS_CHOICES = LINTER_NAMES + [ARGUMENT_PARSER_LINTERS_ALL_LINTERS]
ARGUMENT_PARSER_LINTERS_N_ARGS = "*"
ARGUMENT_PARSER_LINTERS_HELP_MESSAGE = ('Specify which linter/tool prompts to run. '
'Options include flake8, pylint, black, radon, pydocstyle, default, or all.' '"default" uses the default prompt. If not specified, defaults to "default".')
ARGUMENT_PARSER_MODEL_ARGUMENT = "--model"
ARGUMENT_PARSER_MODEL_DEFAUT = "gpt-4-1106-preview"
ARGUMENT_PARSER_MODEL_HELP_MESSAGE = "Specify which model to use for generating responses. Defaults to gpt-4-1106-preview."