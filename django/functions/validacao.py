import re


def validador_cpf(cpf: str):

    #   Retorno:
    #       bool:
    #           - Falso, quando o CPF não possuir 11 caracteres numéricos;
    #           - Falso, quando os dígitos verificadores forem inválidos;
    #           - Verdadeiro, caso contrário.

    #   Obtém apenas os números do CPF, ignorando pontuações
    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    #   Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numeros) != 11 or len(set(numeros)) == 1:
        texto = 'CPF com menos de 11 digitos ou todos os digitos são iguais'
        return False, texto, cpf

    #   Validação do primeiro dígito verificador:
    soma_dos_produtos = sum(
        a*b for a, b in zip(numeros[0:9], range(10, 1, -1))
    )
    calculo_digito = (soma_dos_produtos * 10 % 11) % 10
    if numeros[9] != calculo_digito:
        texto = 'CPF com cálculo inválido.'
        return False, texto, cpf

    #   Validação do segundo dígito verificador:
    soma_dos_produtos = sum(
        a*b for a, b in zip(numeros[0:10], range(11, 1, -1))
    )
    calculo_digito = (soma_dos_produtos * 10 % 11) % 10
    if numeros[10] != calculo_digito:
        texto = 'CPF com cálculo inválido.'
        return False, texto, cpf

    #   Aplica a máscara
    cpf = '{}{}{}.{}{}{}.{}{}{}-{}{}'.format(
        numeros[0], numeros[1], numeros[2], numeros[3], numeros[4], numeros[5],
        numeros[6], numeros[7], numeros[8], numeros[9], numeros[10]
    )

    texto = 'CPF válido'
    return True, texto, cpf


def validador_cnpj(cnpj: str):
    numeros = [int(digito) for digito in cnpj if digito.isdigit()]

    #   Verifica se o CNPJ possui 14 números ou se todos são iguais:
    if len(numeros) != 14 or len(set(numeros)) == 1:
        texto = 'CNPJ com menos de 14 digitos ou todos os digitos são iguais'
        return False, texto, numeros

    #   Validação do primeiro dígito verificador:
    lista = []
    peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(0, len(numeros) - 2):
        lista.append(numeros[i] * peso[i])
    soma_dos_produtos = sum(lista)
    calculo_digito = soma_dos_produtos % 11
    if calculo_digito == 0 or calculo_digito == 1:
        calculo_digito = 0
    elif 2 <= calculo_digito and calculo_digito <= 10:
        calculo_digito = 11 - calculo_digito
    if numeros[12] != calculo_digito:
        texto = 'CPF com cálculo inválido.'
        return False, texto, numeros

    #   Validação do segundo dígito verificador:
    lista = []
    peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(0, len(numeros) - 1):
        lista.append(numeros[i] * peso[i])
    soma_dos_produtos = sum(lista)
    calculo_digito = soma_dos_produtos % 11
    if calculo_digito == 0 or calculo_digito == 1:
        calculo_digito = 0
    elif 2 <= calculo_digito and calculo_digito <= 10:
        calculo_digito = 11 - calculo_digito
    if numeros[13] != calculo_digito:
        texto = 'CPF com cálculo inválido.'
        return False, texto, numeros

    #   Aplica a máscara
    cnpj = '{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}'.format(
        numeros[0], numeros[1], numeros[2], numeros[3], numeros[4], numeros[5],
        numeros[6], numeros[7], numeros[8], numeros[9], numeros[10], numeros[11],
        numeros[12], numeros[13]
    )

    texto = 'CNPJ válido'
    return True, texto, cnpj


def cpf_ou_cnpj(digitos):
    try:
        #   Retira não numericos
        digitos = re.sub(r"\D", "", digitos)
        if len(digitos) == 11:
            status, texto, documento = validador_cpf(digitos)
        elif len(digitos) == 14:
            status, texto, documento = validador_cnpj(digitos)
        else:
            texto = 'Quantidade inválida de digitos.'
            status = False
            documento = digitos

        return status, texto, documento
    except Exception as e:
        print('>>> Erro:  functions.validacao__cpf_ou_cnpj: {}'.format(e))
