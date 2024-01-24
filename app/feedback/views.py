from flask import render_template, redirect, url_for, flash

from app.feedback import feedback_bp
from .forms import FeedbackForm
from ..models import db, Feedback

from config import navigation



@feedback_bp.route('/feedback', methods=['GET', 'POST'])
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

    return render_template('feedback.html', form=form, feedbacks=feedbacks, navigation=navigation)
