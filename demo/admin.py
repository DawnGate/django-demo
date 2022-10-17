from django.contrib import admin

from .models import User, Wallet, Withdrawn, Deposit

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Withdrawn)
admin.site.register(Deposit)

# Register your models here.
