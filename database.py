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

#Funções base da DataBase:

def criar_tabela(cursor): #Verifica se a tabela existe e cria ela automaticamente ao rodar o código.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        telefone TEXT,
        moto TEXT NOT NULL,
        manutencao TEXT NOT NULL,
        data TEXT NOT NULL
    )
    """)

def deletar_dados(cursor): #Deletar os dados de um cliente especifico.
    delete = input_inteiro()
    if delete == "sair":
        return "sair"
    cursor.execute("""
    DELETE FROM clientes
    WHERE id = ?
    """,(delete,))
    if cursor.rowcount > 0:
        print("Dados deletados. ")
    else:
        print("ID não encontrado.")
        
def input_dados(cursor): #Adicionar novo cliente no banco de dados.
    nome = pedir_nome()
    if nome == "sair":
        return "sair"
    telefone = pedir_telefone()
    if telefone == "sair":
        return "sair"
    moto = pedir_moto()
    if moto == "sair":
        return "sair"
    manutencao = pedir_manutencao()
    if manutencao == "sair":
        return "sair"
    data = pedir_data()
    if data == "sair":
        return "sair"
    data = data.isoformat()
    cursor.execute("""
    INSERT INTO clientes (nome, telefone, moto, manutencao, data)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, telefone, moto, manutencao, data))
    print("Dados salvos. ")

def ver_dados(cursor): #Visualizar a tabela toda ou apenas um cliente.
    while True:
        id_cliente = input("Qual ID quer ver? ").lower().strip()
        if id_cliente == "sair":
            return "sair"
        elif id_cliente == "todos":
            cursor.execute("""
            SELECT * FROM clientes
            """)
            break
        elif id_cliente.isdigit():
            id_cliente = int(id_cliente)
            cursor.execute("""
            SELECT * FROM clientes
            WHERE id = ?
            """,(id_cliente,))
            break
        else:
            print("Digite um ID válido ou 'todos'")
    visualizar = cursor.fetchall()
    if not visualizar:
        print("Cliente não encontrado.")
        return  
    print(f"| {'ID': <20} |", f"| {'NOME': <20} |",f"| {'TELEFONE': <20} |", f"| {'MOTO': <20} |", f"| {'MANUTENÇÃO': <20} |", f"| {'DATA': <20} |")
    print ("=" * 149)
    for cliente in visualizar:
        telefone = cliente[2] if cliente[2] is not None else ""
        data_formatada = padronizar_data(cliente[5])
        print(f"| {cliente[0]: <20} |", f"| {cliente[1]: <20} |",f"| {telefone: <20} |", f"| {cliente[3]: <20} |", f"| {cliente[4]: <20} |", f"| {data_formatada: <20} |")

def mudar_dados(cursor): #Altera dados especificos de clientes.
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
    opcao = {
    "1": ("nome", pedir_nome),
    "2": ("telefone", pedir_telefone),
    "3": ("moto", pedir_moto),
    "4": ("manutencao", pedir_manutencao),
    "5": ("data", pedir_data)
    }
    while True:
        qual_coluna = input("""
1-Nome
2-Telefone
3-Moto
4-Manutenção
5- Data

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
    if coluna == "data":
        novo_valor = novo_valor.isoformat()
    cursor.execute(f"""
    UPDATE clientes
    SET {coluna} = ?
    WHERE id = ?
    """, (novo_valor, id_cliente))
    if cursor.rowcount > 0:
        print("Dados atualizados.")
    
def pesquisa_coluna(cursor): #Pesquisa uma coluna individualmente e mostra todos os elementos dentro dela.
    colunas_validas = {
    "1": "nome",
    "2": "telefone",
    "3": "moto",
    "4": "manutencao",
    "5": "data"
    }
    while True:
        selecao_dado = input("""
1-Nome
2-Telefone
3-Moto
4-Manutenção
5-Data

Qual coluna quer ver? """).lower().strip()
        if selecao_dado == "sair":
            return "sair"
        elif selecao_dado in colunas_validas:
            coluna = colunas_validas[selecao_dado]
            cursor.execute(f"""
                SELECT {coluna} FROM clientes
                """)
            break
        else:
            print("Digite uma coluna válida.")
    visualizar = cursor.fetchall()
    if not visualizar:
        print("Coluna não encontrada.")
        return  
    for dado in visualizar:
        valor = dado[0]
        if valor is None:
            valor = ""
        if coluna == "data":
            valor = padronizar_data(valor)
        print(valor)