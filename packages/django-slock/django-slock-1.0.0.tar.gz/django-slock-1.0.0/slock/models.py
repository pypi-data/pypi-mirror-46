from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
import datetime

class BasicUserMixin(object):
    def get_user_url(self):
        return reverse('core_app:user', 
        kwargs={'user_id': self.id})

    def __str__(self):
        return self.name

class BasicUser(BasicUserMixin, models.Model):
    name = models.CharField(null=True,
    blank=False, verbose_name=_("Name"), 
    help_text='User Name', max_length=256)

    password = models.CharField(null=True,
    blank=False, verbose_name=_("Password"), 
    help_text='Password', max_length=256)

    email = models.EmailField(max_length=70, 
    null=True, blank=False, unique=True)



