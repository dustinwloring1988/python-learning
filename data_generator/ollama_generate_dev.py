import requests
import json
import yaml
import os

def save_to_yaml(challenge_data):
    """
    Saves the challenge data to a YAML file.

    Args:
        challenge_data: The data to be saved to the YAML file.

    Returns:
        None
    """
    with open("challenges.yaml", "a", encoding="utf-8") as file:
        yaml.dump(challenge_data, file, allow_unicode=True)
        
def main():
    """
    Sends a POST request to the local llama instance to generate hard-level Python challenges.
    The challenges are defined in the request payload and the response is a YAML file.
    The function checks if the request was successful and extracts the response JSON.
    The response string is cleaned by removing unnecessary characters.
    The YAML string is parsed into a Python dictionary and the 'challenges' key is removed.
    The function checks the saving method and saves the challenges based on the chosen method.
    If the saving method is "yaml", the challenges are saved to a YAML file.
    If the saving method is invalid, an error message is printed.
    If the request was not successful, an error message is printed.
    """
    # Define the request payload
    payload = {
        "model": "llama3", #deepseek-coder:6.7b, #llama3:8b-instruct-q6_K, #llama3, #codegemma, #mistral, # The following will need trainied, #aya, #phi3:14b
        "prompt": "Below is an example of the entries in a YAML file for my Python challenge game. As an expert in this field, your task is to generate challenging Python exercises. Consider the following aspects when generating the challenges:\n\n1. Diversity of Concepts: Provide a range of challenges that cover different Python concepts such as data structures, functions, control flow, and object-oriented programming. Ensure that each challenge offers a unique problem-solving opportunity.\n\n2. Difficulty Levels: Generate challenges with varying difficulty levels (easy, medium, and hard) to cater to learners of different skill levels. The difficulty should be appropriately balanced to challenge but not overwhelm the participants.\n\n3. Real-World Relevance: Choose challenges that are relevant to real-world scenarios or common programming tasks. This helps learners understand the practical applications of Python programming and motivates them to solve the challenges.\n\n Make sure to include atleast 3 test_cases so the users can not check during the challanges.\n\n All answers need to use the solve function.\n\n <examples>\n\nExample 1:\n- task: Write a function named 'calculate_average' that takes a list of numbers as input and returns the average. Ensure that the function handles empty lists gracefully.\n  difficulty: easy\n  test_cases:\n  - expected_output: 3.0\n    inputs: [1, 2, 3, 4, 5]\n  - expected_output: 0.0\n    inputs: []\n\nReason: This example introduces participants to basic function creation and handling edge cases, such as an empty input list. It's categorized as easy to encourage beginners to get started.\n\nExample 2:\n- task: Implement a class named 'Employee' that represents an employee with attributes for name, age, and salary. Include methods to calculate yearly salary increase based on a given percentage and to display employee information.\n  difficulty: medium\n  test_cases:\n  - expected_output: \"John Doe, 30, $60000\"\n    inputs: [\"John Doe\", 30, 50000]\n  - expected_output: \"Mary Smith, 40, $72000\"\n    inputs: [\"Mary Smith\", 40, 60000]\n\nReason: This example introduces object-oriented programming concepts by defining a class and its methods. It's categorized as medium to challenge participants with some programming experience.\n\nExample 3:\n- task: Write a recursive function named 'fibonacci' that calculates the nth Fibonacci number. Optimize the function to use memoization for improved performance.\n  difficulty: hard\n  test_cases:\n  - expected_output: 55\n    inputs: [10]\n  - expected_output: 6765\n    inputs: [20]\n\nReason: This example offers a challenging problem that requires participants to understand recursion and memoization. It's categorized as hard to provide an advanced problem-solving opportunity.\n\n</examples>",
        "format": "json",
        "stream": False
    }

    # Send the HTTP POST request to the local llama instance
    response = requests.post("http://localhost:11434/api/generate", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response JSON from the HTTP response
        response_json = response.json()

        # Extract the response string from the response JSON
        response_string = response_json["response"]

        # Clean the response string by removing unnecessary characters
        cleaned_response = response_string.strip()

        # Parse the YAML string into a Python dictionary
        challenge_data = yaml.safe_load(cleaned_response)

        # Print the parsed challenge data to check its structure
        print("Parsed challenge data:", challenge_data)

        # Remove the 'challenges' key if it exists
        challenge_data = challenge_data.get('challenges', [])

        # Print the challenge data after removing the 'challenges' key
        print("Challenge data after removing 'challenges' key:", challenge_data)

        # Check the saving method
        save_method = os.getenv("SAVE_METHOD", "yaml")

        # Save challenges based on the chosen method
        if save_method == "yaml":
            save_to_yaml(challenge_data)
            print("Challenges saved to challenges.yaml")
        else:
            print("Invalid saving method:", save_method)
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    main()