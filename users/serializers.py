from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User



class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length= 150, validators=[UniqueValidator(queryset=User.objects.all(), message="username already taken.")])
    email = serializers.EmailField(max_length=127, validators=[UniqueValidator(queryset=User.objects.all(), message="email already registered.")])
    birthdate = serializers.DateField(required=False)
    first_name = serializers.CharField(max_length= 50)
    last_name = serializers.CharField(max_length= 50)
    is_employee = serializers.BooleanField(default=False)
    password = serializers.CharField(max_length= 128, write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        
        if validated_data["is_employee"]:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance: User, validated_data: dict):
        for k ,v in validated_data.items():
            if k == 'password':
                instance.set_password(v)
            else:
                setattr(instance, k, v)
        instance.save()
        return instance


