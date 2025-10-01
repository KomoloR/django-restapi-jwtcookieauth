# tests for the models of the application 
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    def test_create_user_with_email_ok(self):
        email = 'test@email.com'
        password = 'testpwd1'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_created_user_email_normalized(self):
        test_emails=[
            ["testuser1@EXAMPLE.com","testuser1@example.com"],
            ["TestUser2@Example.com", "TestUser2@example.com"],
            ["TESTUSER3@EXAMPLE.com", "TESTUSER3@example.com"],
            ["testuser4@example.COM", "testuser4@example.com"],
        ]
        for email, expected in test_emails:
            user=get_user_model().objects.create_user(email, 'testpwd1')
            self.assertEqual(user.email, expected)

    def test_user_without_email_ko(self):
        # test creating user without an email add. fails 
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpwd1')

    def test_create_superuser(self):
        user=get_user_model().objects.create_superuser(
            'testadmin@example.com',
            'testpwd1',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

