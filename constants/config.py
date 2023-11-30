from openai import OpenAI
import os

CHAT_GPT_MODEL = "gpt-4-1106-preview"
OPENAI_API_KEY = "OPENAI_API_KEY"
OPENAI_API_CLIENT = OpenAI(api_key=os.environ[OPENAI_API_KEY])
DATA_FOLDER = "data"
RESPONSE_FOLDER = "gpt_responses"
LINTER_RESULTS_FOLDER = "linter_results"
OUTPUT_FOLDER = "output"