from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, RoleChoices


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,error_messages={"required":"Пароль є обов'язковим"})
    password_confirm = serializers.CharField(write_only=True,required=True, error_messages = {'required': 'Підтвердіть пароль'})
    email = serializers.EmailField(required=True, error_messages={'required': "Email є обов'язковим", 'invalid': "Некоректний формат електронної пошти"})
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True) 

    class Meta:
        model = User
        fields = ['username','email','password', 'first_name', 'last_name', 'role','password_confirm']
    
    def validate(self,data:dict):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({'password_confirm':'Введені паролі не співпадають'})
        return data

    def create(self, validated_data:dict):
        validated_data.pop('password_confirm', None)
        try:
            return User.objects.create_user(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                password=validated_data.get('password'),
                first_name=validated_data.get('first_name',''),
                last_name = validated_data.get('last_name',''),
                role = validated_data.get('role',RoleChoices.USER)
            )
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

class RegisterResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.CharField()        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, error_messages={'required': 'Введіть логін/адресу електронної пошти'})
    password = serializers.CharField(required=True, write_only=True, error_messages = {'required':"Введіть пароль"})

    def validate(self,data):
        username, password = data.get('username'), data.get('password')

        user = authenticate(username=username,password=password)
        data['user'] = user
        return data
    
class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()