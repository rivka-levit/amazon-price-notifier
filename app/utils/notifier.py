"""
Send notifications classes.
"""

import os
import ssl
import smtplib

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

    def __init__(self):
        self.sender = os.environ.get('SENDER_EMAIL')
        self.password = os.environ.get('SENDER_PASS')
        self.receiver = os.environ.get('RECEIVER_EMAIL')

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
#     ntf.notify('$63.85')
