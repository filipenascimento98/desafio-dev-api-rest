from django.db import models


class Portador(models.Model):
    full_name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, primary_key=True)


class DigitalAccount(models.Model):
    portador = models.ForeignKey(
        Portador,
        related_name='digital_account',
        on_delete=models.DO_NOTHING
    )
    current_balance = models.FloatField(default=0)
    number = models.IntegerField()
    agency = models.IntegerField()
    active = models.BooleanField(default=False)
    blocked = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['number', 'agency'], name='unique_number_agency')
        ]


class Transaction(models.Model):
    digital_account = models.ForeignKey(
        DigitalAccount,
        related_name='transaction',
        on_delete=models.DO_NOTHING
    )
    value = models.FloatField()
    transaction_type = models.CharField(choices=(('withdraw', 'Withdraw'), ('deposit', 'Deposit')))
    created_at = models.DateField(auto_now_add=True)