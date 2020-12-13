from django.db import models

# Create your models here.

class ProjectBaseModel(models.Model):
    """Base abstract model for all models used throughout the project."""
    ## Basic time tracking for all models ##
    time_created = models.DateTimeField("created", auto_now_add=True, db_index=True)
    time_modified = models.DateTimeField("modified", auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    def get_fieldValues(self):
        return [field.value_to_string(self) for field in self._meta.fields]

    def get_fieldNames(self):
        return [field.name for field in self._meta.fields]

DISCRECIONALIDADES = {
        ('F', 'Fijo'), # Fijo
        ('V', 'Variable'), # Variable
        ('D', 'Discrecional'), # Discrecional
    }

TIPOS_CAT = {
        'i': [
            1,   # settlement
            4,   # income
            9,   # refund
            11,   # investment sale
            12,   # dividend
        ],
        'e': [
            3,   # expense
            10,   # investment purchase
            8,   # loan
        ]
    }
#6	transfer

CAT_PRINCIPALES = {
    (1, 'HOGAR Y VIVIENDA'),
    (2, 'AUTOMOVIL Y TRANSPORTE'),
    (3, 'ALIMENTOS'),
    (4, 'ROPA'),
    (5, 'CUIDADO PERSONAL'),
    (6, 'CUIDADO DE LA SALUD'),
    (7, 'ENTRETENIMIENTO'),
    (8, 'REGALOS'),
    (9, 'EDUCACION'),
    (10, 'VACACIONES'),
    (11, 'GASTOS DE NEGOCIOS'),
    (12, 'CUIDADO Y DEPENDENCIAS'),
    (13, 'INVERSIONES Y AHORROS'),
    (14, 'SEGUROS'),
    (15, 'ESPIRITUAL'),
    (16, 'DEUDAS REPAGADAS'),
    (17, 'SERVICIOS'),
    (18, 'IMPUESTOS'),
    (19, 'LECCIONES APRENDIDAS'),
    (20, 'HONORARIOS PAGADOS'),

}

TRANSACTION_TYPES = {
        ('income', 'income'),
        ('expense', 'expense'),
        ('transfer', 'transfer'),
        ('refund', 'refund'),
        ('sharedBill', 'sharedBill'),
        ('paidForFriend', 'paidForFriend'),
        ('loan', 'loan')
    }

TIPOS_PAGO = {
    ('$', '$ Efectivo'), # efectivo
    ('T', 'Tarjeta'), # tarjeta
    ('C', 'Cheque'), # Cheque
}

TIPOS_TAG = {
    ('I', 'Ingreso'),
    ('G', 'Gasto'),
    ('A', 'Activo'),
    ('P', 'Pasivo'),
}

class Account(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=3)
    bank = models.CharField(max_length=200)
    #balance = models.FloatField()
    #lastSynced = models.DateTimeField('Last Sync', blank=True, null=True)
    tipo_pago = models.CharField(max_length=1, default=None, choices=TIPOS_PAGO, blank=True, null=True)

    class Meta:
        ordering = ['bank', 'name']

    def __str__(self):
        return f"{self.name} ({self.currency})"

class Tag(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    parentId = models.IntegerField(blank=True, null=True)
    relativeName = models.CharField(max_length=100)
    categoria = models.IntegerField(default=None, choices=CAT_PRINCIPALES, blank=True, null=True)
    tipo_tag = models.CharField(max_length=1, default=None, choices=TIPOS_TAG, blank=True, null=True)
    discrecionalidad = models.CharField(max_length=1, default=None, choices=DISCRECIONALIDADES, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class TransactionType(ProjectBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

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
    accountId = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    #accountName
    tags = models.ManyToManyField('Tag', through='TransactionTag', related_name='transactions')
    status = models.CharField(max_length=200)
    isFutureDated = models.BooleanField(blank=True)
    isPending = models.BooleanField(blank=True)
    sortDate = models.DateField(blank=True)
    fromAccount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactionsFrom', blank=True, null=True)
    toAccount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactionsTo', blank=True, null=True)
    discrecionalidad = models.CharField(max_length=1 ,default=None,choices=DISCRECIONALIDADES, blank=True, null=True)

    class Meta:
        ordering = ['-normalizedDate', 'description']
        # db_table = u'transaction'

    def __str__(self):
        return 'fecha: {} cantidad: {} descripcion: {}'.format(self.normalizedDate, self.amount, self.description)

class TransactionTag(models.Model):
    id = models.IntegerField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, null=True)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)

