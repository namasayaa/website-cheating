from flask import Blueprint, render_template, request,flash, redirect, url_for
from .model import Using
from website.form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from ._init_ import bcrypt

views = Blueprint('views', __name__, template_folder='templete')

@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('app.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Using.query.filter_by(username=form.username.data).first()
        if  user and bcrypt.check_password_hash(user.password_hash, form.password.data
        ):
            login_user(user, remember=True)
            flash(f'Sukses! Kamu masuk sebagai: { user.username}', category="success")
            return redirect(url_for('app.dashboard'))
        else:
            flash('Username dan Password tidak cocok! Silakan Coba Lagi', category="error")

    # if request.method == 'POST':
    #         username = request.form.get('username')
    #         password_hash = request.form.get('password')
    #         user = Using.query.filter_by(username=username).first()
    #         if user:
    #             if check_password_hash(user.password_hash, password_hash):
    #                 login_user(user, remember=True)
    #                 flash(f'Logged in successfully as {username}', category='success')
    #                 return redirect(url_for('app.dashboard'))
    #             else:
    #                 flash('Incorrect password, try again.', category='error')
    #         else:
    #             flash('username or email doesn\'t exist', category='error')


    return render_template("login.html", form=form, boolean=True)

            

    