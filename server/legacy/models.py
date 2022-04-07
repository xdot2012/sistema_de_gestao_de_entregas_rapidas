from django.db import models
from meuapp.models import BaseModel
from django.db import transaction
from routing.router import get_route

DELIVERY_CHOICES = (
    ('DEFAULT', 'Entrega Imediata'),
    ('PICKUP', 'Retirada no Local'),
)

VEHICLE_CHOICES = (
    ('CAR', 'Carro'),
    ('MOTORCYCLE', 'Moto'),
    ('BIKE', 'Bicicleta')
)

STATUS_CHOICES = (
    ('IDLE', 'Aguardando'),
    ('UNAVAILABLE', 'Indisponível'),
    ('IN_ROUTE', 'Em rota')
)

PAYMENT_CHOICES = (
    ('CREDIT_CARD', 'Cartão de Crédito'),
    ('DEBIT_CARD', 'Cartão de Débito'),
    ('CASH', 'Dinheiro Vivo'),
    ('PIX', 'Pix'),
    ('TED', 'Transferência Bancária'),
)


class DeliveryMan(BaseModel):
    name = models.CharField('Nome', max_length=100)
    phone = models.CharField('Telefone', max_length=11, unique=True)
    vehicle_type = models.CharField('Tipo do Veículo', max_length=15, choices=(VEHICLE_CHOICES))
    status = models.CharField('Situação', max_length=15, choices=STATUS_CHOICES, default="IDLE")
    capacity = models.PositiveIntegerField('Capacidade do Veículo (Nº de pedidos)', default=0)


class Client(BaseModel):
    name = models.CharField('Nome', max_length=100)
    phone = models.CharField('Telefone', max_length=11, unique=True)

    class Meta:
        unique_together = ['name', 'phone']

    def __str__(self):
        return self.name


class Order(BaseModel):
    client = models.ForeignKey(verbose_name='Cliente', to='Client', on_delete=models.PROTECT)
    address = models.ForeignKey(verbose_name='Endereço', to='routing.ClientAddress', on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=20, verbose_name='Método de Pagamento', choices=PAYMENT_CHOICES, default='CASH')
    is_paid = models.BooleanField(verbose_name='Já pago', default=False)
    delivery_type = models.CharField(max_length=20, verbose_name='Tipo de Entrega', choices=DELIVERY_CHOICES)
    created_on = models.DateTimeField(verbose_name='Recebido em', auto_now=True)
    modified_on = models.DateTimeField(verbose_name='Modificado em', auto_now_add=True)
    ready_on = models.DateTimeField(verbose_name='Pronto para entrega em', null=True, blank=True)
    finished_on = models.DateTimeField(verbose_name='Concluída em', null=True, blank=True)
    created_by = models.ForeignKey(verbose_name='Criado por', to='accounts.User', related_name='created_orders', on_delete=models.PROTECT)
    modified_by = models.ForeignKey(verbose_name='Modificado por', to='accounts.User', related_name='modified_orders', null=True, blank=True, on_delete=models.PROTECT)
    active = models.BooleanField(verbose_name='Ativa', default=True)

    def __str__(self):
        return f'{self.client} - {self.created_on}'


class OrderProduct(BaseModel):
    order = models.ForeignKey(verbose_name='Ordem', to='Order', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Produto', max_length=200)
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')

    def __str__(self):
        return self.name


class OrderAppointment(BaseModel):
    order = models.ForeignKey(verbose_name='Ordem', to='Order', on_delete=models.CASCADE)
    appointment = models.DateTimeField(verbose_name='Horário de Entrega')
