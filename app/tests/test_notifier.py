"""
Tests for Notifier.
"""
import os

from unittest import TestCase

from utils.notifier import EmailNotifier

from dotenv import load_dotenv

load_dotenv()


class TestEmailNotifier(TestCase):
    """Tests for EmailNotifier class."""

    def test_create_notifier_with_valid_default_data(self):
        """Tests creating an email notifier with valid arguments."""

        ntf = EmailNotifier()

        self.assertEqual(ntf.receiver, os.environ.get('RECEIVER_EMAIL'))
        self.assertEqual(ntf.password, os.environ.get('SENDER_PASS'))
        self.assertEqual(ntf.sender, os.environ.get('SENDER_EMAIL'))

    def test_create_notifier_with_valid_another_receiver(self):
        """Tests creating an email notifier with another receiver."""

        payload = {'receiver': 'test_receiver@example.com'}

        ntf = EmailNotifier(**payload)

        self.assertEqual(ntf.receiver, payload['receiver'])

    def test_create_notifier_with_invalid_receiver_error(self):
        """Tests creating notifier with invalid email raises an error."""

        test_cases = ['', 'asdf.fg', '@example.com', 'asdf@']

        with self.assertRaises(ValueError):
            for case in test_cases:
                EmailNotifier(receiver=case)
