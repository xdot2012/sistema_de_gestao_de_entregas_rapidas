from django.db import models
from meuapp.models import BaseModel

DELIVERY_CHOICES = (
    ('DELIVERY', 'Entrega Imediata'),
    ('PICKUP', 'Retirada no Local'),
)


class Client(BaseModel):
    name = models.CharField('Nome', max_length=100)
    phone = models.CharField('Telefone', max_length=11, unique=True)
    number = models.PositiveIntegerField('Número')
    street = models.CharField('Rua', max_length=100)
    district = models.CharField('Bairro', max_length=100)
    code = models.CharField('CEP', max_length=20)
    reference = models.CharField('Ponto de Referência', max_length=200, null=True, blank=True)
    country_name = models.CharField('País', max_length=100)
    state_name = models.CharField('Estado', max_length=100)
    city_name = models.CharField('Cidade', max_length=100)

    class Meta:
        unique_together: [['name', 'phone']]

    def __str__(self):
        return self.name


class Order(BaseModel):
    client = models.ForeignKey(verbose_name='Cliente', to='Client', on_delete=models.PROTECT)
    delivery_type = models.CharField(max_length=20, verbose_name='Tipo de Entrega', choices=DELIVERY_CHOICES)
    created_on = models.DateTimeField(verbose_name='Recebido em', auto_now_add=True)
    modified_on = models.DateTimeField(verbose_name='Modificado em', auto_now=True)
    created_by = models.ForeignKey(verbose_name='Criado por', to='accounts.User', related_name='created_orders', on_delete=models.PROTECT)
    modified_by = models.ForeignKey(verbose_name='Modificado por', to='accounts.User', related_name='modified_orders', on_delete=models.PROTECT)
    finished_on = models.DateTimeField(verbose_name='Concluída em', null=True, blank=True)


class OrderProduct(BaseModel):
    order = models.ForeignKey(verbose_name='Ordem', to='Order', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Produto', max_length=200)
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')


class OrderAppointment(BaseModel):
    order = models.ForeignKey(verbose_name='Ordem', to='Order', on_delete=models.CASCADE)
    appointment = models.DateTimeField(verbose_name='Horário de Entrega')


class Local(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['user', 'latitude', 'longitude']]