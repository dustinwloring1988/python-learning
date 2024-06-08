import requests
import json
import yaml
import os
import psycopg2

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

def save_to_database(challenge_data):
    """
    Saves the given challenge data to a PostgreSQL database.

    Args:
        challenge_data (list): A list of dictionaries representing challenges. Each dictionary should have the following keys:
            - "task" (str): The task description of the challenge.
            - "test_cases" (list): A list of test cases for the challenge. Each test case should be a dictionary with the following keys:
                - "inputs" (list): A list of input values for the test case.
                - "expected_output" (any): The expected output for the test case.

    Returns:
        None
    """
    # Check if all required environment variables are set
    required_env_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST"]
    missing_vars = [var for var in required_env_vars if os.getenv(var) is None]
    if missing_vars:
        error_message = f"The following environment variables are missing: {', '.join(missing_vars)}"
        raise ValueError(error_message)

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST")
        )
    except Exception as e:
        error_message = f"Failed to connect to the database: {str(e)}"
        raise ConnectionError(error_message)

    # Create a cursor
    cur = conn.cursor()

    # Insert challenges into the database
    for challenge in challenge_data:
        task = challenge.get("task", "")
        test_cases = json.dumps(challenge.get("test_cases", []))
        cur.execute("INSERT INTO challenge (task, test_cases) VALUES (%s, %s)",
                    (task, test_cases))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def main():
    """
    Sends a POST request to the local llama instance to generate hard-level Python challenges.
    The challenges are defined in the request payload and the response is a YAML file.
    The function checks if the request was successful and extracts the response JSON.
    The response string is cleaned by removing unnecessary characters.
    The YAML string is parsed into a Python dictionary and the 'challenges' key is removed.
    The function checks the saving method and saves the challenges based on the chosen method.
    If the saving method is "yaml", the challenges are saved to a YAML file.
    If the saving method is "db", the challenges are saved to the database.
    If the saving method is invalid, an error message is printed.
    If the request was not successful, an error message is printed.
    """
    # Define the request payload
    payload = {
        "model": "llama3",
        "prompt": "You run a Python challenge website and want to add more medium-level challenges to your platform. You need diverse and challenging problems to engage your users. Show the output as a yaml file, all responses will have a solve function that the user has to build as that is what we check. Generate 10 hard-level Python challenges, each with a task description and multiple test cases. <example> - task: 'Write a function named \'solve\' that takes a single integer input and returns its square.' test_cases: - inputs: [2] expected_output: 4 - inputs: [3] expected_output: 9 - inputs: [4] expected_output: 16 - task: 'Write a function named \'solve\' that takes two integers and returns their sum.' test_cases: - inputs: [1, 2] expected_output: 3 - inputs: [5, 7] expected_output: 12 - inputs: [0, 0] expected_output: 0 - task: 'Write a function named \'solve\' that takes a list of integers and returns the maximum value.' test_cases: - inputs: [[1, 2, 3, 4, 5]] expected_output: 5 - inputs: [[-1, -2, -3, -4]] expected_output: -1 - inputs: [[100, 50, 200, 150]] expected_output: 200 </example>",
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

        # Remove the 'challenges' key
        challenge_data = challenge_data.get('challenges', [])

        # Check the saving method
        save_method = os.getenv("SAVE_METHOD", "yaml")

        # Save challenges based on the chosen method
        if save_method == "yaml":
            save_to_yaml(challenge_data)
            print("Challenges saved to challenges.yaml")
        elif save_method == "db":
            save_to_database(challenge_data)
            print("Challenges saved to the database")
        else:
            print("Invalid saving method:", save_method)
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    main()
