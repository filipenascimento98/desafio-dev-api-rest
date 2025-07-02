from django.db import models


class Portador(models.Model):
    full_name = models.CharField(max_length=100)
    document = models.CharField(max_length=11, primary_key=True)


class Account(models.Model):
    portador = models.ForeignKey(
        Portador,
        related_name='account',
        on_delete=models.DO_NOTHING
    )
    current_balance = models.FloatField(default=0)
    number = models.IntegerField()
    agency = models.IntegerField()
    active = models.BooleanField(default=True)
    blocked = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['number', 'agency'], name='unique_number_agency')
        ]


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        related_name='transaction',
        on_delete=models.DO_NOTHING
    )
    value = models.FloatField()
    transaction_type = models.CharField(choices=(('withdraw', 'Withdraw'), ('deposit', 'Deposit')))
    created_at = models.DateField(auto_now_add=True)