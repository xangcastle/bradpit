from __future__ import unicode_literals
from django.db import models
from django.db.models import Max
from django.forms.models import model_to_dict


def get_code(entidad, length=4):
        model = type(entidad)
        code = ''
        sets = model.objects.filter(code__isnull=False)
        if sets:
            maxi = str(sets.aggregate(Max('code'))['code__max'])
            if maxi:
                consecutivo = list(range(1, int(maxi)))
                ocupados = list(sets.values_list('code', flat=True))
                n = 0
                for l in ocupados:
                    ocupados[n] = int(str(l))
                    n += 1
                disponibles = list(set(consecutivo) - set(ocupados))
                if len(disponibles) > 0:
                    code = min(disponibles)
                else:
                    code = max(ocupados) + 1
        else:
            code = 1
        return str(code).zfill(length)


class base(models.Model):

    def __iter__(self):
        for field_name in self._meta.get_all_field_names():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    def __getitem__(self, fieldname):
        try:
            return getattr(self, fieldname)
        except:
            return None

    def to_json(self):
        return model_to_dict(self)

    class Meta:
        abstract = True


class base_entidad(base):
    code = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="codigo")
    name = models.CharField(max_length=100, verbose_name="nombre")

    class Meta:
        abstract = True


class Entidad(base_entidad):
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.code and self.name:
            return str(self.code) + " " + self.name
        elif self.name:
            return self.name
        elif self.code:
            return str(self.code)
        else:
            return ''

    @staticmethod
    def autocomplete_search_fields():
        return ("code__iexact", "name__icontains",)

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = get_code(self)
        super(Entidad, self).save()

    class Meta:
        abstract = True
        ordering = ['name']
