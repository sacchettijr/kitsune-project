from functions.tempo import diferenca_tempo
from decimal import Decimal
from datetime import date


def calculo_saldo(investimentos):
    try:

        #   Inicia as variaveis
        dados = []
        calculo_ganho_b = 0
        calculo_ganho_l = 0

        #   Recebendo a lista de investimentos, faz uma redundância para verificar se o status ainda está
        #   verdadeiro (não feito a retirada) e sendo ela verdadeira, adiciona os valores a um arreio usando
        #   o calculo de retirada como simulação.
        for investimento in investimentos:
            if investimento.status == True:
                dados.append(
                    calculo_retirada(
                        investimento.valor_investido,
                        investimento.data_investimento
                    )
                )

        #   Recebe a lista com os calculos feitos e então é feito um arreio para somar todos os valores.
        #   C é utilizado como um contador para localizar as posições na lista dados.
        c = 0
        for i in dados:

            calculo_ganho_b += dados[c]['valor_final_b']
            calculo_ganho_l += dados[c]['valor_final_l']
            c += 1

        return calculo_ganho_b, calculo_ganho_l
    except Exception as e:
        print('>>> Erro: functions.investimento__calculo_saldo: {}'.format(e))


def calculo_retirada(valor_investido, data_investimento, data_retirada=date.today(), taxa=0.52):

    try:
        #   Recebe a taxa e valor investido
        valor_investido = Decimal(valor_investido)
        taxa = Decimal(taxa)

        #   Calcula quanto tempo passou desde a data do investimento até a retirada
        anos, meses, dias = diferenca_tempo(data_investimento, data_retirada)

        # Inicia a variavel
        valor_final_b = valor_investido

        #   Aplica a porcentagem
        taxa_ganho = taxa / 100

        #   Verifica se passou pelo menos 1 mês.
        #   Se passou, faz um laço para somar o valor total com a porcentagem de ganho do mês
        if not meses == 0:
            for i in range(meses):
                valor_final_b = valor_final_b + (valor_final_b * taxa_ganho)

        #   Calcula o lucro bruto
        lucro_bruto = valor_final_b - valor_investido

        # Baseado em quantos anos passaram, define o imposto
        if anos < 1:
            taxa_tributo = 22.5
        elif anos >= 1 and anos < 2:
            taxa_tributo = 18.5
        elif anos >= 2:
            taxa_tributo = 15.0

        #   Aplica a porcentagem
        taxa_tributo = Decimal(taxa_tributo / 100)

        #   Calcula o imposto baseado no lucro
        imposto = lucro_bruto * taxa_tributo

        #   Calcula os ganhos liquidos
        lucro_liquido = lucro_bruto - imposto
        valor_final_l = valor_investido + lucro_liquido

        #   Retorna um dicionário com todos os dados
        dados = {
            'taxa_ganho': taxa_ganho,
            'taxa_tributo': taxa_tributo,
            'imposto': imposto,
            'lucro_bruto': lucro_bruto,
            'lucro_liquido': lucro_liquido,
            'valor_final_b': valor_final_b,
            'valor_final_l': valor_final_l
        }

        return dados
    except Exception as e:
        print('>>> Erro: functions.investimento__calculo_retirada: {}'.format(e))
