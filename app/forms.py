from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
#from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Workorder, Workcenter, Capac, Sched ,User_query

    

#login Miguel
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    newusername = StringField("newusername")
    newpassword = StringField("newpassword")
    numemploye = StringField("numemploye")
    id = StringField("id")
    name = StringField("name")
    surname = StringField("surname")
    type  =  StringField("type")  
    email  =  StringField("email")    
    modifier = SubmitField('Modifier')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name =  StringField("name")
    surname = StringField("surname") 
    numemploye = StringField("numemploye") 
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirmer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')