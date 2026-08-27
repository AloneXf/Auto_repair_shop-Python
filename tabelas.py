from validacoes import padronizar_data

def tabela_cliente(cursor):
    cursor.execute("""
    SELECT * FROM clientes""")
    visualizar = cursor.fetchall()
    if not visualizar:
        print("Não tem clientes cadastrados.")
        return False
    print(f"| {'ID': <20} |", f"| {'NOME': <20} |",f"| {'TELEFONE': <20} |")
    print ("=" * 74)
    for cliente in visualizar:
        telefone = cliente[2] if cliente[2] is not None else ""
        print(f"| {cliente[0]: <20} |", f"| {cliente[1]: <20} |",f"| {telefone: <20} |")
    return True

def tabela_moto(cursor):
    cursor.execute("""
    SELECT motos.id, clientes.nome, motos.modelo
    FROM motos
    JOIN clientes
    ON motos.cliente_id = clientes.id
    """)
    visualizar = cursor.fetchall()
    if not visualizar:
        print("Não há motos cadastradas.")
        return False
    print(f"| {'ID MOTO': <20} |", f"| {'CLIENTE': <20} |",f"| {'MOTO': <20} |")
    print ("=" * 74)
    for moto in visualizar:                 
        print(f"| {moto[0]: <20} |", f"| {moto[1]: <20} |",f"| {moto[2]: <20} |")
    return True

def tabela_manutencao(cursor):
    cursor.execute("""
    SELECT manutencoes.id,
    clientes.nome,
    motos.modelo,
    manutencoes.servico,
    manutencoes.data
    FROM manutencoes
    JOIN motos
    ON manutencoes.moto_id = motos.id
    JOIN clientes
    ON motos.cliente_id = clientes.id
    """)
    visualizar = cursor.fetchall()
    if not visualizar:
        print("Não há manutenções cadastradas.")
        return False
    print(f"| {'ID MANUTENÇÃO': <20} |", f"| {'CLIENTE': <20} |",f"| {'MOTO': <20} |", f"| {'SERVIÇO': <20} |", f"| {'DATA': <20} |")
    print ("=" * 124)
    for manutencao in visualizar: 
        data = padronizar_data(manutencao[4])                
        print(f"| {manutencao[0]: <20} |", f"| {manutencao[1]: <20} |",f"| {manutencao[2]: <20} |", f"| {manutencao[3]: <20} |",f"| {data: <20} |")
    return True