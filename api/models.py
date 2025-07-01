from django.db import models


class Portador(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, primary_key=True)


class ContaDigital(models.Model):
    portador = models.OneToOneField(
        Portador,
        related_name='conta_digital',
        on_delete=models.DO_NOTHING
    )
    saldo_atual = models.FloatField()
    numero = models.IntegerField()
    agencia = models.IntegerField()
    ativa = models.BooleanField(default=False)
    bloqueada = models.BooleanField(default=False)


class Transacao(models.Model):
    conta_digital = models.ForeignKey(
        ContaDigital,
        related_name='transacao',
        on_delete=models.DO_NOTHING
    )
    valor = models.FloatField()
    data = models.DateField()
    tipo_transacao = models.CharField(choices=(('saque', 'Saque'), ('deposito', 'Deposito')))