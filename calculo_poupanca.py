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

 Questão Bônus: Descrever ou escrever testes para garantir que o código funciona nos casos mais comuns
                (acima da SELIC, abaixo da SELIC, etc).

"""
import requests
from datetime import datetime

def main() -> None:
    dados = inserir_dados()
    investimento_inicial, data_inicial, data_final = dados

    selic_referencial = buscar_selic_referencial(data_inicial, data_final)
    valor_referencial_mesal, valores_selic = selic_referencial

    rendimento_poupanca(investimento_inicial, valores_selic, valor_referencial_mesal)


def rendimento_poupanca(valor_inicial: float, selic: list, referencial: float) -> float:
    """
    A função recebe o valor de investimento inicial e o periodo de duração do investimento, retornando o valor do
    rendimento mês a mês e o resultado do investimento ao final do periodo informado. O parametro com a quantidade
    de meses ficaria redundante, já que é possivel calcular a quantidade de meses a partir da lista com com os valores
    da Taxa SELIC gerados na função buscar_selic_referencial()

    """

    mes: int = 1
    rendimento = []

    print('\n------------------')
    print('Rendimento ao mes:')
    print('------------------')
    for i in selic:
        if i >= 8.5: # Nesse caso a porcentagem de rendimento é fixa em 0.5
            rendimento_mes: float = valor_inicial * 0.05 + referencial


        else: # 70% da taxa SELIC se torna a porcentagem de rendimento da poupança
            rendimento_mes: float = valor_inicial * ((i * 0.70)/100) + referencial


        rendimento.append(rendimento_mes)
        print(f'\nMes: {mes}:\n----\nTaxa SELIC: {i} - Rendimento: R$ {rendimento_mes:.3}')
        mes = mes + 1

    print(rendimento)
    rendimento_total = sum(rendimento)
    resultado_investimento = valor_inicial + rendimento_total
    print('\n----------------------------')
    print('Informações do investimento:')
    print('----------------------------')
    print(f'Investimento inicial: R$ {valor_inicial:.2f}\nRendimento total: R$ {rendimento_total:.2f}\nResultado final do investimento: R$ {resultado_investimento:.2f}\n')
    return float(resultado_investimento)



def inserir_dados() -> tuple[float, str, str]:
    """
    A função recebe os dados variáveis que são informados pelo usuário. As variáveis de datas de inicio e fim do
    investimento são convertidas de string para date e depois novamente de date para string, para tratamento de dados,
    e para a aplicação se tornar mais precisa, evitando que o usuário gere dicionários aleatorios e imprecisos.
    """

    try:
        investimento_inicial: float = float(input("Digite o valor do investimento inicial: "))
        data_inicio = datetime.strptime(input("Digite a data de inicio do investimento no formato dd/mm/aaaa: "), '%d/%m/%Y')
        data_fim = datetime.strptime(input("Digite a data final do investimento no formato dd/mm/aaaa: "), '%d/%m/%Y')

        data_inicio_formatada = data_inicio.strftime('%d/%m/%y')
        data_fim_formatada = data_fim.strftime('%d/%m/%y')
        return  investimento_inicial, data_inicio_formatada, data_fim_formatada

    except ValueError:
        print('Dados digitados são inválidos.')
        pass


def buscar_selic_referencial(data_inicial: str, data_final: str) -> tuple[float, list]:
    """
    Essa função faz um request dos valores da taxa SELIC por mês no periodo informado pelo usuário.
    Também é feito um request para os valores da Taxa de Rendimento, mas o único arquivo .json que encontrei foi o disponibilizado
    pelo BACEN, e o mesmo fornece um dicionário dos valores diários no periodo informado pelo usuário,
    como a Taxa de Rendimento mensal é a soma dos valores das Taxas de Rendimento diários eu fiz um calculo da média
    desses valores no periodo informado pelo usuário. Sei que isso torna o calculo menos preciso, mas acredito que com
    mais tempo poderei implementar um calculo mais satisfatório com informações mais precisas.
    """

    ts = requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}")
    tr = requests.get(f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.226/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}')

    taxas_selic: dict = ts.json()
    taxas_referencial: dict = tr.json()

    valores_selic = [float(item['valor']) for item in taxas_selic]
    valores_referencial = [float(item['valor']) for item in taxas_referencial]

    meses = len(valores_selic)
    valor_referencial_mesal = ((sum(valores_referencial) / meses)/100)

    return valor_referencial_mesal, valores_selic



def test_rendimento_poupanca() -> None:
    """
    Fiz o calculo manualmente para garantir que o valor seria exato
    """
    print('\n-------------')
    print('Texte Assert:')
    print('-------------')
    assert rendimento_poupanca(1, [10, 5.0, 0.20, 0.30], 0) == 4.90



if __name__ == '__main__':
    main()

