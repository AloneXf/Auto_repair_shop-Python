from datetime import date
from datetime import datetime

#Funções de validação e entrada de dados:

def pedir_nome():
    while True:
        nome = input("Digite o nome do cliente: ").strip()
        if nome.lower() == "sair":
            return "sair"
        elif not nome:
            print("Não deixe esse campo vazio. ")
            continue
        return nome

def pedir_telefone():
    while True:
        telefone = input("Contato do cliente: ").strip()
        if telefone.lower() == "sair":
            return "sair"
        elif telefone == "":
            return None
        elif not telefone.isdigit():
            print("Digite apenas números. ")
            continue
        return telefone

def pedir_moto():
    while True:
        moto = input("Modelo da moto: ").strip()
        if moto.lower() == "sair":
            return "sair"
        elif not moto:
            print("É necessário preencher este campo. ")
            continue
        return moto

def pedir_manutencao():
    while True:     
        manutencao = input("Manutenção feita: ").strip()
        if manutencao.lower() == "sair":
            return "sair"
        elif not manutencao:
            print("É necessário preencher este campo. ")
            continue
        return manutencao

def pedir_data():
    while True:
        try:
            dia = (input("Qual o dia? ")).strip().lower()
            if dia == "sair":
                return "sair"
            mes = (input("Qual o mês? ")).strip().lower()
            if mes == "sair":
                return "sair"
            ano = (input("Qual o ano? ")).strip().lower()
            if ano == "sair":
                return "sair"
            data = date(int(ano), int(mes), int(dia))
            return data
        except ValueError:
            print("Data inválida.")  
        
def padronizar_data(data):
    formatos = ["%Y-%m-%d", "%d/%m/%Y"]
    for formato in formatos:
        try:
            data_convertida = datetime.strptime(data, formato)
            return data_convertida.strftime("%d/%m/%Y")
        except ValueError:
            continue
    return data

def input_inteiro():
    while True:
        try:
            numero = input("Qual? ").strip().lower()
            if numero == "sair":
                return "sair"
            return int(numero)
        except ValueError:
            print("Digite apenas números.")
