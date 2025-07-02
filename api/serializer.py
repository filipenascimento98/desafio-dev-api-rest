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
    portador = serializers.CharField(max_length=11)
    current_balance = serializers.FloatField(required=False)
    number = serializers.IntegerField()
    agency = serializers.IntegerField()
    active = serializers.BooleanField(required=False)
    blocked = serializers.BooleanField(required=False)

    
class DigitalAccountDeserializer(serializers.Serializer):
    portador = PortadorSerializer()
    current_balance = serializers.FloatField(required=False)
    number = serializers.IntegerField()
    agency = serializers.IntegerField()
    active = serializers.BooleanField(required=False)
    blocked = serializers.BooleanField(required=False)


class TransactionSerializer(serializers.Serializer):
    number_account = serializers.IntegerField()
    agency_account = serializers.IntegerField()
    value = serializers.FloatField()
    type = serializers.ChoiceField(choices=(('withdraw', 'Withdraw'), ('deposit', 'Deposit')))


class AccountStatementSerializer(serializers.Serializer):
    number_account = serializers.IntegerField()
    agency_account = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()

    def validate_month(self, value):
        validator = Validator()

        if not validator.validate_month(value):
            raise serializers.ValidationError('Mês inválido')
        
        return value
    
    def validate_year(self, value):
        validator = Validator()

        if not validator.validate_year(value):
            raise serializers.ValidationError('Ano inválido')

        return value

class AccountStatementDeserializer(serializers.Serializer):
    created_at = serializers.DateField()
    value = serializers.FloatField()
    transaction_type = serializers.CharField()


class DeactivateAccountSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    agency = serializers.IntegerField()