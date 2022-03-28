from django.db import models, transaction
from meuapp.models import BaseModel
from .router import get_route


def get_format(obj):
    return f'Rua {obj.street} nº{obj.number}, Bairro {obj.district} - {obj.city_name}/{obj.state_name}.CEP: {obj.code}'


def get_nominatin(obj):
    return f'Rua {obj.street}, {obj.city_name}, {obj.state_name}, {obj.code}'


class Branch(models.Model):
    country_name = models.CharField('País', max_length=100)
    state_name = models.CharField('Estado', max_length=100)
    city_name = models.CharField('Cidade', max_length=100)
    number = models.PositiveIntegerField('Número')
    street = models.CharField('Rua', max_length=100)
    district = models.CharField('Bairro', max_length=100)
    code = models.CharField('CEP', max_length=20)
    reference = models.CharField('Ponto de Referência', max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    altitude = models.DecimalField(max_digits=22, decimal_places=16)
    active = models.BooleanField(default=True)

    def __str__(self):
        return get_format(self)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            Branch.objects.filter().update(active=False)
            return super(Branch, self).save(*args, **kwargs)


class ClientAddress(BaseModel):
    client = models.ForeignKey(to="legacy.Client", on_delete=models.CASCADE, related_name="addresses", )
    country_name = models.CharField('País', max_length=100)
    state_name = models.CharField('Estado', max_length=100)
    city_name = models.CharField('Cidade', max_length=100)
    number = models.PositiveIntegerField('Número')
    street = models.CharField('Rua', max_length=100)
    district = models.CharField('Bairro', max_length=100)
    code = models.CharField('CEP', max_length=20)
    reference = models.CharField('Ponto de Referência', max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    altitude = models.DecimalField(max_digits=22, decimal_places=16)
    active = models.BooleanField(default=True)
    distance = models.FloatField('Distância (KM)')
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-active', '-created_on']
        unique_together = ['client', 'street', 'number']

    def __str__(self):
        return get_format(self)

    def save(self, *args, **kwargs):
        if not self.distance:
            branch = Branch.objects.filter(active=True).first()
            route = get_route(branch.latitude, branch.longitude, self.latitude, self.longitude)
            self.distance = route['distance']

        with transaction.atomic():
            ClientAddress.objects.filter(client=self.client.pk).update(active=False)
            return super(ClientAddress, self).save(*args, **kwargs)
