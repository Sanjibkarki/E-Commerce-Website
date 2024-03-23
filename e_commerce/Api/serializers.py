from rest_framework import serializers
from Posti.models import Ordermodel,Customer
from Api.serializerbranch import Userserializer
class MyModelSerializer(serializers.ModelSerializer):
    Info = Userserializer(source='product',read_only=True)
    Date_of_order = serializers.DateTimeField(source= 'date',read_only=True,format='%Y-%m-%d T-%H:%M:%S')
    class Meta:
        model = Ordermodel
        fields = ['PName','PPrice','Size','Quantity','Info','oredered','Date_of_order']

    