import ast
import traceback

def execute_user_code(user_code, input_data):
    """
    Executes the user-provided code by creating a local namespace dictionary and running the code in that context. 
    If the 'solve' function is defined in the code, it is called with the provided input data. 
    If 'solve' is not defined, returns an error message. 
    If an exception occurs during execution, an error message with the exception details is returned.
    """
    local_vars = {}
    try:
        exec(user_code, {}, local_vars)
        if 'solve' in local_vars:
            result = local_vars['solve'](*input_data)
            return result
        else:
            return "Error: Your code must define a function named 'solve'."
    except Exception as e:
        return f"Error executing your code: {e}\n{traceback.format_exc()}"
