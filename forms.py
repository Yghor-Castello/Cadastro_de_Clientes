# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, Length
#
#
# class FormCliente(FlaskForm):
#     nome = StringField('Nome de Usúario')
#     cpf = StringField('CPF', validators=[DataRequired(), Length(11)])
#     endereco = StringField('Endereço')
#     botao_add_cadastrar = SubmitField('Add Cliente')
#
#
# class FormCarros(FlaskForm):
#     carro = StringField('Carro')
#     modelo = StringField('Modelo')
#     cor = StringField('Cor')
#     botao_add_carros = SubmitField('Add Carros')
#
#     csrf token