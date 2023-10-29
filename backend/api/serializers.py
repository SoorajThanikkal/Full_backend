from rest_framework import serializers
from .models import User, Client, Freelancer
from rest_framework.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_client', 'is_freelancer']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        is_client = data.get('is_client', False)
        is_freelancer = data.get('is_freelancer', False)

        # Check if at least one of the fields is set to True
        if not is_client and not is_freelancer:
            raise ValidationError("You must select at least one of is_client or is_freelancer.")
        return data


    def create(self, validated_data):
        is_client = validated_data.get('is_client', False)
        is_freelancer = validated_data.get('is_freelancer', False)

        # Create a new user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_client=is_client,
            is_freelancer=is_freelancer
        )

        if is_client:
            # If the user is a client, create a client profile
            client_data = {'user': user}
            client = Client.objects.create(**client_data)

        if is_freelancer:
            # If the user is a freelancer, create a freelancer profile
            freelancer_data = {'user': user}
            freelancer = Freelancer.objects.create(**freelancer_data)

        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    



class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['profilepic', 'last_name', 'phone', 'address', 'about']


