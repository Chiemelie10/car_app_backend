"""This module defines class Util."""
from uuid import uuid4
from django.core.mail import EmailMessage


class Util():
    """
    This class defines a method that handles sending email to the user.
    """
    @staticmethod
    def send_email(data):
        """This method sends the email to the user."""
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

def generate_ref_code():
    """Generates referral code."""
    code = str(uuid4()).replace('-', '')[:12]
    return code
