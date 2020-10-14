"""Entry point for Solaru App."""

# Flask
from flask import render_template, url_for

# Local
from app import app_factory
from app.forms import DataToCalcForm
from app.models import CalcActive

# Create app
app = app_factory()


# Error handlers
@app.errorhandler(404)
def not_fount(error):
    """Return template for not found URL"""

    return render_template('error_404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    """Return template for not found URL"""

    return render_template('error_500.html', error=error)


# Principal view
@app.route('/', methods=['GET', 'POST'])
def index():
    """Principal View."""

    data_form = DataToCalcForm()
    calc = CalcActive()
    context = {'data_form': data_form, 'calc': calc}

    if data_form.is_valid():
        data = data_form.get_data()
        calc.activate(**data)
        return render_template('post.html', **context)

    return render_template('index.html', **context)


if __name__ == "__main__":
    app.run()
