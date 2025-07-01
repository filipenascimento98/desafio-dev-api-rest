from rest_framework import serializers
from api.validators import Validator


class PortadorSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    cpf = serializers.CharField(max_length=11)

    def validate_cpf(self, value):
        validator = Validator()
        
        if not validator.validate_cpf(value):
            raise serializers.ValidationError('Invalid CPF')
        
        return value