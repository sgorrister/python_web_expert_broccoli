import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'


navigation = {
    'Про мене': 'portfolio.home',
    'Проєкти': 'portfolio.page2',
    'Контакти': 'portfolio.page3',
    'Skills': 'portfolio.display_skills',
    'todo': 'todos.todos',
    'all users': 'accounting.users',
    'feedback': 'feedback.feedback',
    'Posts': 'posts.list_posts',
    'Create Post': 'posts.create_post'
}
