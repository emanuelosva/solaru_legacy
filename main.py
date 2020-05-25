"""Entry point for Solaru App."""

# Flask
from flask import redirect, render_template, url_for, make_response

# Local
from app import app_factory
from app.forms import DataToCalcForm

# Create app
app = app_factory()


# Principal view
@app.route('/', methods=['GET', 'POST'])
def index():
    """Principal View."""

    data_form = DataToCalcForm()
    context = {
        'data_form': data_form
    }

    return render_template('index.html', **context)


if __name__ == "__main__":
    app.run()
