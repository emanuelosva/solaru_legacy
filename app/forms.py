"""Solaru app forms."""

# Flask
from flask_wtf import FlaskForm
from wtforms.fields import FloatField, SubmitField
from wtforms.validators import DataRequired, ValidationError


# Messages
message_is_positive = 'El número debe ser positivo'
message_is_numeric = 'El valor debe ser numérico'
message_bound_latitude = 'La latitud debe estar entre -80 y 80'
message_bound_longitude = 'La longitud debe estar entre -180 y 180'


# Validators
def is_positive(form, field):
    """Verificate if data is positive."""
    if field.data < 0:
        raise ValidationError(message_is_positive)


def is_numeric(form, field):
    """"Verificates if data is numeric."""
    data = str(field.data)
    if data.isalpha():
        raise ValidationError(message_is_numeric)


def bound_latitude(form, field):
    """Verificates if latitude is inside bounds."""
    bound = (field.data > -80) & (field.data <= 80)
    if not bound:
        raise ValidationError(message_bound_latitude)


def bound_longitude(form, field):
    """Verificates if latitude is inside bounds."""
    bound = (field.data > -180) & (field.data <= 180)
    if not bound:
        raise ValidationError(message_bound_longitude)


# Form
class DataToCalcForm(FlaskForm):
    """
    Form for adquire needed data for calculations.
    """

    latitude = FloatField(
        'Latitud (°)',
        validators=[DataRequired(), is_numeric, bound_latitude]
    )

    longitude = FloatField(
        'Longitud (°)',
        validators=[DataRequired(), is_numeric, bound_longitude]
    )

    width = FloatField(
        'Ancho disponible [m]',
        validators=[DataRequired(), is_positive, is_numeric]
    )

    height = FloatField(
        'Largo disponible [m]',
        validators=[DataRequired(), is_positive, is_numeric]
    )

    mean_consume = FloatField(
        'Consumo medio [kWh]',
        validators=[DataRequired(), is_positive, is_numeric]
    )

    kwh_cost = FloatField(
        'Costo del kWh [MXN]',
        validators=[DataRequired(), is_positive, is_numeric]
    )

    submit = SubmitField('Calcular')
