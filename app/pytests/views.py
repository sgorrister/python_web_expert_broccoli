from datetime import date

import pytest
from flask import url_for

from app import create_app, db
from app.models import User
from app.posts.models import Tag, Category, Post
from config import TestConfig

@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='module')
def tags():
    tags = [Tag(name='games'),  Tag(name='coding'),  Tag(name='video'),  Tag(name='tests')]
    yield tags

@pytest.fixture(scope='module')
def default_user():
    user = User(email='test_user@gmail.com', username='test_user')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()
    yield user

@pytest.fixture(scope='module')
def init_db(default_user, posts, categories):
    db.create_all()

    user =User(
        email="test_user2@gmail.com",
        username="test_user2",
        password="testpass"
    )

    user.posts = [posts[2]]
    default_user.posts = [posts[0], posts[1]]

    db.session.add_all([default_user, user])

    for category in categories:
        db.session.add(category)

    db.session.commit()

    yield

@pytest.fixture(scope='function')
def auth_user(client, default_user, init_db):
    client.post(
        url_for('auth.login'),
        data={'login': default_user.email, 'password': 'testpass', "remember": True},
        follow_redirects=True
    )

    yield default_user

    client.post(url_for('auth.logout'))

@pytest.fixture(scope='module')
def categories():
    categories = [Category(name='Development'), Category(name='Java'), Category(name="Test")]
    yield categories

@pytest.fixture(scope='module')
def posts(categories, tags):
    yield [
        Post(title='New post test 1', text='New post test 1', created=date(2023, 12, 7),
               category=categories[0], tags=[tags[0]], user_id=1),

        Post(title='New post test 2', text='New post test 2', created=date(2023, 12, 7),
               category=categories[0], tags=[tags[0], tags[1]], user_id=0),

        Post(title='New post test 3', text='New post test 3', created=date(2023, 12, 7),
               category=categories[1], tags=[tags[2], tags[3]], user_id=0)
    ]

def test_all_post_view(client, auth_user):
    response = client.get(url_for('posts.all_posts'), follow_redirects=True)

    assert response.status_code == 200
    assert 'Posts' in response.text
    assert 'Create post' in response.text
    assert f'<form action="{url_for("posts.all_posts")}' in response.text

def test_post_create_view(client, auth_user):
    response = client.get(url_for('posts.create_post'), follow_redirects=True)

    assert response.status_code == 200
    assert 'Create post' in response.text
    assert f'<form action="{url_for("posts.create_post")}' in response.text

def test_post_by_id_view(client, auth_user, init_db):
    post = Post.query.get(1)
    response = client.get(url_for('posts.get_post', id=1), follow_redirects=True)

    assert response.status_code == 200

    if post.user_id == auth_user.id:
        assert f'<a href="{url_for("posts.update_post", id=1)}">' in response.text
        assert f'<a href="{url_for("posts.delete_post", id=1)}">' in response.text
    else:
        assert f'<a href="{url_for("posts.update_post", id=1)}">' not in response.text
        assert f'<a href="{url_for("posts.delete_post", id=1)}">' not in response.text

    assert str(post.created) in response.text

def test_post_edit_view(client, auth_user):
    response = client.get(url_for('posts.update_post', id=1), follow_redirects=True)

    assert response.status_code == 200
    assert 'Edit post' in response.text
    assert f'<form action="{url_for("posts.update_post", id=1)}' in response.text

def test_create_post(client, auth_user):
    response = client.post(url_for('posts.create_post'), data={
        'title': 'Test Post',
        'text': 'This is a test post content',
        'category': '1'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Test Post' in response.text
    assert 'This is a test post content' in response.text

def test_update_post(client, auth_user, init_db):
    old_post = Post.query.first()

    data = {
        "title": "New best title",
        "text": "Very coool text",
        "image": old_post.image,
        "category": Category.query.get(1).id,
        "tags": [tag.name for tag in old_post.tags],
        "enable": old_post.enable
    }

    response = client.post(url_for('posts.update_post', id=old_post.id), data=data, follow_redirects=True)

    assert response.status_code == 200

    post = Post.query.get(old_post.id)

    assert post.title == data["title"]
    assert post.text == data["text"]
    assert post.category.id == data["category"]

def test_delete_post(client, auth_user, init_db):
    post = Post.query.first()
    response = client.get(url_for('posts.delete_post', id=post.id), follow_redirects=True)

    assert response.status_code == 200
    assert 'Post successfully deleted' in response.text
    assert Post.query.get(post.id) is None
