from django.contrib import admin
from .models import Transaction, User, Wallet

admin.site.register((Transaction, User, Wallet), admin.ModelAdmin)
