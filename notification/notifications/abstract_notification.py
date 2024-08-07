from abc import ABC, abstractmethod


class AbstractNotification(ABC):
    @abstractmethod
    def send_message(self, subject, message, recipient):
        pass
