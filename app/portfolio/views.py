import platform
from datetime import datetime

from flask import render_template, flash, redirect, url_for, request

from . import portfolio_bp

from config import navigation


@portfolio_bp.route('/')
def home():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = None

    return render_template('page1.html', os_info=os_info, user_agent=user_agent, current_time=current_time,
                           username=username, is_home=True, navigation=navigation)


@portfolio_bp.route('/page1')
def page1():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = None
    return render_template('page1.html', os_info=os_info, user_agent=user_agent, current_time=current_time,
                           username=username, is_home=True, navigation=navigation)


@portfolio_bp.route('/page2')
def page2():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page2.html', os_info=os_info, user_agent=user_agent, current_time=current_time,
                           navigation=navigation)


@portfolio_bp.route('/page3')
def page3():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page3.html', os_info=os_info, user_agent=user_agent, current_time=current_time,
                           navigation=navigation)


@portfolio_bp.route('/skills', methods=['GET', 'POST'])
def display_skills():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        skill_name = request.form.get('skill_name')
        for i, skill in enumerate(my_skills):
            if skill_name.lower() in skill.lower():
                flash(f"Навичка '{skill}' знайдена!", 'success')
                return redirect(url_for('portfolio.display_skill', id=i))

        flash("Навичка не знайдена.", 'danger')

    return render_template('skills.html', my_skills=my_skills, os_info=os_info, user_agent=user_agent,
                           current_time=current_time, navigation=navigation)


@portfolio_bp.route('/skills/<int:id>')
def display_skill(id):
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 0 <= id < len(my_skills):
        return f"Навичка з id {id}: {my_skills[id]}"
    else:
        return "Навичка не знайдена."
