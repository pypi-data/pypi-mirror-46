from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django_pays import payment_url

from .models import Order, OrderPayment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_id', 'amount', 'payment_link')

    def payment_link(self, obj):
        return mark_safe('<a href="{url}" target="_blank">{url}</a>'.format(
            url=payment_url(
                gateway=obj.pays_gateway,
                order_id=obj.order_id,
                amount=int(obj.amount * 100),
                currency='CZK',
            ),
        ))
    payment_link.short_description = _('payment link')
    payment_link.allow_tags = True


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment', 'amount')
