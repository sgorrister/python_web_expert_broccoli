import unittest
from flask import url_for
from flask_login import current_user
from flask_testing import TestCase
from .. import create_app, db
from ..models import User

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

    def test_registration(self):
        response = self.client.post(
            url_for('accounting.register'),
            data={'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword',
                  'confirm_password': 'testpassword'},
            follow_redirects=True
        )
        self.assert200(response)
        self.assert_template_used('login.html')
        self.assertTrue(User.query.filter_by(username='testuser').first())

    def test_login(self):
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(
            url_for('accounting.login'),
            data={'email': 'testuser@example.com', 'password': 'testpassword'},
            follow_redirects=True
        )
        self.assert200(response)
        self.assert_template_used('page1.html')
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        # Assuming you have a test user in the database
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post(
            url_for('accounting.login'),
            data={'email': 'testuser@example.com', 'password': 'testpassword'},
            follow_redirects=True
        )

        response = self.client.get(url_for('accounting.logout'), follow_redirects=True)

        self.assert200(response)
        self.assert_template_used('page1.html')
        self.assertFalse(current_user.is_authenticated)

    def test_update_profile(self):
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post(
            url_for('accounting.login'),
            data={'email': 'testuser@example.com', 'password': 'testpassword'},
            follow_redirects=True
        )

        response = self.client.post(
            url_for('accounting.account'),
            data={'username': 'newusername', 'email': 'newemail@example.com', 'about_me': 'new about me'},
            follow_redirects=True
        )
        self.assert200(response)
        self.assert_template_used('account.html')
        updated_user = User.query.filter_by(username='newusername').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertEqual(updated_user.about_me, 'new about me')

if __name__ == '__main__':
    unittest.main()