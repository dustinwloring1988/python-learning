import ast
import traceback

def execute_user_code(user_code, input_data):
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
