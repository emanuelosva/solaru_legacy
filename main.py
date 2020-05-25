"""Entry point for Solaru App."""

# Flask
from flask import redirect, render_template, url_for, make_response

# Local
from app import app_factory

# Create app
app = app_factory()


# Principal view
@app.route('/', methods=['GET', 'POST'])
def index():
    """Principal View."""

    return "Hello World."


if __name__ == "__main__":
    app.run()
