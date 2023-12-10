import json
import os
import platform
import secrets
from datetime import datetime
from os.path import join, dirname, realpath

from PIL import Image
from flask import current_app
from flask import render_template, redirect, url_for, session, request, make_response, flash
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from . import app, db
from .forms import LoginForm, ChangePasswordForm, TodoForm, RegistrationForm, UpdateAccountForm, ResetPasswordForm
from .models import Todo, User

navigation = {
    'Про мене': 'portfolio.home',
    'Проєкти': 'portfolio.page2',
    'Контакти': 'portfolio.page3',
    'Skills': 'portfolio.display_skills',
    'todo': 'todos',
    'all users': 'users'
}
dataJsonPath = join(dirname(realpath(__file__)), 'users.json')
with open(dataJsonPath, 'r+') as f:
    users_data = json.load(f)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     os_info = platform.platform()
#     user_agent = request.headers.get('User-Agent')
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#
#         if username in users_data and users_data[username]['password'] == password:
#
#             if form.remember.data:
#                 session['username'] = username
#                 flash('Ви успішно увійшли!', 'success')
#                 return redirect(url_for('info', username=username))
#             else:
#                 flash('Ви успішно увійшли але вас ніхто ніколи не згадає!', 'success')
#                 return redirect(url_for('page1', username=username))
#         else:
#             flash('Невірне ім\'я користувача або пароль', 'danger')
#
#     return render_template('login.html', os_info=os_info, user_agent=user_agent,
#                            current_time=current_time, form=form, navigation=navigation)




@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))


@app.route('/change_password/<username>', methods=['POST'])
def change_password(username):
    if 'username' in session and session['username'] == username:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            users_data[username]['password'] = new_password

            with open(dataJsonPath, 'w') as f:
                json.dump(users_data, f, indent=2)

            flash('Пароль успішно змінено!', 'success')
            return redirect(url_for('info', username=username))

    return redirect(url_for('login'))


@app.route('/todos')
def todos():
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos, navigation=navigation)


@app.route('/todo/<int:todo_id>')
def todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return render_template('todo.html', todo=todo, navigation=navigation)


@app.route('/add_todo', methods=['GET', 'POST'])
def add_todo():
    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('todos'))

    return render_template('add_todo.html', form=form, navigation=navigation)


@app.route('/delete_todo/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('todos'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ця електронна адреса вже зайнята. Будь ласка, виберіть іншу.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        try:
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Помилка бази даних. Спробуйте ще раз.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form, navigation=navigation)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Успішний вхід!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Невірна електронна адреса або пароль. Спробуйте ще раз.', 'danger')

    return render_template('login.html', title='Login', form=form, navigation=navigation)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users, navigation=navigation)


def save_picture(form_picture):
    # Generate a random filename to avoid collisions
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    # Save the resized image
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    reset_form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif reset_form.validate_on_submit():
        if current_user.check_password(reset_form.old_password.data):
            current_user.set_password(reset_form.password.data)
            db.session.commit()
            flash('Your password has been reset!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid password', 'danger')
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, reset_form=reset_form,
                           navigation=navigation)


@app.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while updating user last seen!', 'danger')
    return response
