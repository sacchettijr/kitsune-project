from django.db import models
from datetime import date
from decimal import Decimal
from django.dispatch import receiver
from django.utils.timezone import now
from usuario.models import UsuarioModel
from django.db.models.signals import post_save
from functions.investimento import calculo_retirada, calculo_saldo
from functions.tempo import diferenca_tempo
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class InvestimentoModel(models.Model):
    proprietario = models.ForeignKey(UsuarioModel, on_delete=models.DO_NOTHING)
    valor_investido = models.DecimalField(
        'Valor investido', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    data_investimento = models.DateField(
        'Data do investimento', default=now,
        validators=[
            #   Impede datas futuras
            MaxValueValidator(limit_value=date.today)
        ]
    )
    meses_de_investimento = models.PositiveIntegerField(
        'Meses de investimento', null=True, blank=True
    )

    #  False = Já retirado, True = Ainda aberto
    status = models.BooleanField('Status', default=True)

    class Meta:
        db_table = 'investimento'
        verbose_name = 'Investimento'
        verbose_name_plural = 'Investimentos'
        ordering = ('-pk',)

    def __str__(self):
        return 'Id: {} - Valor: {}'.format(self.pk, self.valor_investido)

    def save(self, *args, **kwargs):
        try:
            anos, meses, dias = diferenca_tempo(self.data_investimento)
            self.meses_de_investimento = meses

            return super().save(*args, **kwargs)
        except Exception as e:
            print('>>> Investimento.models.InvestimentoModel: {}'.format(e))
            return e


#   Quando o insert é feito nos investimentos dispara uma função e calcula coisas como o saldo.
#   Então aplica no campo, na tabela de usuário
@receiver(post_save, sender=InvestimentoModel)
def investimento_post_save_receiver(sender, instance, **kwargs):

    usuario = instance.proprietario.pk
    saldo_b, saldo_l = calculo_saldo(
        InvestimentoModel.objects.filter(
            proprietario=usuario,
            status=True
        )
    )

    usuario_tb = UsuarioModel.objects.get(
        pk=usuario
    )
    usuario_tb.saldo = saldo_b
    usuario_tb.save()


class RetiradaModel(models.Model):
    investimento = models.OneToOneField(InvestimentoModel, on_delete=models.DO_NOTHING)
    data_retirada = models.DateField(
        default=now,
        validators=[
            MaxValueValidator(limit_value=date.today),
        ]
    )

    taxa_ganho = models.DecimalField(
        'Taxa de ganho', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    taxa_tributo = models.DecimalField(
        'Taxa de tributo', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    imposto = models.DecimalField(
        'Imposto', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    lucro_bruto = models.DecimalField(
        'Lucro bruto', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    lucro_liquido = models.DecimalField(
        'Lucro líquido', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    valor_final_b = models.DecimalField(
        'Valor de retorno bruto', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )
    valor_final_l = models.DecimalField(
        'Valor de retorno líquido', max_digits=15, decimal_places=2,
        validators=[
            #   Impede valor menor que 0
            MinValueValidator(Decimal('0.00'))
        ]
    )

    class Meta:
        db_table = 'retirada'
        verbose_name = 'Retirada'
        verbose_name_plural = 'Retiradas'
        ordering = ('-pk',)

    def __str__(self):
        return 'ID: {} - INVESTIMENTO: {} - DATA DE RETIRADA: {}'.format(
            self.pk, self.investimento.pk, self.data_retirada.strftime('%d/%m/%Y'))

    #   TODO: corrigir - exibir o erro para o campo e não para o form
    def clean(self):
        if self.data_retirada < self.investimento.data_investimento:
            raise ValidationError('A data de retirada não pode ser anterior à data de investimento')
        return super().clean()

    def save(self, *args, **kwargs):
        try:
            #   Método save reescrito para que apenas receba o id do investimento e a data
            #   em que está sendo feito a retirada. Tendo esses dados, ele já calcula todas
            #   as outras informações e salva na tabela de forma automatica.

            # Se for um INSERT
            if not self.pk:

                dados = calculo_retirada(
                    self.investimento.valor_investido,
                    self.investimento.data_investimento
                )

                self.taxa_ganho = dados['taxa_ganho']
                self.taxa_tributo = dados['taxa_tributo']
                self.imposto = dados['imposto']
                self.lucro_bruto = dados['lucro_bruto']
                self.lucro_liquido = dados['lucro_liquido']
                self.valor_final_b = dados['valor_final_b']
                self.valor_final_l = dados['valor_final_l']

            # Se for um UPDATE
            else:
                pass
            return super().save(*args, **kwargs)
        except Exception as e:
            print('>>> Investimento.models.RetiradaModel: {}'.format(e))
            return e


@receiver(post_save, sender=RetiradaModel)
def retirada_post_save_receiver(sender, instance, **kwargs):
    try:
        #   Quando o insert é feito nas retiradas dispara uma função onde calcula o saldo e aplica
        #   na tabela de usuário e muda o status do investimento para False.

        usuario = instance.investimento.proprietario.pk
        investimento = instance.investimento.pk

        investimento_tb = InvestimentoModel.objects.get(
            pk=investimento
        )
        investimento_tb.status = False
        investimento_tb.save()

        saldo_b, saldo_l = calculo_saldo(
            InvestimentoModel.objects.filter(
                proprietario=usuario,
                status=True
            )
        )

        usuario_tb = UsuarioModel.objects.get(
            pk=usuario
        )
        usuario_tb.saldo = saldo_b
        usuario_tb.save()
    except Exception as e:
        print('>>> Investimento.models.RetiradaModel__post_save: {}'.format(e))
