from flask import Flask, render_template, request, redirect, url_for
import platform
from datetime import datetime

app = Flask(__name__)

my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'Bootstrap', 'JavaScript', 'SQL']

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

if __name__ == '__main__':
    app.run(debug=True)
