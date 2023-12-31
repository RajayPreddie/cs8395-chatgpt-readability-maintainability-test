from constants.prompts import BLACK_PROMPT, DEFAULT_PROMPT, FLAKE8_PROMPT, PYDOCSTYLE_PROMPT, PYLINT_PROMPT, RADON_PROMPT

PYDOCSTYLE = 'pydocstyle'
RADON = 'radon'
BLACK = 'black'
PYLINT = 'pylint'
FLAKE8 = 'flake8'
DEFAULT = 'default'
LINTER_PROMPTS_MAP = {DEFAULT: DEFAULT_PROMPT, FLAKE8: FLAKE8_PROMPT, PYLINT: PYLINT_PROMPT, BLACK: BLACK_PROMPT, RADON: RADON_PROMPT, PYDOCSTYLE: PYDOCSTYLE_PROMPT}
LINTER_NAMES = LINTER_NAMES = [key for key in LINTER_PROMPTS_MAP.keys() if key != DEFAULT]


