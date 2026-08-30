import sqlite3 as sq
import core
import terminal

def main():
    conexao = sq.connect("oficina.db")
    cursor = conexao.cursor()
    try:
        core.criar_tabelas(cursor)
        conexao.commit()
        opcoes = {
            "1": terminal.cadastro,
            "2": terminal.alterar_dados,
            "3": terminal.deletar_dados,
            "4": terminal.pesquisar,
            "5": terminal.resumo
        }
        while True:
            print()
            escolha = input("1-Cadastrar\n2-Alterar\n3-Excluir\n4-Pesquisar\n5-Resumo\n0-Sair\nO que deseja fazer?").strip().lower()
            if escolha in ("0", "sair"):
                break
            if escolha not in opcoes:
                print("Opção inválida.")
                continue
            try:
                resultado = opcoes[escolha](cursor)
                if resultado == "sair":
                    conexao.rollback()
                    break
                if escolha in ("1", "2", "3"):
                    conexao.commit()
            except sq.Error as erro:
                conexao.rollback()
                print (f"Erro no banco de dados: {erro}")
    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    main()