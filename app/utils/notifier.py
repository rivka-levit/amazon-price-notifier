"""
Send notifications classes.
"""

import os
import ssl
import smtplib
import re

from abc import ABC, abstractmethod

from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


class AbstractNotifier(ABC):
    """Abstract notifier."""

    @abstractmethod
    def notify(self, price: str) -> None:
        pass


class EmailNotifier(AbstractNotifier):
    """Notify users via email."""

    def __init__(self, receiver: str = None) -> None:
        self.sender = os.environ.get('SENDER_EMAIL')
        self.password = os.environ.get('SENDER_PASS')
        self._receiver = None
        if receiver is None:
            self.receiver = os.environ.get('RECEIVER_EMAIL')
        else:
            self.receiver = receiver

    def __eq__(self, other):
        return (isinstance(other, EmailNotifier) and
                self.sender == other.sender and
                self.receiver == other.receiver)

    def __hash__(self):
        return hash((self.__class__.__name__, self.sender, self.receiver))

    @property
    def receiver(self):
        return self._receiver

    @receiver.setter
    def receiver(self, receiver_mail: str) -> None:
        if not self.valid_email(receiver_mail):
            raise ValueError('Invalid email address!')

        self._receiver = receiver_mail

    @staticmethod
    def valid_email(email: str) -> bool:
        """Validate email address"""

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        return re.fullmatch(pattern, email) is not None

    def notify(self, price: str) -> None:
        msg = EmailMessage()
        msg['Subject'] = 'Amazon Price Notification'
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg.set_content(f"Hi! the price that you are interested in, has been "
                        f"changed. By now it is {price}")

        context = ssl.create_default_context()

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls(context=context)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())


# if __name__ == '__main__':
#     ntf = EmailNotifier()
#     print(ntf.__class__.__name__)
#     ntf.notify('$63.85')
