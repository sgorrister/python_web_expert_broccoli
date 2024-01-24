import unittest
from flask import url_for
from flask_testing import TestCase
from .. import create_app, db

class TestViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection in testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get(url_for('portfolio.home'))
        self.assert200(response)
        self.assert_template_used('page1.html')

    def test_registration_page(self):
        response = self.client.get(url_for('accounting.register'))
        self.assert200(response)
        self.assert_template_used('register.html')

    def test_login_page(self):
        response = self.client.get(url_for('accounting.login'))
        self.assert200(response)
        self.assert_template_used('login.html')

    def test_cookies_info_page(self):
        response = self.client.get(url_for('cookies.info', username='testuser'))
        self.assert200(response)
        self.assert_template_used('info.html')

    def test_feedback_page(self):
        response = self.client.get(url_for('feedback.feedback'))
        self.assert200(response)
        self.assert_template_used('feedback.html')

    def test_portfolio_page(self):
        response = self.client.get(url_for('portfolio.page1'))
        self.assert200(response)
        self.assert_template_used('page1.html')

    def test_list_posts_page(self):
        response = self.client.get(url_for('posts.list_posts'))
        self.assert200(response)
        self.assert_template_used('list_posts.html')


if __name__ == '__main__':
    unittest.main()
