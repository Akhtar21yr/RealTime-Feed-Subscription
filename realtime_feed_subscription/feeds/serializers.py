from rest_framework import serializers
from .models import Subscription,User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    city = serializers.CharField(max_length = 250,required = False)
    class Meta:
        model = User
        fields = ['email','age', 'full_name','city','password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
             raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        return data

    def create(self, data):
        password = data.pop('password2', '')
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        return user
    