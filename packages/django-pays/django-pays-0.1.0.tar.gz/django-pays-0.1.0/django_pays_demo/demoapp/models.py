from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from django_pays.models import Gateway, Payment


class Order(models.Model):
    name = models.CharField(max_length=30)
    order_id = models.CharField(max_length=10, unique=True)
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=20)
    pays_gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return self.name


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, editable=False, null=True, on_delete=models.CASCADE,
                                   related_name='identified_order_payment')
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=20)

    class Meta:
        verbose_name = _('order payment')
        verbose_name_plural = _('order payments')

    def __str__(self):
        return '{}, {}'.format(self.order, self.amount)


@receiver(post_save, sender=Payment)
def create_order_payment(instance, **kwargs):
    payment = instance
    if payment.status == Payment.REALIZED:
        order = Order.objects.filter(order_id=payment.order_id).first()
        if order:
            OrderPayment.objects.create(order=order, payment=payment, amount=payment.amount / payment.base_units)
