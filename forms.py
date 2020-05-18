from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email(),Length(min=4,max=25)])
    password = PasswordField('Password', validators=[InputRequired(),EqualTo('confirm',message='Passwords must match'),Length(min=6,max=35)])
    confirm = PasswordField('Confirm Password', validators=[Length(min=6,max=35)])
    submit = SubmitField('Submit')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email(),Length(min=4,max=25)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=6,max=35)])
    submit = SubmitField('Sign In')

class EditPetForm(FlaskForm):
    name = StringField("Pet's Name", validators = [InputRequired()])
    age = StringField("Pet's Age", validators = [InputRequired()])
    bio = StringField("Pet's Bio", validators = [InputRequired()])
    submit = SubmitField("Edit Pet")