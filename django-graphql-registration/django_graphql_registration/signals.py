from django.dispatch import Signal

account_registered = Signal()
account_activated = Signal()
password_reset_requested = Signal()
password_reset = Signal()
