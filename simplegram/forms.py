from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, TextAreaField, FileField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed

from simplegram.models.models import User

class LoginForm(FlaskForm):
    username = StringField('Nama user', validators=[DataRequired()])
    password = PasswordField('Kata sandi', validators=[DataRequired()])
    remember = BooleanField('Ingat saya')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email()])
    fullname = StringField('Nama lengkap', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(),Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    confirm = PasswordField('Konfirmasi', 
                            validators=[DataRequired(), 
                                        EqualTo('password', message='Password dan konfirmasi harus sama')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username tersebut sudah digunakan.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email tersebut sudah digunakan')

class PostForm(FlaskForm):
    post_id = HiddenField('id')
    image = FileField('Foto keren', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Deskripsi singkat', validators=[DataRequired()])
    submit = SubmitField('Tambah Postingan')

class EditPostForm(FlaskForm):
    description = TextAreaField('Deskripsi singkat', validators=[DataRequired()])
    submit = SubmitField('Edit Postingan')

class CommentForm(FlaskForm):
    user_id = HiddenField('user_id')
    post_id = HiddenField('post_id')
    comment = TextAreaField('Komentar', validators=[DataRequired()])
    submit = SubmitField('Tambah Komentar')
    
# Ini tambahan Kode saya
class ProfileForm(FlaskForm):
    fullname = StringField('Nama lengkap', validators=[DataRequired()])    
    profpic = FileField('Foto keren', validators=[FileAllowed(['jpg', 'png']), Optional()])
    description = TextAreaField('Deskripsi singkat')
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    confirm = PasswordField('Konfirmasi', validators=[EqualTo('password'), Optional()])
    submit = SubmitField('Simpan Profil')    

class MessageForm(FlaskForm):
    receiver_id = SelectField('Penerima', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Isi Pesan', validators=[DataRequired()])
    submit = SubmitField('Kirim Pesan')
