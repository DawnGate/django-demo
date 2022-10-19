from email.policy import default
from django.db import models
import uuid

class User(models.Model): 
    id = models.CharField(primary_key = True, max_length = 50)

class Wallet(models.Model):
    class Status(models.TextChoices):
        ENABLE = 'ENA', "enabled"
        DISABLED = 'DIS', "disabled"
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    status = models.CharField(max_length = 3, choices = Status.choices, default = "ENA")
    enabled_at = models.DateTimeField(null = True)
    disabled_at = models.DateTimeField(null = True)
    balance = models.PositiveIntegerField(default=0)
    owned_by = models.ForeignKey(User, on_delete = models.CASCADE)

class TransactionStatus(models.TextChoices):
    SUCCESS = 'SUCC', 'success'
    FAIL = 'FAIL', 'fail'

class Withdrawn(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    ref_id = models.CharField(unique = True, max_length =  50)
    widthdrawn_by = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    withdrawn_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices = TransactionStatus.choices, default = "FAIL")

class Deposit(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    ref_id = models.CharField(unique = True, max_length =  50)
    deposit_by = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    deposit_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices = TransactionStatus.choices, default = "FAIL")

