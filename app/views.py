from flask import render_template, redirect, url_for, flash

from . import app, db
from .models import Todo

navigation = {
    'Про мене': 'portfolio.home',
    'Проєкти': 'portfolio.page2',
    'Контакти': 'portfolio.page3',
    'Skills': 'portfolio.display_skills',
    'todo': 'todos',
    'all users': 'accounting.users'
}


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



