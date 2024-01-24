import unittest
from flask import url_for
from flask_testing import TestCase
from .. import create_app, db
from ..models import User

class TestAuthenticationViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self, email, password):
        response = self.client.post(
            url_for('accounting.register'),
            data=dict(email=email, password=password),
            follow_redirects=True
        )
        return response

    def login_user(self, email, password):
        response = self.client.post(
            url_for('accounting.login'),
            data=dict(email=email, password=password),
            follow_redirects=True
        )
        return response

    def logout_user(self):
        response = self.client.get(url_for('accounting.logout'), follow_redirects=True)
        return response

    def test_register_and_login(self):
        # Register user
        response = self.register_user('testuser@example.com', 'password')
        self.assert200(response)
        self.assert_template_used('register.html')

        # Login user
        response = self.login_user('testuser@example.com', 'password')
        self.assert200(response)
        self.assert_template_used('login.html')  # Replace 'dashboard.html' with the actual template for the user's dashboard

    def test_edit_profile(self):
        # Register user
        response = self.register_user('testuser@example.com', 'password')
        self.assert200(response)
        self.assert_template_used('register.html')

        # Login user
        response = self.login_user('testuser@example.com', 'password')
        self.assert200(response)
        self.assert_template_used('login.html')

        # Edit user profile
        new_email = 'newemail@example.com'
        response = self.client.post(
            url_for('accounting.account'),  # Оновлено тут
            data=dict(email=new_email),
            follow_redirects=True
        )
        self.assert200(response)
        self.assert_template_used('login.html')  # Змінено тут

        # Verify that user with the new email exists in the database
        user = User.query.filter_by(email=new_email).first()
        self.assertIsNotNone(user)
    # def test_logout(self):
    #     # Register user
    #     response = self.register_user('testuser@example.com', 'password')
    #     self.assert200(response)
    #     self.assert_template_used('login.html')
    #
    #     # Login user
    #     response = self.login_user('testuser@example.com', 'password')
    #     self.assert200(response)
    #     self.assert_template_used('dashboard.html')  # Replace 'dashboard.html' with the actual template for the user's dashboard
    #
    #     # Logout user
    #     response = self.logout_user()
    #     self.assert200(response)
    #     self.assert_template_used('home.html')  # Replace 'home.html' with the actual template for the home page

if __name__ == '__main__':
    unittest.main()
