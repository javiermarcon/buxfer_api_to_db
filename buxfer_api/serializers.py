from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from django.db.models import Q
import pprint
from .models import Account, Tag, TransactionType, Transaction

# https://stackoverflow.com/questions/17280007/retrieving-a-foreign-key-value-with-django-rest-framework-serializers
# https://stackoverflow.com/questions/14573102/how-do-i-include-related-model-fields-using-django-rest-framework
# https://stackoverflow.com/questions/33182092/django-rest-framework-serializing-many-to-many-field

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'currency', 'bank', 'balance', 'lastSynced')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'parentId', 'relativeName')

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ('id', 'name')

class TransactionSerializer(serializers.ModelSerializer):
    #tagNames = serializers.CharField(source='tags') #serializers.SerializerMethodField('get_tag_id', source='tags')
    tagNames = TagSerializer(read_only=True, many=True, source='tags') # llamar a transactionserializer con many= True para que sea man to many
    #transactionType = TransactionTypeSerializer(read_only=True) # ReadOnlyField(source='TransactionType.name')
    #accountId = ReadOnlyField(source='Account.id')
    #fromAccount = ReadOnlyField(source='Account.name')
    #toAccount = ReadOnlyField(source='Account.name')

    def to_internal_value(self, data):

        if data['tagNames']:
            tags_qs = Q()
            for tag in data['tagNames']:
                tags_qs = tags_qs | Q(name=tag)
            tag_objs = Tag.objects.filter(tags_qs)
            data['tagNames'] = [x.id for x in tag_objs]

        if 'fromAccount' in data and data['fromAccount']:
            data['fromAccount'] = data['fromAccount']['id']
        if 'toAccount' in data and data['toAccount']:
            data['toAccount'] = data['toAccount']['id']
        transaction_type = TransactionType.objects.filter(name=data['transactionType'])
        if not transaction_type:
            transaction_type = TransactionType(id=data['rawTransactionType'], name=data['transactionType'])
            transaction_type.save()
        else:
            transaction_type = transaction_type[0]
        try:
            print(transaction_type.id)
            #import pdb
            #pdb.set_trace()
            data['transactionType'] = transaction_type.id
        except Exception as e:
            print(e)
        print(data)
        return super(TransactionSerializer, self).to_internal_value(data)

    #def get_tag_id(self, obj):
    #    import pdb
    #    pdb.set_trace()
    #    return obj.tags

    class Meta:
        model = Transaction
        fields = ('id', 'description', 'normalizedDate', 'transactionType', 'amount', 'expenseAmount', 'accountId', 'tagNames', 'status',
                  'isFutureDated', 'isPending', 'sortDate', 'fromAccount', 'toAccount')

    def create(self, validated_data):
        #tags = validated_data.pop('tracks')
        pprint.pprint(validated_data)
        #import pdb; pdb.set_trace()
        #for tag in tags:
        #    Track.objects.create(album=album, **track_data)
        transaction = Transaction.objects.create(**validated_data)

        return transaction