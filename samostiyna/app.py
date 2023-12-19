import platform
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from forms import FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SECRET_KEY'] = '***'

my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'Bootstrap', 'JavaScript', 'SQL']
db = SQLAlchemy(app)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    liked = db.Column(db.Boolean, nullable=True, default=False)

    def __init__(self, name, feedback_text, liked):
        self.name = name
        self.feedback_text = feedback_text
        self.liked = liked


m = Migrate(app, db)


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


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        feedback_text = form.feedback_text.data
        liked = form.liked.data

        feedback = Feedback(name=name, feedback_text=feedback_text, liked=liked)

        db.session.add(feedback)
        db.session.commit()

        flash('Ваш відгук було збережено!', 'success')
        return redirect(url_for('feedback.feedback'))


    feedbacks = Feedback.query.all()

    return render_template('feedback.html', form=form, feedbacks=feedbacks)


if __name__ == '__main__':
    app.run(debug=True)
