from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=1)  # Ensures at least 1 character
    
    class Meta:
        model = User
        fields = '__all__'
