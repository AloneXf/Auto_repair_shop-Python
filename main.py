import sqlite3
from database import (criar_tabela, input_dados, ver_dados, mudar_dados, deletar_dados, pesquisa_coluna)
conexao = sqlite3.connect("oficina.db")
cursor = conexao.cursor()

criar_tabela(cursor) #Garante que a tabela exista.
conexao.commit()

try:
    while True:
        opcao = input("""
    1-Inserir
    2-Ver
    3-Mudar
    4-Deletar
    5-Sair
    6-Pesquisar

    O que deseja fazer? """).strip()                                                                                          
        selecao_opcao = {
        "1": input_dados,
        "2": ver_dados,
        "3": mudar_dados,
        "4": deletar_dados,
        "6": pesquisa_coluna}
        if opcao == "5":
            break
        elif opcao in selecao_opcao:
            resultado = selecao_opcao[opcao](cursor)
            if resultado == "sair":
                break
            conexao.commit()
        else:
            print("Insira apenas números válidos.")
finally:
    conexao.commit()
    conexao.close()