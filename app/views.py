import json

from flask import Flask, render_template, request, redirect, url_for, session, request, make_response

from os.path import join, dirname, realpath

from app import app
import platform
from datetime import datetime

my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'Bootstrap', 'JavaScript', 'SQL']

dataJsonPath = join(dirname(realpath(__file__)), 'users.json')
with open(dataJsonPath, 'r+') as f:
    users_data = json.load(f)


@app.route('/')
def home():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/page1')
def page1():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/page2')
def page2():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page2.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/page3')
def page3():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page3.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/skills', methods=['GET', 'POST'])
def display_skills():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        skill_name = request.form.get('skill_name')
        for i, skill in enumerate(my_skills):
            if skill_name.lower() in skill.lower():
                return redirect(url_for('display_skill', id=i))
        return "Навичка не знайдена."

    return render_template('skills.html', my_skills=my_skills, os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/skills/<int:id>')
def display_skill(id):
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 0 <= id < len(my_skills):
        return f"Навичка з id {id}: {my_skills[id]}"
    else:
        return "Навичка не знайдена."


@app.route('/login', methods=['GET', 'POST'])
def login():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_data and users_data[username]['password'] == password:
            session['username'] = username  # Збереження ім'я користувача в сесії
            return redirect(url_for('info', username=username))
        else:
            error = 'Невірне ім\'я користувача або пароль'
            return render_template('login.html', error=error)

    return render_template('login.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/info/<username>', methods=['GET', 'POST'])
def info(username):
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_cookies = request.cookies.items()

    if request.method == 'POST':
        if 'add_cookie_button' in request.form:
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            expire_time = request.form.get('expire_time')

            if key and value and expire_time:
                response = make_response(redirect(url_for('info', username=username)))
                response.set_cookie(key, value, max_age=int(expire_time))
                return response

        elif 'remove_cookie_button' in request.form:
            key_to_remove = request.form.get('key_to_remove')

            if key_to_remove:
                response = make_response(redirect(url_for('info', username=username)))
                response.delete_cookie(key_to_remove)
                return response

        elif 'remove_all_cookies_button' in request.form:
            response = make_response(redirect(url_for('info', username=username)))

            for key, _ in current_cookies:
                response.delete_cookie(key)

            return response

    return render_template('info.html', username=username, os_info=os_info, user_agent=user_agent,
                           current_time=current_time, current_cookies=current_cookies)
@app.route('/logout', methods=['POST'])
def logout():
    # Видалення інформації про користувача з сесії
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/change_password/<username>', methods=['POST'])
def change_password(username):
    if 'username' in session and session['username'] == username:
        # Assuming users_data is a global dictionary containing user data
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            # Update the password in your users_data dictionary
            users_data[username]['password'] = new_password

            # Save the updated users_data dictionary to your file or database
            with open(dataJsonPath, 'w') as f:
                json.dump(users_data, f, indent=2)

            # Redirect to the info page with the updated password
            return redirect(url_for('info', username=username))

    # If the user is not logged in or does not match the username, redirect to login
    return redirect(url_for('login'))