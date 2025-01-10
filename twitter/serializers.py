from django.contrib.auth.models import User
from twitter.models import Postagem,Comentario
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,write_only=True)
    confirmation_password = serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','password','confirmation_password','first_name','last_name']

    def validate(self, attrs):
        password = attrs.get('password')
        confirmation_password = attrs.get('confirmation_password')
        if not password == confirmation_password:
            raise serializers.ValidationError({"password":"Senhas estão diferentes diferentes"})
        return attrs

    def create(self,validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
class PostagemSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    comentario = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Postagem
        fields = ['id','usuario','titulo','postagem','imagem','criado','editado','comentario']

class ComentarioSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    class Meta:
        model = Comentario
        fields = ['id','usuario','postagem','titulo','comentario','criado','editado']
