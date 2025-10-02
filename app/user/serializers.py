from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer



class CustomRegisterSerializer(RegisterSerializer):
    # remove username field 
    username= None
    # custom serializer for user registration 
    name=serializers.CharField(max_length=255)

    # define transaction atomic to rollback the save operation incase of error 
    @transaction.atomic
    def save(self, request):
        user=super().save(request)
        user.name=self.data.get('name')
        user.save()

        return user

class CustomLoginSerializer(LoginSerializer):
    username=None
    email=serializers.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= get_user_model()
        fields= ['email', 'password', 'name']
        extra_kwargs= {"password" :{'write_only':True , 'min_length':5}}

    def create(self, validated_data):
        # creating a user with validated data 
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, **validated_data):
        # updating a user 
        password=validated_data.pop('password', None)
        user=super().update(instance, validated_data)

        if password :
            user.set_password(password)
            user.save()

        return user