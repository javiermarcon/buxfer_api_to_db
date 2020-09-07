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
    parentId = models.IntegerField(blank=True, null=True)
    relativeName = models.CharField(max_length=100)



    def __str__(self):
        return f"{self.name}, id= {self.id} "

class TransactionType(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

class Transaction(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=200)
    #date = models.DateTimeField('Last Sync', blank=True, null=True)
    normalizedDate  = models.DateField('Last Sync', blank=True, null=True)
    #type: "transfer",
    transactionType = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='transactions')
    #rawTransactionType: 6,
    amount = models.FloatField()
    expenseAmount = models.FloatField()
    accountId = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    #accountName
    tags = models.ManyToManyField('Tag', related_name='transactions')
    status = models.CharField(max_length=200)
    isFutureDated = models.BooleanField(blank=True)
    isPending = models.BooleanField(blank=True)
    sortDate = models.DateField(blank=True)
    fromAccount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactionsFrom', blank=True, null=True)
    toAccount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactionsTo', blank=True, null=True)
