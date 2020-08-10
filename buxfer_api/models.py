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
    lastSynced = models.DateTimeField('Last Sync', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, id= {self.id}, currency= {self.currency} "

class Tag(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    parentId = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}, id= {self.id} "

