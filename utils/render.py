from flask import render_template_string

def render_template(html_template, **kwargs):
    return render_template_string(html_template, **kwargs)
