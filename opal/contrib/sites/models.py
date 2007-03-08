from opal.db import models
from opal.utils.translation import gettext_lazy as _

class SiteManager(models.Manager):
    def get_current(self):
        from opal.conf import settings
        return self.get(pk=settings.SITE_ID)

class Site(models.Model):
    domain = models.CharField(_('domain name'), maxlength=100)
    name = models.CharField(_('display name'), maxlength=50)
    objects = SiteManager()
    class Meta:
        db_table = 'opal_site'
        verbose_name = _('site')
        verbose_name_plural = _('sites')
        ordering = ('domain',)
    class Admin:
        list_display = ('domain', 'name')
        search_fields = ('domain', 'name')

    def __str__(self):
        return self.domain
