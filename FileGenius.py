import re
import os
from datetime import datetime


# Define a estrutura do arquivo
HEADER_ARQUIVO = "0"
HEADER_LOTE = "1"
REGISTRO_DETALHE = "3"
TRAILER_LOTE = "5"
TRAILER_ARQUIVO = "9"

# Define o nome do arquivo de saída
nome_arquivo_saida = 'Relatório.txt'
      
# verifica se o arquivo já existe
if os.path.exists(nome_arquivo_saida):
    i = 1
    while os.path.exists(f"Relatório({i}).txt"):
        i += 1
    nome_arquivo_saida = f"Relatório({i}).txt"

# Variável para escrever no relatório
def armazenar_em_relatorio(nome_arquivo_saida, header_arquivo_list, header_lote_list, registro_detalhe_list):
  with open(nome_arquivo_saida, 'a') as arquivo_saida:
      arquivo_saida.write('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
      arquivo_saida.write('{:<30} | {:<30} | {:<13} | {:<40} | {:<15} | {:<20} | {:<10} | {:<2}\n'.format('Nome da Empresa', 'Numero de Inscricao da Empresa', 'Nome do Banco', 'Nome da Rua', 'Numero do Local', 'Nome da Cidade', 'CEP', 'Sigla do Estado'))
      arquivo_saida.write('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
  
      # Escreve os dados do header do arquivo
      for item in header_arquivo_list:
          nome_empresa = item.get('nome_empresa', '')
          cnpj_empresa = item.get('cnpj_empresa', '')
          nome_banco = item.get('nome_banco', '')
    
      for item in header_lote_list:
          endereco_empresa = item.get('endereco_empresa', '')
          numero_local = item.get('numero_local', '')
          cidade_empresa = item.get('cidade_empresa', '')
          cep_empresa = item.get('cep_empresa', '')
          estado_empresa = item.get('estado_empresa', '')
  
          arquivo_saida.write('{:<30} | {:<30} | {:<13} | {:<40} | {:<15} | {:<20} | {:<10} | {:<2}\n'.format(nome_empresa, cnpj_empresa, nome_banco, endereco_empresa, numero_local, cidade_empresa, cep_empresa, estado_empresa))
          
  
      arquivo_saida.write('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
      arquivo_saida.write('{:<30} | {:<17} | {:<16} | {:<40} | {:<20}\n'.format('Nome do Favorecido', 'Data de Pagamento', 'Valor do Pagamento', 'Numero do Documento Atribuido pela Empresa', 'Forma de Lancamento'))
      arquivo_saida.write('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
  
      # Escreve os dados dos registros detalhe
      for item in registro_detalhe_list:
          nome_favorecido = item.get('nome_favorecido', '')
          data_pagamento = item.get('data_pagamento', '')
          valor_pagamento = item.get('valor_pagamento', '')
          numero_documento = item.get('numero_documento', '')
          forma_lancamento = item.get('forma_lancamento', '')
  
          arquivo_saida.write('{:<30} | {:<17} | {:<18} | {:<42} | {:<20}\n'.format(nome_favorecido, data_pagamento, valor_pagamento, numero_documento, forma_lancamento))
  
      # Escreve o rodapé do relatório
      arquivo_saida.write('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')


# Define o tamanho de cada campo
TAMANHO_CAMPO = {
    "tipo_registro": 1,
    "nome_empresa": 30,
    "nome_banco": 30,
    "cnpj_empresa": 14,
    "endereco_empresa": 40,
    "numero_local": 8,
    "cidade_cep_estado": 50,
    "bairro:": 40,
    "cidade": 40,
    "cidade_empresa": 15,
    "cep_empresa": 8,
    "estado_empresa": 2,
    "forma_lancamento": 2,
    "nome_favorecido": 30,
    "data_pagamento": 8,
    "valor_pagamento": 13,
    "numero_documento": 20,
}

# Lista para armazenar as informações
header_arquivo_list = []
header_lote_list = []
registro_detalhe_list = []
trailer_lote_list = []
trailer_arquivo_list = []

# Abre o arquivo e modifica para ser tratado pela app
with open('modelo_arquivo.txt', 'r') as modelo_arquivo:
    conteudo = modelo_arquivo.read()

conteudo_modificado = re.sub(' +', '\t', conteudo)

with open('arquivo_modificado.txt', 'w') as arquivo_modificado:
    arquivo_modificado.write(conteudo_modificado)

# Abre o arquivo modificado para extrair informações úteis
with open('arquivo_modificado.txt', 'r') as arquivo_entrada:
    for linha in arquivo_entrada:
      
        # Encerra o loop caso não tenha mais linhas
        if not linha:
          break
        tipo_registro = linha[7]

        # Condição para saber se a linha é um Header de arquivo, caso seja extrai dados
        if tipo_registro == '0':
          HEADER_ARQUIVO
          strings = linha.split('\t')
          header_arquivo_salvo = {}
          nome_empresa = strings[2][20:].strip() + ' ' + strings[3]
          nome_banco = strings[4].strip()
          cnpj_empresa = strings[1][1:15].strip()
          
          print('log de HEADER_ARQUIVO:\n' 'nome da empresa: ' + nome_empresa + '\n' ,'nome do banco: ' + nome_banco + '\n' ,'cnpj da empresa: ' + cnpj_empresa + '\n')
          
          header_arquivo_salvo['nome_empresa'] = nome_empresa
          header_arquivo_salvo['nome_banco'] = nome_banco
          cnpj_empresa = cnpj_empresa
          header_arquivo_salvo['cnpj_empresa'] = re.sub(r"(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})", r"\1.\2.\3/\4-\5", cnpj_empresa)                                             
          header_arquivo_list.append(header_arquivo_salvo)

        # Condição para saber se a linha é um Header de lote, caso seja extrai dados
        if tipo_registro == '1':
          HEADER_LOTE
          strings = linha.split('\t')
          header_lote_salvo = {}
          endereco_empresa = strings[4].strip() + ' ' + strings[5].strip() + ' ' + strings[6].strip()
          numero_local = strings[7].strip()
          cidade_empresa = strings[8][:-10].strip()
          cep_empresa = strings[8][-10:-2].strip()
          estado_empresa = strings[8][-2:].strip() 
          
          print('log de HEADER_LOTE:\n' + 'endereço da empresa: ' + endereco_empresa + '\n' ,'número do local: ' + numero_local + '\n', 'bairro e cidade da empresa: ' + cidade_empresa + '\n', 'cep da empresa:' + cep_empresa + '\n', 'estado da empresa: ' + estado_empresa + '\n')
          
          header_lote_salvo['endereco_empresa'] = endereco_empresa
          header_lote_salvo['numero_local'] = numero_local
          header_lote_salvo['cidade_empresa'] = cidade_empresa
          header_lote_salvo['cep_empresa'] = cep_empresa
          header_lote_salvo['estado_empresa'] = estado_empresa
          header_lote_list.append(header_lote_salvo)
          
        # Condição para saber se a linha é um Registro de detalhe, caso seja extrai dados
        if tipo_registro == '3':
          REGISTRO_DETALHE
          strings = linha.split('\t')
          registro_detalhe_salvo = {}
          forma_lancamento = strings[0][5:7].strip()
          nome_favorecido = strings[0][43:].strip() + ' ' + strings[1].strip() + ' ' + strings[2].strip()
          data_pagamento = strings[4][:8].strip()
          data_pagamento = datetime.strptime(data_pagamento, "%d%m%Y").strftime("%d/%m/%Y")
          valor_pagamento = strings[4][11:].lstrip("0").strip()
          valor_pagamento = float(valor_pagamento)/100
          valor_pagamento = "R${:,.2f}".format(valor_pagamento)
          numero_documento = strings[3].strip()

          #Definindo tradutor para código de forma_lancamento
          if forma_lancamento == '01':
            forma_lancamento = 'Crédito em conta'
          elif forma_lancamento == '02':
            forma_lancamento = 'Cheque pagamento / Administrativo'
          elif forma_lancamento == '03':
            forma_lancamento = 'DOC/TED'
          elif forma_lancamento == '04':
            forma_lancamento = 'Cartão Salário'
          elif forma_lancamento == '05':
            forma_lancamento = 'Crédito em Conta Poupança'
          elif forma_lancamento == '06':
            forma_lancamento = 'Liberação de Títulos HSBC'
          elif forma_lancamento == '07':
            forma_lancamento = 'Emissão de Cheque Salário'
          elif forma_lancamento == '08':
            forma_lancamento = 'Liquidação de Parcelas de Cobrança Não Registrada'
          elif forma_lancamento == '09':
            forma_lancamento = 'Arrecadação de Tributos Federais'
          elif forma_lancamento == '10':
            forma_lancamento = 'OP à Disposição'
          elif forma_lancamento == '11':
            forma_lancamento = 'Pagamento de Contas e Tributos com Código de Barras'
          elif forma_lancamento == '12':
            forma_lancamento = 'Doc Mesma Titularidade'
          elif forma_lancamento == '13':
            forma_lancamento = 'Pagamentos de Guias'
          elif forma_lancamento == '14':
            forma_lancamento = 'Crédito em Conta Corrente Mesma Titularidade'
          elif forma_lancamento == '16':
            forma_lancamento = 'Tributo - DARF Normal'
          elif forma_lancamento == '17':
            forma_lancamento = 'Tributo - GPS (Guia da Previdência Social)'
          elif forma_lancamento == '18':
            forma_lancamento = 'Tributo - IPTU - Prefeituras'
          elif forma_lancamento == '19':
            forma_lancamento = 'Pagamento com Autenticação'
          elif forma_lancamento == '20':
            forma_lancamento = 'Tributo - DARJ'
          else:
            forma_lancamento = 'Código inválido'
          
          registro_detalhe_salvo['forma_lancamento'] = forma_lancamento
          registro_detalhe_salvo['nome_favorecido'] = nome_favorecido
          registro_detalhe_salvo['data_pagamento'] = data_pagamento
          registro_detalhe_salvo['valor_pagamento'] = valor_pagamento
          registro_detalhe_salvo['numero_documento'] = numero_documento
          registro_detalhe_list.append(registro_detalhe_salvo)

          print('log de REGISTRO_DETALHE:\n' + 'forma de lancamento: ' + forma_lancamento + '\n' ,'nome do favorecido: ' + nome_favorecido + '\n' ,'data de pagamento: ' + data_pagamento + '\n' ,'valor de pagamento: ' + valor_pagamento + '\n' ,'número do documento: ' + str(numero_documento) + '\n')
      
        # Condição para saber se a linha é um Trailer de Lote
        if tipo_registro == '5':
          TRAILER_LOTE
          print('log de TRAILER_LOTE: \n' + 'Lotes contidos no HEADER_ARQUIVO encerrados!') 
    
        # Condição para saber se a linha é um Trailer de arquivo, caso seja armazena as informações coletadas no arquivo de relatório, limpa as listas, e retorna ao loop
        if tipo_registro == '9':
          TRAILER_ARQUIVO
          armazenar_em_relatorio(nome_arquivo_saida, header_arquivo_list, header_lote_list, registro_detalhe_list)
          header_arquivo_list.clear()
          header_lote_list.clear()
          registro_detalhe_list.clear()
          print('log de TRAILER_ARQUIVO: \n' + 'Cabeçalhos do arquivo encerrados! \n')

      
        # Condição de erro, caso não seja um dos tipos de registros padrão do documento de entrada
        if not tipo_registro:
          print('erro_1 - Uma das linhas não pode ser lida pelo padrão estar incorreto \n')

# exibe mensagem de finalização
print("Processamento finalizado com sucesso!")