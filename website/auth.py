from flask import Blueprint, render_template, request,flash, redirect, url_for
from .model import Using
from .form import RegisterForm, ResetRequestPassword, ChangePassword
from ._init_ import db, mail, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message

auth = Blueprint('views', __name__,template_folder='templete')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_to_create = Using(name=form.name.data,username=form.username.data,
                               email=form.email_address.data,
                               password_hash=hashed_password)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Akun berhasil dibuat: {form.username.data}', category='success')
        return redirect(url_for('view.home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Terjadi error dalam pembuatan akun: {err_msg}', category='error')
    return render_template("signup.html", form=form)

def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', sender='dontrepthis@gmail.com' ,recipients=[user.email])
    msg.body=f''' To reset your password. Please follow this link below.
    
    {url_for('auth.reset_token',token=token,_external=True)}

    if you din't send a password reset request. Please ignore this message.

    '''
    mail.send(msg)

@auth.route('/requestresetpassword', methods=['GET', 'POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = ResetRequestPassword()
    if form.validate_on_submit():
        user = Using.query.filter_by(email=form.email_address.data).first()
        if user:
            send_mail(user)
            flash('Permintaan reset password telah terkirim.Silakan cek email anda.', category='success')
            return redirect(url_for('view.home'))
    return render_template("resetpass.html", form=form)

@auth.route('/requestresetpassword/<token>',  methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    user = Using.verify_reset_token(token)
    if user is None:
        flash('Token sudah tidak valid atau kadaluwarsa. silakan coba lagi', category='error')
        return redirect(url_for('auth.reset'))
    form = ChangePassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_password
        db.session.commit()
        flash('Password behasil diubah! Silahkan Login!', category='success')
        return redirect(url_for('view.home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Kata sandi tidak cocok! : {err_msg}', category='error')
    
    return render_template("resetpass2.html", user=current_user, form=form)

    