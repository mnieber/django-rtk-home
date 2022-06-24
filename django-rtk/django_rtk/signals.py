from django.dispatch import Signal

account_registered = Signal()
account_activated = Signal()
password_reset_requested = Signal()
password_reset = Signal()
password_changed = Signal()
magic_link_sent = Signal()
signed_in_by_magic_link = Signal()
