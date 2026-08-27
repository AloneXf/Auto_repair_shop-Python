from validacoes import (pedir_nome, pedir_telefone, pedir_moto, pedir_manutencao, pedir_data, padronizar_data, input_inteiro)
from tabelas import (tabela_cliente, tabela_moto, tabela_manutencao)
import sqlite3 as sq

#Funções principais do sistema:

def criar_tabelas(cursor):
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        telefone TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS motos (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        modelo TEXT NOT NULL,

        FOREIGN KEY (cliente_id)
            REFERENCES clientes(id)
    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER PRIMARY KEY,
            moto_id INTEGER NOT NULL,
            servico TEXT NOT NULL,
            data TEXT NOT NULL,
    
            FOREIGN KEY (moto_id)
                REFERENCES motos(id)
        )
        """)

#FUNÇÔES DE CADASTRO DE DADOS###################################################################################################################
    
def cadastrar_cliente(cursor):
    nome = pedir_nome()
    if nome == "sair":
        return "sair"
    telefone = pedir_telefone()
    if telefone == "sair":
        return "sair"
    cursor.execute("""
    INSERT INTO clientes (nome, telefone)
    VALUES (?, ?)
    """, (nome, telefone))
    cliente_id = cursor.lastrowid
    print(f"Cliente {nome} cadastrado. ID: {cliente_id}")

def cadastrar_moto(cursor):
    while True:
        if not tabela_cliente(cursor):
            return
        try:
            cliente_id = (input("Qual o ID do cliente? ")).strip().lower()
            if cliente_id == "sair":
                return "sair"
            else:
                cliente_id = int(cliente_id)
        except ValueError:
            print("Digite um ID válido.")
            continue
        cursor.execute("""
        SELECT id FROM clientes
        WHERE id = ?
        """, (cliente_id,))
        cliente = cursor.fetchone()
        if cliente is None:
            print("Cliente não encontrado.")
            continue
        moto = pedir_moto()
        if moto == "sair":
            return "sair"
        cursor.execute("""
        INSERT INTO motos (cliente_id, modelo)
        VALUES (?, ?)
        """, (cliente_id, moto))
        print("Moto vinculada ao cliente.")
        break
    
def cadastrar_manutencao(cursor):
    while True:
        if not tabela_moto(cursor):
            return
        try:
            moto_id = input("Qual o ID da moto? ").strip()
            if moto_id == "sair":
                return "sair"
            else:
                moto_id = int(moto_id)
        except ValueError:
            print("Digite apenas números.")
            continue
        cursor.execute("""
        SELECT id FROM motos
        WHERE id = ?
        """, (moto_id,))
        moto_encontrada = cursor.fetchone()
        if moto_encontrada is None:
            print("Moto não encontrada.")
            continue
        manutencao = pedir_manutencao()
        if manutencao == "sair":
            return "sair"
        data = pedir_data()
        if data == "sair":
            return "sair"
        data = data.isoformat()
        cursor.execute("""
        INSERT INTO manutencoes (moto_id, servico, data)
        VALUES (?, ?, ?)
        """, (moto_id, manutencao, data))
        break



def buscar_dados(cursor):
    opcao = {
        "1": "clientes.nome",
        "2": "clientes.telefone",
        "3": "motos.modelo",
        "4": "manutencoes.servico",
        "5": "manutencoes.data",
        "6": "clientes.id"
    }
    while True:
        escolha = input("""
1-Nome
2-Telefone
3-Moto
4-Serviço
5-Data
6-ID do cliente

Qual informação deseja buscar? """).strip().lower()
        if escolha == "sair":
            return "sair"
        if escolha not in opcao:
            print("Opção inválida.")
            continue
        coluna = opcao[escolha]
        if escolha in ("1", "2", "3", "4"):
            busca = input("O que deseja buscar? ").strip()
            if busca.lower() == "sair":
                return "sair"
            if not busca:
                print("Preencha este campo.")
                continue
            busca = f"%{busca}%"
            cursor.execute(f"""
            SELECT clientes.nome,
                   clientes.telefone,
                   motos.modelo,
                   manutencoes.servico,
                   manutencoes.data
            FROM clientes
            LEFT JOIN motos
            ON clientes.id = motos.cliente_id
            LEFT JOIN manutencoes
            ON motos.id = manutencoes.moto_id
            WHERE {coluna} LIKE ?
            ORDER BY manutencoes.data DESC
            """, (busca,))
        elif escolha == "5":
            busca = pedir_data()
            if busca == "sair":
                return "sair"
            busca = busca.isoformat()
            cursor.execute("""
            SELECT clientes.nome,
                clientes.telefone,
                motos.modelo,
                manutencoes.servico,
                manutencoes.data
            FROM clientes
            LEFT JOIN motos
            ON clientes.id = motos.cliente_id
            LEFT JOIN manutencoes
            ON motos.id = manutencoes.moto_id
            WHERE manutencoes.data = ?
            ORDER BY manutencoes.data DESC
            """, (busca,))
        elif escolha == "6":
            busca = input_inteiro()
            if busca == "sair":
                return "sair"
            cursor.execute("""
            SELECT clientes.nome,
                clientes.telefone,
                motos.modelo,
                manutencoes.servico,
                manutencoes.data
            FROM clientes
            LEFT JOIN motos
            ON clientes.id = motos.cliente_id
            LEFT JOIN manutencoes
            ON motos.id = manutencoes.moto_id
            WHERE clientes.id = ?
            ORDER BY manutencoes.data DESC
            """, (busca,))
        resultado = cursor.fetchall()
        if not resultado:
            print("Nenhum resultado encontrado.")
            return
        print(
f"| {'CLIENTE': <20} |",
f"| {'TELEFONE': <20} |",
f"| {'MOTO': <20} |",
f"| {'SERVIÇO': <20} |",
f"| {'DATA': <20} |"
)
        print("=" * 124)
        for registro in resultado:
            telefone = registro[1] if registro[1] is not None else ""
            moto = registro[2] if registro[2] is not None else ""
            servico = registro[3] if registro[3] is not None else ""
            data = padronizar_data(registro[4]) if registro[4] is not None else ""
            print(
                f"| {registro[0]: <20} |",
                f"| {telefone: <20} |",
                f"| {moto: <20} |",
                f"| {servico: <20} |",
                f"| {data: <20} |"
            )
        return

def ver_historico(cursor):
    while True:
        if not tabela_cliente(cursor):
            return
        opcao = input("Digite um ID ou 'todos'. ").lower().strip()
        if opcao == "sair":
            return "sair"
        elif opcao == "todos":
            cursor.execute("""
            SELECT clientes.nome,
                motos.modelo,
                manutencoes.servico,
                manutencoes.data
            FROM manutencoes
            JOIN motos
            ON manutencoes.moto_id = motos.id
            JOIN clientes
            ON motos.cliente_id = clientes.id
            ORDER BY manutencoes.data DESC
            """)  
            visualizar = cursor.fetchall()
            if not visualizar:
                print("Nenhum histórico encontrado.")
                return
            print(f"| {'NOME': <20} |", f"| {'MOTO': <20} |",f"| {'MANUTENÇÃO': <20} |", f"| {'DATA': <20} |")
            print ("=" * 99)
            for cliente in visualizar:
                print(f"| {cliente[0]: <20} |", f"| {cliente[1]: <20} |",f"| {cliente[2]: <20} |", f"| {cliente[3]: <20} |")
            break
        else:    
            try:
                cliente_id = int(opcao)
            except ValueError:
                print("Digite um ID válido ou 'todos'.")   
                continue
            cursor.execute("""
            SELECT clientes.nome,
                motos.modelo,
                manutencoes.servico,
                manutencoes.data
            FROM manutencoes
            JOIN motos
            ON manutencoes.moto_id = motos.id
            JOIN clientes
            ON motos.cliente_id = clientes.id
            WHERE clientes.id = ?
            ORDER BY manutencoes.data DESC
            """, (cliente_id,))  
            visualizar = cursor.fetchall()
            if not visualizar:
                print("Nenhum histórico encontrado.")
                return
            print(f"| {'NOME': <20} |", f"| {'MOTO': <20} |",f"| {'MANUTENÇÃO': <20} |", f"| {'DATA': <20} |")
            print ("=" * 99)
            for registro in visualizar:
                print(f"| {registro[0]: <20} |", f"| {registro[1]: <20} |",f"| {registro[2]: <20} |", f"| {registro[3]: <20} |")
            break
   
#FUNÇÕES DE MUDAR DADOS#########################################################################################################################
        
def mudar_cliente(cursor):
    opcao = {
    "1": ("nome", pedir_nome),
    "2": ("telefone", pedir_telefone)
    }
    while True:
        if not tabela_cliente(cursor):
            return
        while True:
            id_cliente = input_inteiro()
            if id_cliente == "sair":
                    return "sair"
            cursor.execute("""
                SELECT * FROM clientes
                WHERE id = ?
                """, (id_cliente,))
            cliente = cursor.fetchone()
            if cliente is None:
                print("ID não encontrado.")
                continue
            break
        while True:
            qual_coluna = input("""
1-Nome
2-Telefone

Qual informação quer mudar? """).strip()
            if qual_coluna.lower() == "sair":
                return "sair"
            if qual_coluna in opcao:
                coluna, funcao = opcao[qual_coluna]
                break
            else:
                print("Insira um valor válido.")
        novo_valor = funcao()
        if novo_valor == "sair":
            return "sair"
        cursor.execute(f"""
            UPDATE clientes
            SET {coluna} = ?
            WHERE id = ?
            """, (novo_valor, id_cliente))
        if cursor.rowcount > 0:
            print("Dados alterados.")
        return
def mudar_moto(cursor):
    while True:
        if not tabela_moto(cursor):
            return
        while True:
            moto_id = input_inteiro()
            if moto_id == "sair":
                    return "sair"
            cursor.execute("""
                SELECT * FROM motos
                WHERE id = ?
                """, (moto_id,))
            moto_saida = cursor.fetchone()
            if moto_saida is None:
                print("Moto não encontrada.")
                continue
            break
        novo_valor = pedir_moto()
        if novo_valor == "sair":
            return "sair"
        cursor.execute("""
            UPDATE motos
            SET modelo = ?
            WHERE id = ?
            """, (novo_valor, moto_id))
        if cursor.rowcount > 0:
            print("Dados alterados.")
        return
def mudar_manutencao(cursor):
    opcao = {
    "1": ("servico", pedir_manutencao),
    "2": ("data", pedir_data)
    }
    if not tabela_manutencao(cursor):
        return
    while True:
        manutencao_id = input_inteiro()
        if manutencao_id == "sair":
            return "sair"
        cursor.execute("""
        SELECT id FROM manutencoes
        WHERE id = ?               
        """, (manutencao_id,))
        manutencao_encontrada = cursor.fetchone()
        if manutencao_encontrada is None:
            print("Manutenção não encontrada.")
            continue
        while True:
            qual_coluna = input("""
1-Serviço
2-Data

Quer alterar qual informação dessa manutenção? """)
            if qual_coluna == "sair":
                return "sair"
            if qual_coluna not in opcao:
                print("Opção inválida.")
                continue
            coluna, funcao = opcao[qual_coluna]
            novo_valor = funcao()
            if novo_valor == "sair":
                return "sair"
            if coluna == "data":
                novo_valor = novo_valor.isoformat()
            cursor.execute(f"""
            UPDATE manutencoes
            SET {coluna} = ?
            WHERE id = ?
            """, (novo_valor, manutencao_id))
            if cursor.rowcount > 0:
                print("Dados alterados.")
            return

#FUNÇÕES DE DELETAR DADOS#######################################################################################################################

def deletar_cliente(cursor):
    while True:
        if not tabela_cliente(cursor):
            return
        cliente_id = input_inteiro()
        if cliente_id == "sair":
            return "sair"
        try:
            cursor.execute("""
            DELETE FROM clientes
            WHERE id = ?
            """, (cliente_id,))
        except sq.IntegrityError:
            print("Existem motos vinculadas a esse cliente.")
            continue
        if cursor.rowcount == 0:
            print("Cliente não encontrado")
            continue
        print("Cliente deletado.")
        return         
def deletar_moto(cursor):
    while True:
        if not tabela_moto(cursor):
            return
        moto_id = input_inteiro()
        if moto_id == "sair":
            return "sair"
        try:
            cursor.execute("""
            DELETE FROM motos
            WHERE id = ?
            """, (moto_id,))
        except sq.IntegrityError:
            print("Existem manutenções vinculadas a essa moto.")
            continue
        if cursor.rowcount == 0:
            print("Moto não encontrada")
            continue
        print("Moto deletada.")
        return         
def deletar_manutencao(cursor):
    while True:
        if not tabela_manutencao(cursor):
            return
        manutencao_id = input_inteiro()
        if manutencao_id == "sair":
            return "sair"
        cursor.execute("""
        DELETE FROM manutencoes
        WHERE id = ?               
        """, (manutencao_id,))
        if cursor.rowcount == 0:
            print("Manutenção não encontrada.")
            continue
        print("Manutenção deletada.")
        return
        

#####################################
#FUNÇÕES QUE UNIFICAM OUTRAS MENORES############################################################################################################
#####################################
 
def cadastro(cursor): #cadastrar novos clientes.
    opcao = {
    "1": cadastrar_cliente,
    "2": cadastrar_moto,
    "3": cadastrar_manutencao
    }  
    while True:
        escolha = input("""
1-Cliente
2-Moto
3-Manutencao

Quer cadastrar o que? """).lower().strip()  
        if escolha == "sair":
            return "sair"
        elif escolha in opcao:
            opcao[escolha](cursor)
            break
        else:
            print("Insira um número válido.")

def alterar_dados(cursor): #Alterar algum dado da database.
    opcao = {
    "1": mudar_cliente,
    "2": mudar_moto,
    "3": mudar_manutencao
    }  
    while True:
        mudanca = input("""
1-Cliente
2-Moto
3-Manutencao

Qual dado quer alterar? """).lower().strip()  
        if mudanca == "sair":
            return "sair"
        elif mudanca in opcao:
            resultado = opcao[mudanca](cursor)
            if resultado == "sair":
                return "sair"
            break
        else:
            print("Insira um número válido.")
            
def deletar_dados(cursor): #Deletar algum dado da database.
    opcao = {
    "1": deletar_cliente,
    "2": deletar_moto,
    "3": deletar_manutencao
    }  
    while True:
        escolha = input("""
1-Cliente
2-Moto
3-Manutencao

Quer deletar o que? """).lower().strip()  
        if escolha == "sair":
            return "sair"
        elif escolha in opcao:
            opcao[escolha](cursor)
            break
        else:
            print("Insira um número válido.")

def pesquisar(cursor):
    while True:
        escolha = input("""
1-Buscar dados
2-Ver histórico

O que deseja pesquisar? """).strip().lower()

        if escolha == "sair":
            return "sair"

        elif escolha == "1":
            resultado = buscar_dados(cursor)

        elif escolha == "2":
            resultado = ver_historico(cursor)

        else:
            print("Opção inválida.")
            continue

        if resultado == "sair":
            return "sair"

        break