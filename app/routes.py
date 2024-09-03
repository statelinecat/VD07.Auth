from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, EditProfileForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# @app.route('/edit', methods=['GET', 'POST'])
# def edit():
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Вы успешно изменили свои данные!', 'success')
#         return redirect(url_for('login'))
#     return render_template('edit.html', form=form, title='Edit')

# @app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = ProfileForm(current_user.username, current_user.email)
#
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#
#         if form.new_password.data:
#             current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
#
#         db.session.commit()
#         flash('Профиль успешно обновлен!', 'success')
#         return redirect(url_for('account'))
#
#     return render_template('edit_profile.html', form=form, title='Edit Profile')


# class ProfileForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     email = EmailField('Email', validators=[DataRequired(), Email()])
#     new_password = PasswordField('New Password', validators=[Optional(), EqualTo('confirm_password')])
#     confirm_password = PasswordField('Confirm Password', validators=[EqualTo('new_password')])
#
#     def __init__(self, username, email, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.username.data = username
#         self.email.data = email


@app.route('/delete_account')
@login_required
def delete_account():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Ваш аккаунт был удален.', 'warning')
    return redirect(url_for('home'))

@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Ваш профиль был обновлен!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_account.html', form=form, title='Edit Account')