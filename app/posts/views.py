from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from . import posts_bp
from .. import db
from .models import Post, Category, Tag
from .forms import PostForm
from .forms import CategoryForm

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
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        tags_input = form.tags.data
        tags_list = [tag.strip()[1:] for tag in tags_input.split(',') if tag.strip().startswith('#')]
        post_tags = []
        for tag_name in tags_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            post_tags.append(tag)

        post = Post(
            title=form.title.data,
            text=form.text.data,
            user_id=current_user.id,
            category_id=form.category.data,
            tags=post_tags

        )
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('create_post.html', title='Create Post', form=form, navigation=navigation)


@posts_bp.route("/post", methods=['GET'])
def list_posts():
    posts = Post.query.all()
    categories = Category.query.all()  # Added to pass categories to the template

    return render_template('list_posts.html', title='List Posts', posts=posts, navigation=navigation)

@posts_bp.route("/post/<int:id>", methods=['GET'])
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('view_post.html', title=post.title, post=post, navigation=navigation)


@posts_bp.route("/post/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.options(joinedload(Post.category)).get_or_404(id)

    # Check if the current user is the author of the post
    if current_user.id != post.user_id:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('posts.list_posts'))

    form = PostForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.category_id = form.category.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('posts.list_posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
        form.category.data = post.category_id

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

@posts_bp.route("/category/create", methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('create_category.html', title='Create Category', form=form, navigation=navigation)

@posts_bp.route("/category/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('posts.list_posts'))
    elif request.method == 'GET':
        form.name.data = category.name
    return render_template('update_category.html', title='Update Category', form=form, navigation=navigation)

@posts_bp.route("/category/<int:id>/delete", methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return redirect(url_for('posts.list_posts'))