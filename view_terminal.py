from datetime import datetime

def exibir_tabela(cabecalhos, registros):
    if not registros:
        print("Nenhum registro encontrado.")
        return False
    linhas = []
    for registro in registros:
        linha = []
        for valor in registro:
            texto = "" if valor is None else str(valor)
            linha.append(texto)
        linhas.append(linha)
    larguras = []
    for indice, cabecalho in enumerate(cabecalhos):
        maior = len(str(cabecalho))
        for linha in linhas:
            if len(linha[indice]) > maior:
                maior = len(linha[indice])
        larguras.append(maior)
    borda = "+"
    for largura in larguras:
        borda += "-" * (largura + 2) + "+"
    print()
    print(borda)
    linha_cabecalho = "|"
    for indice, cabecalho in enumerate(cabecalhos):
        linha_cabecalho += f" {cabecalho:<{larguras[indice]}} |"
    print(linha_cabecalho)
    print(borda)
    for linha in linhas:
        linha_registro = "|"
        for indice, valor in enumerate(linha):
            linha_registro += f" {valor:<{larguras[indice]}} |"
        print(linha_registro)
    print(borda)
    return True

def tabela_clientes(registros):
    cabecalhos = ("ID", "NOME", "TELEFONE")
    return exibir_tabela(cabecalhos, registros)
def tabela_motos(registros):
    cabecalhos = ("ID", "CLIENTE", "MOTO", "PLACA", "ANO")
    return exibir_tabela(cabecalhos, registros)

def formatar_data(data):
    if data is None:
        return ""
    return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
def formatar_valor(valor_centavos):
    if valor_centavos is None:
        return ""
    valor = valor_centavos / 100
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def tabela_manutencoes(registros):
    registros_formatados = []
    for registro in registros:
        linha = list(registro)

        linha[4] = formatar_data(linha[4])
        linha[6] = formatar_valor(linha[6])
        registros_formatados.append(linha)
    cabecalhos = (
        "ID",
        "CLIENTE",
        "MOTO",
        "SERVIÇO",
        "DATA",
        "QUILOMETRAGEM",
        "VALOR",
        "STATUS")
    return exibir_tabela(cabecalhos, registros_formatados)

def tabela_registros(registros):
    registros_formatados = []
    for registro in registros:
        linha = list(registro)
        linha[9] = formatar_data(linha[9])
        linha[11] = formatar_valor(linha[11])
        registros_formatados.append(linha)
    cabecalhos = (
        "ID CLIENTE",
        "CLIENTE",
        "TELEFONE",
        "ID MOTO",
        "MOTO",
        "PLACA",
        "ANO",
        "ID MANUTENÇÃO",
        "SERVIÇO",
        "DATA",
        "QUILOMETRAGEM",
        "VALOR",
        "STATUS",
        "OBSERVAÇÕES")
    return exibir_tabela(cabecalhos, registros_formatados)

def exibir_resumo(resumo):
    print()
    print("=== RESUMO DA OFICINA ===")
    print(f"Manutenções registradas: {resumo['total']}")
    print(f"Pendentes: {resumo['pendentes']}")
    print(f"Em andamento: {resumo['em_andamento']}")
    print(f"Concluídas: {resumo['concluidas']}")
    print(f"Canceladas: {resumo['canceladas']}")
    print(f"Valor total registrado: {formatar_valor(resumo['valor_total'])}")
    print(f"Valor das concluídas: {formatar_valor(resumo['valor_concluido'])}")