from .models import User
from rest_framework import serializers

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
