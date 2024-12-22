"""Tests for gmail module"""

from sxolar.util import gmail

class TestGmail:
    """Test the gmail module"""

    def test_send_email(self):
        """Test the send_email function"""
        gmail.send_email(
            subject="Test Email Sxolar",
            to="jameswkennington@gmail.com",
            body="This is a test email from Sxolar",
        )
