import decimal
import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from contrib.middleware import get_current_user

# from cuser.fields import CurrentUserField
# from cuser.middleware import CuserMiddleware


# from contrib.utils import getLogger

logger = logging.getLogger(__name__)


class AuditableModel(models.Model):
    created_by = models.ForeignKey(User, blank=True, null=True, related_name="created_by_user", on_delete=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, related_name="modified_by_user", on_delete=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class AuditableMixins(object):

    AUDITABLE = {}

    def __setattr__(self, name, value):
        new_value = value

        if name not in ('old_fields', 'audit_fields'):
            hasattr(self, 'audit_fields') is False and self._detect_auditable_fields()

            if self.AUDITABLE:
                if name in self.audit_fields and hasattr(self, name):
                    new_value = float(value) if isinstance(value, decimal.Decimal) else value
                    old_value = float(
                        getattr(
                            self,
                            name)) if isinstance(
                        getattr(
                            self,
                            name),
                        decimal.Decimal) else getattr(
                        self,
                        name)

                    if name not in self.old_fields and self.changed_field(name, value) is True:
                        self.old_fields[name] = old_value
                    elif name in self.old_fields and new_value == self.old_fields[name]:
                        self.old_fields.pop(name)

        super(AuditableMixins, self).__setattr__(name, new_value)

    def changed_field(self, field, value):
        cast = {
            decimal.Decimal: lambda x: float(x or 0),
            int: lambda x: int(x or 0),
            models.BooleanField: lambda x: int(x or 0) == 1,
        }

        field = getattr(self, field)
        fn = cast.get(field.__class__, lambda x: x)

        logger.debug([field, fn, value])

        return fn(value) != fn(field)

    def _detect_auditable_fields(self):
        self.audit_fields = [f for f in self.AUDITABLE.get('fields', []) if f not in self.AUDITABLE.get('exclude', [])]

    def __init__(self, *args, **kargs):
        super(AuditableMixins, self).__setattr__('old_fields', {})
        super(AuditableMixins, self).__setattr__('audit_fields', [])

        self._detect_auditable_fields()

        super(AuditableMixins, self).__init__(*args, **kargs)

    def equals(self, other, exclude=[]):
        for key in self.audit_fields:
            try:
                if key not in exclude and float(getattr(self, key, None)) != float(getattr(other, key, None)):
                    return False
            except Exception:
                if key not in exclude and getattr(self, key, None) != getattr(other, key, None):
                    return False
        return True

    def differences(self, other):
        diffs = []
        for key in self.audit_fields:
            try:
                if float(getattr(self, key, None)) != float(getattr(other, key, None)):
                    diffs.append(key)
            except Exception:
                if getattr(self, key, None) != getattr(other, key, None):
                    diffs.append(key)
        return diffs

    @property
    def is_dirty(self):
        return (self.old_fields and True) or False

    @property
    def changed(self):
        return (self.old_fields and True) or False


class AuditTimestampModel(AuditableMixins, models.Model):
    # user = CuserMiddleware.get_user()

    class Meta:
        abstract = True

    # Using DjangoCuser, but it's not working as should
    # created_by = CurrentUserField(user, null=True, blank=True, add_only=True, related_name='created_by_%(class)s', on_delete=models.PROTECT, verbose_name=u'Criado por')
    # modified_by = CurrentUserField(user, null=True, blank=True, related_name="modified_by_%(class)s", on_delete=models.PROTECT, verbose_name=u'Alterado por')

    # Using User field Django
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="+", default=1, verbose_name=u'Criado por')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="+", default=1, verbose_name=u'Alterado por')

    created_at = models.DateTimeField(verbose_name=u'Criado em', auto_now_add=True)
    created_at.editable = False
    modified_at = models.DateTimeField(verbose_name=u'Modificado em', auto_now=True)
    modified_at.editable = False

    def __init__(self, *args, **kargs):
        super(AuditTimestampModel, self).__init__(*args, **kargs)

        if self.AUDITABLE.get('fields', False) is False:
            self.audit_fields = [f.name for f in self._meta.fields if f.name not in self.AUDITABLE.get('exclude', [])]

        for field in AuditTimestampModel._meta.fields:
            if field.name in self.audit_fields:
                self.audit_fields.remove(field.name)

    def changed_field(self, field, value):
        old_value = float(
            getattr(
                self,
                field)) if isinstance(
            getattr(
                self,
                field),
            decimal.Decimal) else getattr(
            self,
            field)
        return old_value != value

    def save(self, *args, **kargs):
        if not self.pk:
            self.created_by = get_current_user()
            self.created_at = timezone.now()
            self.modified_by = get_current_user()
            self.modified_at = timezone.now()

        super(AuditTimestampModel, self).save(*args, **kargs)

        if self.AUDITABLE.get('clear_after_save', False):
            self.old_fields = {}


class CObject(AuditTimestampModel):
    nome = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True, verbose_name='Descrição')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome
