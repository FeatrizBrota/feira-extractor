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
        link_mapa = item.find('a', id='hlkMapa').text.strip()


        # Converter a observação para o novo formato
        dadosObs = converter_observacao(observacao)
        # print('dadosobs: ',dadosObs)
        dias, horarios = extrair_dias_horarios(dadosObs)
        # print('Dias da Semana:', dias)
        # print('Horários:', horarios)

        numeros1 = converter_dias_para_numeros(dias)
        dia_semana = numeros1
        horario_inicial, horario_final = converter_horarios(horarios)

        # Crie um dicionário com os dados do item "Guia"
        guia_dict = {
            'tipoart': tipo_feira,
            'titulo': titulo,
            'endereco': endereco,
            'bairro': bairro,
            'telefone': telefone,
            'dia_da_semana': dia_semana,
            'horario_inicial': horario_inicial,
            'horario_final': horario_final,
            'link_mapa': link_mapa,
            'referencia':''
        
        }
        
        dados_feiras.append(guia_dict)
    
    return dados_feiras

def converter_horarios(array_horarios):
    horarios_iniciais = []
    horarios_finais = []
    
    for i in range(0, len(array_horarios), 2):
        horario_inicial = array_horarios[i]
        
        if i + 1 < len(array_horarios):
            horario_final = array_horarios[i + 1]
            horarios_finais.append(horario_final)
        else:
            horario_final = ''  # Tratar o caso em que não há horário final
            horarios_finais.append(horario_final)
        
        horarios_iniciais.append(horario_inicial)
    
    return horarios_iniciais, horarios_finais

def extrair_dias_horarios(linha):
    dias_semana = []
    horarios = []

    for palavra in linha:
            # Verificar se a palavra é um dia da semana
        if palavra.endswith('-feira') or palavra.endswith('s') and palavra not in ['das', 'às']:
            dias_semana.append(palavra)
            # Verificar se a palavra possui formato de horário (exemplo: "08h" ou "13h")
        elif palavra.endswith('h'):
            horarios.append(palavra)

    return dias_semana, horarios


def converter_dias_para_numeros(dias_semana):
    dias_numeros = []
    dias_da_semana = ['Domingos', 'Segundas', 'Terças', 'Quartas', 'Quintas', 'Sextas', 'Sábados']
    
    for dia in dias_semana:
        # Verificar se o dia está presente na lista de dias da semana
        if dia in dias_da_semana:
            dia_numero = dias_da_semana.index(dia)
            dias_numeros.append(dia_numero)
    
    return dias_numeros





def converter_observacao(observacao):
    dias_semana = []

    # Remover espaços em branco extras e dividir a observação em palavras
    observacao_split = observacao.strip().split()
    return observacao_split


# Função para salvar os dados em formato JSON
def salvar_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False)

def salvar_no_banco_de_dados(dados_feiras):
    url = 'http://localhost:3000/feiras'
    
    for feira in dados_feiras:
        # Converter o dicionário para formato JSON
        payload = json.dumps(feira)
        
        # Definir o cabeçalho da requisição
        headers = {'Content-Type': 'application/json'}
        
        # Enviar a requisição POST para a rota
        response = requests.post(url, data=payload, headers=headers)
        
        # Verificar o código de resposta
        if response.status_code == 200:
            print('Feira salva com sucesso:', feira)
        else:
            print('Erro ao salvar feira:', feira)
            print('Código de resposta:', response.status_code)



url='https://m-turismo.curitiba.pr.gov.br/conteudos/artesanato/17/'
tipo_feira = input("Digite o tipo de feira: ")

# Extrair dados do site
dados_feiras = extrair_dados_do_site(url, tipo_feira)


# Chamar a função para salvar os dados no banco de dados
salvar_no_banco_de_dados(dados_feiras)

# Salvar dados em JSON
salvar_em_json(dados_feiras, 'feiras.json')

# Salvar dados no MongoDB
# salvar_no_mongodb(dados_feiras)
