from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from . import posts_bp
from .. import db
from .models import Post
from .forms import PostForm
navigation = {
    'Про мене': 'portfolio.home',
    'Проєкти': 'portfolio.page2',
    'Контакти': 'portfolio.page3',
    'Skills': 'portfolio.display_skills',
    'todo': 'todos.todos',
    'all users': 'accounting.users',
    'feedback': 'feedback.feedback'
}
@posts_bp.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            text=form.text.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('create_post.html', title='Create Post', form=form, navigation=navigation)

@posts_bp.route("/post", methods=['GET'])
def list_posts():
    posts = Post.query.all()
    return render_template('list_posts.html', title='List Posts', posts=posts, navigation=navigation)

@posts_bp.route("/post/<int:id>", methods=['GET'])
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('view_post.html', title=post.title, post=post, navigation=navigation)

@posts_bp.route("/post/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)

    # Check if the current user is the author of the post
    if current_user.id != post.user_id:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('posts.list_posts'))

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('posts.list_posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
    return render_template('update_post.html', title='Update Post', form=form, navigation=navigation, post=post)

@posts_bp.route("/post/<int:id>/delete", methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    # Check if the current user is the author of the post
    if current_user.id != post.user_id:
        flash('You are not authorized to delete this post.', 'danger')
        return redirect(url_for('posts.list_posts'))

    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!', 'success')
    return redirect(url_for('posts.list_posts'))
