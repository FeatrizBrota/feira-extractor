import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from datetime import datetime, timedelta

# Função para extrair dados do site e retornar uma lista de dicionários
def extrair_dados_do_site(url, tipo_feira):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    dados_feiras = []
    
    # Realize a extração dos dados do item "Guia"
    itens_guia = soup.find_all('div', class_='itemGuia')
    
    for item in itens_guia:
        titulo = item.find('span', class_='txtTitGuia').text.strip()
        endereco = item.find('span', id='lblEndereco').text.strip()
        bairro = item.find('span', id='lblBairro').text.strip()
        telefone = item.find('span', id='lblTelefone').text.strip()
        observacao = item.find('span', id='lblObservacao').text.strip()
        
        # Converter a observação para o novo formato
        dia_semana, horario_inicial, horario_final = converter_observacao(observacao)
        
        # Crie um dicionário com os dados do item "Guia"
        guia_dict = {
            'tipo_feira': tipo_feira,
            'titulo': titulo,
            'endereco': endereco,
            'bairro': bairro,
            'telefone': telefone,
            'observacao': {
                'dia_da_semana': dia_semana,
                'horario_inicial': horario_inicial,
                'horario_final': horario_final
            }
        }
        
        dados_feiras.append(guia_dict)
    
    return dados_feiras

# Função para converter a observação para o novo formato
def converter_observacao(observacao):
    dias_semana = []

    # Remover espaços em branco extras e dividir a observação em palavras
    observacao_split = observacao.strip().split()

    # Verificar os diferentes tipos de padrões de observação
    if len(observacao_split) == 5 and observacao_split[1] == 'das':
        # Padrão: "<dia> das <horario_inicial> às <horario_final>"
        dia_semana_str = observacao_split[0]
        
        dia_semana = obter_dia_semana(dia_semana_str)
        dias_semana.append(dia_semana)
    
    elif len(observacao_split) >= 5 and observacao_split[1] == 'e':
        # Padrão: "<dia1> e <dia2> das <horario_inicial> às <horario_final> ..."
        dias_semana_str = observacao_split[0:observacao_split.index('das')]
        
        for dia_semana_str in dias_semana_str:
            dia_semana = obter_dia_semana(dia_semana_str)
            dias_semana.append(dia_semana)
    
    return dias_semana

def obter_dia_semana(dia_semana_str):
    dia_semana = -1
    
    if dia_semana_str.lower() == 'domingos' or dia_semana_str.lower() == 'domingo':
        dia_semana = 0
    elif dia_semana_str.lower() == 'segundas' or dia_semana_str.lower() == 'segunda':
        dia_semana = 1
    elif dia_semana_str.lower() == 'terças' or dia_semana_str.lower() == 'terça':
        dia_semana = 2
    elif dia_semana_str.lower() == 'quartas' or dia_semana_str.lower() == 'quarta':
        dia_semana = 3
    elif dia_semana_str.lower() == 'quintas' or dia_semana_str.lower() == 'quinta':
        dia_semana = 4
    elif dia_semana_str.lower() == 'sextas' or dia_semana_str.lower() == 'sexta':
        dia_semana = 5
    elif dia_semana_str.lower() == 'sábados' or dia_semana_str.lower() == 'sábado' or dia_semana_str.lower() == 'sabado':
        dia_semana = 6
    
    return dia_semana


# Função para salvar os dados em formato JSON
def salvar_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False)

# Função para salvar os dados no banco de dados MongoDB
def salvar_no_mongodb(dados):
    client = MongoClient('localhost', 27017)  # Substitua pelas configurações reais do seu banco de dados
    db = client['feiras']
    colecao = db['dados']
    
    # Insira os dados na coleção
    colecao.insert_many(dados)

# Solicitar ao usuário o link do site e o tipo de feira
url = input("Digite o link do site: ")
tipo_feira = input("Digite o tipo de feira: ")

# Extrair dados do site
dados_feiras = extrair_dados_do_site(url, tipo_feira)

# Salvar dados em JSON
salvar_em_json(dados_feiras, 'feiras.json')

# Salvar dados no MongoDB
# salvar_no_mongodb(dados_feiras)
