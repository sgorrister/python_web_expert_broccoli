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
    skill_name = request.args.get('skill_name')
    if skill_name is not None:
        for skill in my_skills:
            if skill_name.lower() in skill.lower():
                return render_template('skills.html', skill=skill)
        return render_template('skills.html', skill=None)

    return render_template('skills.html', my_skills=my_skills)



if __name__ == '__main__':
    app.run(debug=True)
