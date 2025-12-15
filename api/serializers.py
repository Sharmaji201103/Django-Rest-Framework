from rest_framework import serializers
from students.models import Student
from employees.models import Employee
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"
        
class ImportSerializer(serializers.Serializer):
    file=serializers.FileField()
    
class RegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','password2']
        
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password must match")
        return data
    
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user