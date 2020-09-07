from django.contrib import admin
from .models import Account, Tag, Transaction

# Register your models here.
admin.site.register(Account)
admin.site.register(Tag)
admin.site.register(Transaction)
