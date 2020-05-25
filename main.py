"""Entry point for Solaru App."""

# Flask
from flask import redirect, render_template, url_for, make_response

# Local
from app import app_factory
from app.forms import DataToCalcForm
from app.models import CalcActive

# Create app
app = app_factory()


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
