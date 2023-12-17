# ChatGPT Code Readability and Maintainability Tester

## Welcome to the ChatGPT Code Readability and Maintainability Tester!

### Elevating Python Code Quality with AI and Expert Tools

Embark on an insightful journey into the world of code quality with our ChatGPT Code Readability and Maintainability Tester. This innovative tool is your gateway to uncovering the depths of readability and maintainability in Python code, especially the kind generated by the advanced AI of OpenAI's GPT models.

### A Fusion of AI and Linting Excellence

At the heart of our tool lies a powerful combination of AI-generated Python code and a suite of renowned linting tools. We employ the best in class – Flake8, Black, Radon, Pydocstyle, and Pylint – to delve into the intricacies of code quality. It's a symphony of technological prowess designed to offer you comprehensive insights into how ChatGPT's code stacks up in terms of readability, maintainability, and adherence to revered coding standards.

### A Kaleidoscope of Coding Challenges

The adventure doesn't end there. Our tool features 6 unique prompts, each a call to ChatGPT to craft a Python program based on specific guidelines. These guidelines are not just any rules; they are inspired by one or more keywords from a curated list of 100, ensuring a diverse range of coding scenarios.

### Adhering to the Gold Standards

Each piece of ChatGPT-generated Python code is an exploration in itself, conforming to one of the five different linting standards: Flake8, Black, Radon, Pydocstyle, and Pylint. We also introduce a default prompt, free from the specifics of any linting tool, adding another layer to this fascinating analysis.

### 120 Programs, Unbounded Insights

With 20 Python programs generated for each prompt type, we present you with a total of 120 ChatGPT-crafted Python programs. This extensive collection is more than just code; it's a treasure trove of insights waiting to be discovered.

## Installation

**Prerequisites:**
- Python 3.9.6 (if this does not work, try a higher version)
- pip package manager

**Steps:**
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Set up the environment:
```
python3 -m venv venv
```
```
source venv/bin/activate  # Unix/MacOS
```
```
venv\Scripts\activate  # Windows
```
4. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

## Configuration
Set up the project using `config.json`. This configuration file includes essential parameters such as the GPT model version and command options. Modify the fields as needed to tailor the tool to our specific project requirements.

## Usage
Execute the tool with the following command:

```
python3 main.py --generate_responses --linters [OPTIONS]
```

- `--generate_responses`: Activates the generation of Python programs using ChatGPT.
- `--linters`: Specify which linter prompts to apply. Options include `flake8`, `pylint`, `black`, `radon`, `pydocstyle`, `default`, and `all`. Defaults to `default` when not specified.
On each run of the tool, all of the linters/tools are used. The --linters argument is
for speciyfing which linter prompts to use when prompting ChatGPT for python programs.
- `-- model`: This is here for integrating with the [cs8395/test-suite](https://github.com/nkalupahana/cs8395-test-suite). The input model is not used. The repository utilizes gpt-4-1106-preview. I recommend to not use the model argument.

For example:

```bash
python3 main.py --generate_responses --linters flake8 pylint
```

This command generates Python programs using ChatGPT prompts that ask to adhere to flake8 and pylint.

## Utility Scripts Overview
- **chat_gpt_utils.py**: Manages interactions with GPT models for problem description generation.
- **data_processing_utils.py**: Integrates Chat GPT responses with linters for data processing.
- **general_utils.py**: Provides JSON data extraction and other general functionalities.
- **linting_utils.py**: Contains linting functionalities, crucial for code quality checks.
- **radon_data.py**, **violation_data.py**, **linter_data.py**, **analysis_data.py**, **default_data.py**: Handle data analysis and management related to linting and code quality.

## Constants
Constants in `prompts.py`, `keywords.py`, and `linters.py` guide Python code generation and analysis, integral to the tool's functionality.

## Results Explanation
The results provide a comprehensive assessment of Python code quality, combining complexity analysis with adherence to coding standards across multiple linters. They offer actionable insights into areas of improvement, guiding efforts towards cleaner, more maintainable, and well-documented code. Below are classes that are used to represent and manipulate data.

### LinterData Class
Aggregates data from different linting tools, providing an overview and detailed analysis by category. Useful for a comprehensive understanding of code quality across multiple dimensions.

### RadonData Class
Offers insights into code complexity, including:
- `average_file_score`: Reflects the overall complexity of the analyzed code. A lower score suggests simpler code.
- `average_code_block_type_scores`: Shows the average complexity for different code block types, indicating specific areas where the code might be overly complex or hard to maintain. The code block types include the following: function, class, and method.

### ViolationData Class
Focuses on code standard violations (pylint, pydocstyle, flake8), providing detailed metrics such as:
- `total_violations`: The total number of violations found across all analyzed code.
- `average_violations_per_line`: Average number of violations per line of code, indicating overall code cleanliness.
- `average_violations_per_file`: Average violations in each file, providing a file-level view of code quality.
- `violation_frequencies`: A breakdown of the frequency of each type of violation.
- `most_frequent_violation`: The most commonly occurring violation.
- `top_violations`: A list of the most frequent violations, offering a quick view of the primary issues in the codebase.

### DefaultLinterData Class
A generalized form of data tracking for various linting tools, highlighting overall code violations and identifying frequent issues. Specifically for the Black tool, it includes metrics like total violations and violation frequencies.

### Individual Linter Output Scores
The `output.json` file provides an overall analysis of code readability and maintainability through the lens of Radon.

Each score is the Radon average score per file for each linter prompt, providing an insight into the readability and maintainability of the code ChatGPT writes based on the linter prompt.

## Acknowledgement
The inspiration for the methodology diffculty levels comes from one of the research 
presentations I viewed in CS8395.

The following repositories of mine helped with the development of this code: 
1. [ChatGPT Python Code Execution Comparison](https://github.com/RajayPreddie/cs8395-chatgpt-python-code-execution-comparison)
2. [Test ChatGPT Coding Style](https://github.com/RajayPreddie/cs8395-test-chat-gpt-coding-style)

## Sources
1. [stackoverflow](https://stackoverflow.com/questions/56875810/new-pull-request-when-one-is-already-opened)
## ChatGPT Chat Links:
1. [ChatLink](https://chat.openai.com/share/9c43608f-52d8-4415-8203-57a693547093)
2. [ChatLink](https://chat.openai.com/share/cbfa536a-aa16-4024-b7df-bf2bf43df448)
3. [ChatLink](https://chat.openai.com/share/8216251e-6534-4e45-b0e6-1b085bdc25e3)
4. [ChatLink](https://chat.openai.com/share/5a456d75-a3ac-403c-b974-f255f947e5dc)
5. [ChatLink](https://chat.openai.com/share/56829880-fc4f-4a9d-8bda-ea17fed2087d)
6. I utilized many other ChatGPT chats for developing the code.


## License
[MIT License]