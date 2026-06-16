from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializers(serializers.ModelSerializer):
      
             password = serializers.CharField(write_only=True)

             class Meta :
                    model = User

                    fields = (
                        'id',
                        'username',
                        'email',
                        'mobile',
                        'password',
                            
                    ) 

                    read_only_fields = (
                        'id',
                    )



             def create(self, validated_data):
                        
                user = User.objects.create_user(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    mobile=validated_data['mobile'],
                    password=validated_data['password'],
                )

                return user

class LoginSerializers(serializers.Serializer):
        
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)

        def validate(self,data):
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username,password=password)     

            if not user:
                   raise serializers.ValidationError("Invalid username or password")
            
            return {
                    "user": user.username
            }