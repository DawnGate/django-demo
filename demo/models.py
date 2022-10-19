from email.policy import default
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserAccountManager(BaseUserManager):
    def create_superuser(self, xid, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        user =  self.create_user(xid, password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, xid, password, **other_fields):
        if not xid:
            raise ValueError('Xid is required!')
        user = self.model(xid=xid, password=password, **other_fields)
        user.set_unusable_password()
        user.save()
        print(user)
        return user

class User(AbstractBaseUser, PermissionsMixin): 
    xid = models.CharField(unique = True, max_length = 50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserAccountManager()
    USERNAME_FIELD = 'xid'

    def __str__(self):
        return self.xid


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

