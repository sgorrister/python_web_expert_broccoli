import platform
from datetime import datetime

from flask import request, make_response, redirect, url_for, flash, render_template

from app.cookies import cookies_bp

from config import navigation


@cookies_bp.route('/info/<username>', methods=['GET', 'POST'])
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
                flash('Cookie додано успішно!', 'success')
                return response

        elif 'remove_cookie_button' in request.form:
            key_to_remove = request.form.get('key_to_remove')

            if key_to_remove:
                response = make_response(redirect(url_for('info', username=username)))
                response.delete_cookie(key_to_remove)
                flash('Cookie видалено успішно!', 'success')
                return response

        elif 'remove_all_cookies_button' in request.form:
            response = make_response(redirect(url_for('info', username=username)))

            for key, _ in current_cookies:
                response.delete_cookie(key)
                flash('Усі Cookie видалено успішно!', 'success')
            return response

    return render_template('info.html', username=username, os_info=os_info, user_agent=user_agent,
                           current_time=current_time, current_cookies=current_cookies, navigation=navigation)
