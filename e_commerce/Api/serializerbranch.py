from rest_framework import serializers

class UserLinkedInline(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='detail',
        lookup_field = 'pk',
        read_only = True
    )
    
class Userserializer(serializers.Serializer):
    email = serializers.CharField(source= 'customer',read_only=True)
    path = serializers.SerializerMethodField(read_only=True)
    
    def get_path(self,obj):
        request = self.context.get('request')
        
        mydata = obj.ordermodel_set.all()
        return UserLinkedInline(mydata,many = True,context = {'request':request}).data