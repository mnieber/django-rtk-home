import django
from django.utils.encoding import force_str

# This line adds an alias for the force_str function. This alias is used
# by django-graphene (which assumes that the old name "force_text" is still used).
django.utils.encoding.force_text = force_str
