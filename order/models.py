from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Order(models.Model):
    aid = models.CharField(max_length=100)
    tid = models.CharField(max_length=20)
    cid = models.CharField(max_length=100)
    sid = models.CharField(max_length=100, blank=True, null=True)
    partner_order_id = models.CharField(max_length=100)
    partner_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payment_method_type = models.CharField(max_length=100)
    amount = models.JSONField()
    card_info = models.JSONField(blank=True, null=True)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField()
    approved = models.DateTimeField()

    def __str__(self):
        return self.tid

class OrderPrepare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tid = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)

    def get_order_id(self):
        return self.order_id

    def __str__(self):
        return self.user.username + "'s orderprepare"