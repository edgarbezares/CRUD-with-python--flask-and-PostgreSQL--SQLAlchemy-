 #Clase con WTForms
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class LibroForm(FlaskForm):
    nombre=StringField('Nombre',validators=[DataRequired()])
    autor=StringField('Autor', validators=[DataRequired()])
    year=IntegerField('Año', validators=[DataRequired()])
    enviar=SubmitField('Enviar')