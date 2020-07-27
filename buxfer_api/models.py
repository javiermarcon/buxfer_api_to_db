from django.db import models

# Create your models here.

class ProjectBaseModel(models.Model):
    """Base abstract model for all models used throughout the project."""
    ## Basic time tracking for all models ##
    time_created = models.DateTimeField("created", auto_now_add=True, db_index=True)
    time_modified = models.DateTimeField("modified", auto_now=True, db_index=True)

    class Meta:
        abstract = True

TRANSACTION_TYPES = {
        ('income', 'income'),
        ('expense', 'expense'),
        ('transfer', 'transfer'),
        ('refund', 'refund'),
        ('sharedBill', 'sharedBill'),
        ('paidForFriend', 'paidForFriend'),
        ('loan', 'loan')
    }

class Account(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=3)
    bank = models.CharField(max_length=200)
    balance = models.FloatField()
    lastSynced = models.DateTimeField('Last Sync')


"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='users')
    # Empresa esta en el profile
    area = models.CharField(max_length=200)  # Área
    reference_number = models.CharField(max_length=50)  # Número de referencia interno
    quotation_type = models.CharField(max_length=50, choices=TYPE)
    delivery_date = models.DateTimeField('Fecha de entrega')  # Fecha entrega requerida
    reference_price = models.FloatField()
    notify_all = models.BooleanField(blank=True)
"""