"""
Testes de requests para a taxa referencial

"""
import requests
from datetime import datetime

data_inicio = datetime.strptime(input("Digite a data de inicio do investimento no formato dd/mm/aaaa: "), '%d/%m/%Y')
data_fim = datetime.strptime(input("Digite a data final do investimento no formato dd/mm/aaaa: "), '%d/%m/%Y')
data_inicio_formatada = data_inicio.strftime('%d/%m/%Y')
data_fim_formatada = data_fim.strftime('%d/%m/%Y')

ts = requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial={data_inicio_formatada}&dataFinal={data_fim_formatada}")
tr = requests.get(f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.226/dados?formato=json&dataInicial={data_inicio_formatada}&dataFinal={data_fim_formatada}')

taxas_selic: dict = ts.json()
taxas_referencial: dict = tr.json()
print(taxas_selic)
print(taxas_referencial)



tr1 =[]

# taxa = [item['data'] == data_inicio_formatada for item in taxas_referencial]

for item in taxas_referencial:
    if item['data'] == data_inicio_formatada or item['data'] == data_fim_formatada:
        tr1.append(item)


print(tr1)

