from rest_framework import serializers, viewsets
from Posti.models import Ordermodel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordermodel
        fields = ['PName','PPrice','Size','Quantity','product']
    
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer