from datetime import date


def diferenca_tempo(data_inicial, data_final=date.today()):

    diff = data_final - data_inicial

    dias = diff.days
    anos, dias = int(dias // 365), dias % 365
    meses, dias = int(dias // 30), dias % 30
    meses = meses + (anos * 12)
    dias = diff.days

    return anos, meses, dias
