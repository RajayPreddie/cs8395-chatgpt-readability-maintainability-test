DEFAULT_PROMPT = ("Act as a Python developer and create a Python program. "
    "Ensure your code is clean and readable. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")

FLAKE8_PROMPT = ("Act as a Python developer and create a Python program that adheres to the flake8 coding standard. "
    "Here's an example snippet:\n\n"
    "# Example Snippet for Flake8\n"
    "def find_max(numbers):\n"
    "    \"\"\"Find the maximum number in a list.\"\"\"\n"
    "    return max(numbers) if numbers else None\n\n"
    "Ensure your code is clean, readable, and adheres to flake8 standards. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")

PYLINT_PROMPT = (    "Act as a Python developer and write a Python program that strictly adheres to the pylint coding standard. "
    "Here's an example snippet compliant with pylint:\n\n"
    "\"\"\"Module for demonstrating pylint adherence.\n\n"
    "This module provides an example function formatted to comply with pylint standards.\n"
    "\"\"\"\n\n"
    "def calculate_sum(a, b):\n"
    "    \"\"\"Calculate and return the sum of two numbers.\"\"\"\n"
    "    return a + b\n"
    "\n"
    "Focus on clean, readable code following the style of the provided snippet. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface."
)

BLACK_PROMPT = (    "Act as a Python developer and write a Python program that strictly adheres to the Black coding style. "
    "Here's an example snippet formatted using Black:\n\n"
    "def format_name(first_name, last_name):\n"
    "    formatted_first_name = first_name.strip().title()\n"
    "    formatted_last_name = last_name.strip().title()\n"
    "    return f\"{formatted_first_name} {formatted_last_name}\"\n\n"
    "Ensure the code is formatted according to Black's uncompromising style. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface."
)

RADON_PROMPT = (    "Act as a Python developer and write a Python program with a focus on maintainable and low-complexity code as measured by radon. "
    "Here's a example snippet with low cyclomatic complexity:\n\n"
    "# Example Snippet for Radon\n"
    "def fibonacci(n):\n"
    "    \"\"\"Return the nth Fibonacci number.\"\"\"\n"
    "    if n <= 1:\n"
    "        return n\n"
    "    return fibonacci(n - 1) + fibonacci(n - 2)\n\n"
    "def main():\n"
    "    for i in range(10):\n"
    "        print(fibonacci(i))\n\n"
    "if __name__ == \"__main__\":\n"
    "    main()\n\n"
    "Strive for a simple and clear code structure, minimizing cyclomatic complexity. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")

PYDOCSTYLE_PROMPT = (    "Act as a Python developer and write a Python program that strictly adheres to the pydocstyle standard for docstrings. "
    "Here's an example snippet:\n\n"
    "\"\"\"Module for demonstrating pydocstyle adherence.\n\n"
    "This module provides examples of how to write docstrings that conform to pydocstyle standards.\n"
    "\"\"\"\n\n"
    "def add_numbers(x, y):\n"
    "    \"\"\"Add two numbers and return the result.\n\n"
    "    :param x: The first number to add.\n"
    "    :param y: The second number to add.\n"
    "    :return: The sum of x and y.\n"
    "    \"\"\"\n"
    "    return x + y\n\n"
    "Focus on comprehensive and compliant docstring documentation. "
    "Return only the raw code for the Python program, ensuring it's functional and follows Python best practices. "
    "Verify the program's correctness as if using a Command Line Interface.")
ADDITIONAL_PROMPT_SPECIFICATIONS = "Remember to only respond with the raw code for the Python program. Generate a Python program that uses the keyword(s) for inspiration on the type of problem to solve. Only return the code that you would write in a .py file. Do not output in Markdown format.\n"