from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class CensusForm(FlaskForm):
    entry_date = DateField('Date', validators=[DataRequired()])
    # Morning Old Cases
    m_old_male = IntegerField('Morning Old Male', default=0, validators=[NumberRange(min=0)])
    m_old_female = IntegerField('Morning Old Female', default=0, validators=[NumberRange(min=0)])
    m_old_child = IntegerField('Morning Old Child', default=0, validators=[NumberRange(min=0)])
    # Morning New Cases
    m_new_male = IntegerField('Morning New Male', default=0, validators=[NumberRange(min=0)])
    m_new_female = IntegerField('Morning New Female', default=0, validators=[NumberRange(min=0)])
    m_new_child = IntegerField('Morning New Child', default=0, validators=[NumberRange(min=0)])
    # Evening Old Cases
    e_old_male = IntegerField('Evening Old Male', default=0, validators=[NumberRange(min=0)])
    e_old_female = IntegerField('Evening Old Female', default=0, validators=[NumberRange(min=0)])
    e_old_child = IntegerField('Evening Old Child', default=0, validators=[NumberRange(min=0)])
    # Evening New Cases
    e_new_male = IntegerField('Evening New Male', default=0, validators=[NumberRange(min=0)])
    e_new_female = IntegerField('Evening New Female', default=0, validators=[NumberRange(min=0)])
    e_new_child = IntegerField('Evening New Child', default=0, validators=[NumberRange(min=0)])
    submit = SubmitField('Submit Census Entry')
