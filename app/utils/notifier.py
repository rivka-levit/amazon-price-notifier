from abc import ABC, abstractmethod


class AbstractNotifier(ABC):
    """Abstract notifier."""

    @abstractmethod
    def notify(self):
        pass


class EmailNotifier(AbstractNotifier):
    """Notify users via email."""

    def __init__(self):
        pass

    def notify(self):
        pass
