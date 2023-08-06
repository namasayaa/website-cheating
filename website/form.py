from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TimeField, DateField, TextAreaField
from wtforms.validators import Length,Email, DataRequired, ValidationError, EqualTo, Optional, Regexp
from website.model import Using


class RegisterForm(FlaskForm):

        def validate_username(self, username_to_check):
             user = Using.query.filter_by(username=username_to_check.data).first()
             if user:
                  raise ValidationError('Username sudah ada! Silakan coba Username yang berbeda')
             
        def validate_email_address(self, email_address_to_check):
             email = Using.query.filter_by(email=email_address_to_check.data).first()
             if email:
                  raise ValidationError('Email sudah ada! Silakan coba Email yang berbeda')

        name = StringField(label='Name: ', validators=[Length(min=2, max=30), DataRequired()])
        username = StringField(label='Username: ', validators=[Length(min=2, max=30), DataRequired()])
        email_address = StringField(label='Email: ', validators=[Email(Length(min=4)), DataRequired()])
        password = PasswordField(label='Password: ', validators=[Length(min=5), DataRequired()])
        submit = SubmitField (label='Register')

class LoginForm(FlaskForm):
    username = StringField(label="Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Login')

class ResetRequestPassword(FlaskForm):
     email_address = StringField(label='Email: ', validators=[Email(Length(min=4)), DataRequired()])
     submit = SubmitField(label='Reset Password')

class ChangePassword(FlaskForm):
     password = PasswordField(label='New Password: ', validators=[Length(min=5), DataRequired()])
     confirm_password = PasswordField(label='Confirm Password:', validators=[Length(min=5), DataRequired(), EqualTo('password')])
     submit = SubmitField(label='Change Password')


class formulir(FlaskForm):
     nama_pengawas = StringField(label="Nama Pengawas:", validators=[DataRequired()])
     tanggal = DateField(label="Tanggal:", validators=[DataRequired()])
     jam = TimeField(label="Jam:", validators=[DataRequired()])
     ruangan = StringField(label="Ruangan:", validators=[DataRequired()])
     kelas = StringField(label="Kelas:", validators=[DataRequired()])
     matkul = StringField(label="Mata Kuliah:", validators=[DataRequired()])
     submit = SubmitField(label="Submit")

class pengaturan(FlaskForm):
    name = StringField(label="Nama:", validators=[])
    email_address = StringField(label='Email: ', validators=[Email(Length(min=4))])
    phone = StringField(label="Phone Number:", validators=[Optional(), Regexp(r'^$|^\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$')])
    bio = TextAreaField(label="Bio:", validators=[Optional()])
    old_password = PasswordField(label='Old Password:', validators=[Length(min=5), DataRequired()])
    new_password= PasswordField(label='New Password:', validators=[Length(min=5), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[Length(min=5), DataRequired()])
    submit = SubmitField(label="Update")

