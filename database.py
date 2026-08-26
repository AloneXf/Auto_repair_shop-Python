from validacoes import (pedir_nome, pedir_telefone, pedir_moto, pedir_manutencao, pedir_data, padronizar_data, input_inteiro)

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
        
def input_dados(cursor): #Adicionar novo cliente ao banco de dados.
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

def buscar_dados(cursor): #Realiza personalizadas na database.
    opcao = {
    "1": "nome",
    "2": "telefone",
    "3": "moto",
    "4": "manutencao",
    "5": "data",
    "6": "id" 
    }
    while True:
        qual_coluna = input("""
1-Nome
2-Telefone
3-Moto
4-Manutenção
5-Data
6-ID

Qual informação quer buscar? """).strip().lower()
        if qual_coluna == "sair":
            return "sair"
        if qual_coluna not in opcao:
            print("Opção inválida.")
            continue
        coluna = opcao[qual_coluna]
        while True:
            if coluna == "id":
                busca = input("Qual buscar? ").strip().lower()
                if busca == "sair":
                    return "sair" 
                if not busca:
                    print("Preencha este campo.")
                    continue
                try:
                    cursor.execute("""
                    SELECT * FROM clientes
                    WHERE id = ?
                    """, (int(busca),))
                    visualizar = cursor.fetchall()
                    break
                except ValueError:
                    print("Digite um ID válido.")
            elif coluna == "data":
                busca = pedir_data()
                if busca == "sair":
                    return "sair"
                busca = busca.isoformat()
                cursor.execute("""
                SELECT * FROM clientes
                WHERE data = ?
                """, (busca,)) 
                visualizar = cursor.fetchall()
                break
            else:
                busca = input("Qual buscar? ").strip().lower()
                if busca == "sair":
                    return "sair" 
                if not busca:
                    print("Preencha este campo.")
                    continue
                busca = f"%{busca}%"
                cursor.execute(f"""
                SELECT * FROM clientes
                WHERE {coluna} like ?           
                """, (busca,))
                visualizar = cursor.fetchall()
                break
        if not visualizar:
            print("Nenhum resultado encontrado.")
            return
        print(f"| {'ID': <20} |", f"| {'NOME': <20} |",f"| {'TELEFONE': <20} |", f"| {'MOTO': <20} |", f"| {'MANUTENÇÃO': <20} |", f"| {'DATA': <20} |")
        print ("=" * 149)
        for cliente in visualizar:
            telefone = cliente[2] if cliente[2] is not None else ""
            data_formatada = padronizar_data(cliente[5])
            print(f"| {cliente[0]: <20} |",f"| {cliente[1]: <20} |",f"| {telefone: <20} |", f"| {cliente[3]: <20} |", f"| {cliente[4]: <20} |", f"| {data_formatada: <20} |")
        return