import sqlite3
from database import (criar_tabelas, cadastro, alterar_dados, deletar_dados, pesquisar)

def main():
    conexao = sqlite3.connect("oficina.db")
    cursor = conexao.cursor()

    criar_tabelas(cursor) #Garante que a tabela exista.
    conexao.commit()

    selecao_opcao = {
    "1": cadastro,
    "2": alterar_dados,
    "3": deletar_dados,
    "4": pesquisar

    }
    
    try:
        while True:
            opcao = input("""
0-Fechar programa
1-Cadastrar
2-Alterar
3-Deletar
4-Consultar

O que deseja fazer? """).strip()                                                                                          
            if opcao == "0":
                break
            elif opcao in selecao_opcao:
                resultado = selecao_opcao[opcao](cursor)
                if resultado == "sair":
                    break
                conexao.commit()
            else:
                print("Insira apenas números válidos.")
    finally:
        conexao.close()
if __name__ == "__main__":
    main()