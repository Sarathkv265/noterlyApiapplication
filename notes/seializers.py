from rest_framework import serializers

from notes.models import User,Task

class UserSerializer(serializers.ModelSerializer):
    
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    password=serializers.CharField(read_only=True)
    
    class Meta:
        
        model = User
        
        fields = ["id","username","email","password1","password2","phone","password"]
        
    def create(self,validate_data):
        
        password1=validate_data.pop("password1")       #pass1 & pass2 are poping from validated data for get only one password that is  used on return as pswd=paswd1
        password2=validate_data.pop("password2")
        
        return User.objects.create_user(**validate_data,password=password1)
    
    def validate(self,data):                                    # valdate method overiding heare to validate the password1 and pswd2
        
        if data["password1"] != data["password2"]:
            
            raise serializers.ValidationError("password mismatch")
        
        return data
    


class TaskSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        
        model = Task
        
        fields="__all__"
        
        read_only_fields = ["crated_date","owner","is_active"]