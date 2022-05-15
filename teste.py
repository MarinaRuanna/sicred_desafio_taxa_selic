"""
Questão 2: Calcular o rendimento da poupança de acordo com os seguintes requisitos:

  - As entradas são: valor, quantidade de meses, taxa SELIC, e Taxa Referencial;
  - Se a SELIC estiver abaixo de 8.5, a poupança rende 70% de Taxa SELIC e Taxa Referencial (ao mês)
  - Se a SELIC estiver acima, a poupança rende 0.5% + Taxa Referencial (ao mês);
  - A saída deve ser o resultado do investimento (inicial + rendimento).

Questão 3: Retorna não apenas o resultado, mas retorna de forma estruturada:
 - o valor inicial;
 - resultado final do investimento;
 - resultado do rendimento mês a mês;

"""
import requests
from datetime import datetime

def rendimento_poupanca(valor_inicial: float, selic: list, referencial: list) -> float:

    rendimento = []
    print('\n------------------')
    print('Rendimento ao mes:')
    print('------------------')
    for i in selic:
        mes: int = 1
        if i < 8.5:
            rendimento_mes: float = i * 0.70
            for j in referencial:
                rendimento_mes = rendimento_mes + j

            print(f'\nMes {mes}: \nTaxa SELIC: {i} - Rendimento: R$ {rendimento_mes:.3}')
            mes = mes + 1
            rendimento.append(rendimento_mes)


        elif i >= 8.5:
            rendimento_mes: float = valor_inicial * 0.05
            for j in referencial:
                rendimento_mes = rendimento_mes + j
            print(f'Mes: {mes} - Taxa SELIC: {i} - Rendimento: R$ {rendimento_mes:.3}')
            mes = mes + 1
            rendimento.append(rendimento_mes)


        rendimento_total = sum(rendimento)
        resultado_investimento = valor_inicial + rendimento_total
        print('\n----------------------------')
        print('Informações do investimento:')
        print('----------------------------')
        print(f'Investimento inicial: R$ {valor_inicial:.2f}\nRendimento total: R$ {rendimento_total:.2f}\nResultado final do investimento: R$ {resultado_investimento:.2f}\n')
        return float(resultado_investimento)


try:
    investimento_inicial: float = float(input("Digite o valor do investimento inicial: "))
    data_inicio = datetime.strptime(input("Digite a data de inicio do investimento no formato dd/mm/aaaa: "), '%d/%m/%Y')
    data_fim = datetime.strptime(input("Digite a data final do investimento no formato dd/mm/aaaa: "), '%d/%m/%Y')

    data_inicio_formatada = data_inicio.strftime('%d/%m/%y')
    data_fim_formatada = data_fim.strftime('%d/%m/%y')


    ts = requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial={data_inicio_formatada}&dataFinal={data_fim_formatada}")
    tr = requests.get(f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.226/dados?formato=json&dataInicial={data_inicio_formatada}&dataFinal={data_fim_formatada}')

    taxas_selic: dict = ts.json()
    taxas_referencial: dict = tr.json()

    valores_selic = [float(item['valor']) for item in taxas_selic]
    valores_referencial: list = [float(item['valor']) for item in taxas_referencial]

    """
    Chamando a função e aplicando os parâmetros fornecidos pelo usuário.
    """
    rendimento_poupanca(investimento_inicial, valores_selic, valores_referencial)

except ValueError:
    print('Dados digitados são inválidos.')
    pass




def test_rendimento_poupanca() -> None:
    """
    Fiz o calculo manualmente para garantir que o valor seria exato
    """
    print('\n-------------')
    print('Texte Assert:')
    print('-------------')
    assert rendimento_poupanca(1, [10, 5.0, 0.20, 0.30], [0.0, 0.0, 0.0, 0.0]) == 4.90

