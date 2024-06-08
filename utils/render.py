from flask import render_template_string

def render_template(html_template, **kwargs):
    """
    Render an HTML template using the provided template string and keyword arguments.

    Parameters:
        html_template (str): The HTML template string to render.
        **kwargs: Keyword arguments to pass to the template for rendering.

    Returns:
        str: The rendered HTML string.

    This function takes an HTML template string and keyword arguments, and uses the Flask `render_template_string` function to render the template with the provided arguments. The rendered HTML string is then returned.

    Example usage:
        template_string = "<html><body><h1>{{ title }}</h1></body></html>"
        rendered_html = render_template(template_string, title="Hello, World!")
        print(rendered_html)  # Output: "<html><body><h1>Hello, World!</h1></body></html>"
    """
    return render_template_string(html_template, **kwargs)
