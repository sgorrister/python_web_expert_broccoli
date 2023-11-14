import json

from flask import Flask, render_template, request, redirect, url_for
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
    if request.method == 'POST':
        skill_name = request.form.get('skill_name')
        for i, skill in enumerate(my_skills):
            if skill_name.lower() in skill.lower():
                return redirect(url_for('display_skill', id=i))
        return "Навичка не знайдена."

    return render_template('skills.html', my_skills=my_skills)


@app.route('/skills/<int:id>')
def display_skill(id):
    if 0 <= id < len(my_skills):
        return f"Навичка з id {id}: {my_skills[id]}"
    else:
        return "Навичка не знайдена."


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_data and users_data[username]['password'] == password:
            return redirect(url_for('info',username=username))
        else:
            error = 'Невірне ім\'я користувача або пароль'
            return render_template('login.html', error=error)

    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('login.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/info/<username>')
def info(username):
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('info.html',username=username,os_info=os_info, user_agent=user_agent, current_time=current_time)
