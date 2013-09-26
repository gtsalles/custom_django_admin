from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class CommonUser(models.Model):
    """
    A Commom User
    """

    user = models.ForeignKey(User)
    name = models.CharField(_(u'Name'), max_length=30)
    email = models.EmailField()
    phone = models.CharField(_(u'Telephone'), max_length=11, blank=True)
    address = models.CharField(_(u'Address'), max_length=75, blank=True)
    active = models.BooleanField(_(u'Active'), default=True)
    date_joined = models.DateTimeField(_(u'Member Since'), auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Commom User')