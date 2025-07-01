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


class DigitalAccountSerializer(serializers.Serializer):
    portador = PortadorSerializer()
    current_balance = serializers.FloatField(required=False)
    number = serializers.IntegerField()
    agency = serializers.IntegerField()
    active = serializers.BooleanField(required=False)
    blocked = serializers.BooleanField(required=False)