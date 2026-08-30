import core
import validations
import sqlite3 as sq
from view_terminal import (
    tabela_clientes, tabela_motos, tabela_manutencoes, tabela_registros, exibir_resumo)

def pedir_valor(mensagem, validador):
    print()
    while True:
        valor = input(mensagem)
        if valor.strip().lower() == "sair":
            return "sair"
        try:
            return validador(valor)
        except ValueError as erro:
            print(f"Erro: {erro}")
def pedir_id_existente(cursor, mensagem, funcao_existe, mensagem_nao_encontrado):
    print()
    while True:
        id_registro = pedir_valor(mensagem, validations.validar_id)
        if id_registro == "sair":
            return "sair"
        if not funcao_existe(cursor, id_registro):
            print(mensagem_nao_encontrado)
            continue
        return id_registro
def pedir_opcao(mensagem, opcoes):
    print()
    while True:
        escolha = input(mensagem).strip().lower()
        if escolha == "sair":
            return "sair"
        if escolha in opcoes:
            return opcoes[escolha]
        print("Opção inválida.")
def pedir_confirmacao(mensagem):
    print()
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == "sair":
            return "sair"
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Digite 'sim' ou 'não'.")
def executar_menu(cursor, mensagem, opcoes):
    print()
    while True:
        escolha = input(mensagem).strip().lower()
        if escolha == "sair":
            return "sair"
        if escolha not in opcoes:
            print("Opção inválida.")
            continue
        resultado = opcoes[escolha](cursor)
        if resultado == "sair":
            return "sair"
        return
            
            
def cadastrar_cliente(cursor):
    nome = pedir_valor("Digite o nome do cliente: ", validations.validar_nome)
    if nome == "sair":
        return "sair"
    telefone = pedir_valor("Contato do cliente: ", validations.validar_telefone)
    if telefone == "sair":
        return "sair"
    cliente_id = core.inserir_cliente(cursor, nome, telefone)
    print(f"Cliente cadastrado. ID: {cliente_id}")
def alterar_cliente(cursor):
    clientes = core.listar_clientes(cursor)
    if not tabela_clientes(clientes):
        return
    cliente_id = pedir_id_existente(cursor, "ID do cliente: ", core.cliente_existe, "Cliente não encontrado.")
    if cliente_id == "sair":
        return "sair"
    opcoes = {
        "1": ("nome", validations.validar_nome, "Novo nome: "),
        "2": ("telefone", validations.validar_telefone, "Novo telefone (vazio para remover): ")
    }
    escolha = pedir_opcao("1-Nome\n2-Telefone\nQual informação deseja alterar? ", opcoes)
    if escolha == "sair":
        return "sair"
    coluna, validador, mensagem = escolha
    novo_valor = pedir_valor(mensagem, validador)
    if novo_valor == "sair":
        return "sair"
    if not core.alterar_cliente(cursor, cliente_id, coluna, novo_valor):
        print("Cliente não encontrado.")
        return
    print("Cliente alterado.")
def deletar_cliente(cursor):
    clientes = core.listar_clientes(cursor)
    if not tabela_clientes(clientes):
        return
    cliente_id = pedir_id_existente(cursor, "ID do cliente: ", core.cliente_existe, "Cliente não encontrado.")
    if cliente_id == "sair":
        return "sair"
    confirmacao = pedir_confirmacao("Tem certeza que deseja excluir este cliente? (sim/não): ")
    if confirmacao == "sair":
        return "sair"
    if not confirmacao:
        print("Exclusão cancelada.")
        return
    try:
        deletado = core.deletar_cliente(cursor, cliente_id)
    except sq.IntegrityError:
        print("Não é possível excluir o cliente porque existem motos vinculadas a ele.")
        return
    if not deletado:
        print("Cliente não encontrado.")
        return
    print("Cliente excluído.")
    
def cadastrar_moto(cursor):
    clientes = core.listar_clientes(cursor)
    if not tabela_clientes(clientes):
        return
    cliente_id = pedir_id_existente(cursor, "Qual o ID do cliente? ", core.cliente_existe, "Cliente não encontrado.")
    if cliente_id == "sair":
        return "sair"
    moto = pedir_valor("Modelo da moto: ", validations.validar_moto)
    if moto == "sair":
        return "sair"
    ano = pedir_valor("Ano da moto (opcional): ", validations.validar_ano)
    if ano == "sair":
        return "sair"
    while True:
        placa = pedir_valor("Placa da moto (opcional): ", validations.validar_placa)
        if placa == "sair":
            return "sair"
        try:
            moto_id = core.inserir_moto(cursor, cliente_id, moto, placa, ano)
        except sq.IntegrityError as erro:
            if "UNIQUE constraint failed: motos.placa" in str(erro):
                print("Já existe uma moto cadastrada com essa placa.")
                continue
            raise
        if moto_id is None:
            print("Cliente não encontrado.")
            return
        print(f"Moto cadastrada. ID: {moto_id}")
        return
def alterar_moto(cursor):
    motos = core.listar_motos(cursor)
    if not tabela_motos(motos):
        return
    moto_id = pedir_id_existente(cursor, "ID da moto: ", core.moto_existe, "Moto não encontrada.")
    if moto_id == "sair":
        return "sair"
    opcoes = {
        "1": ("modelo", validations.validar_moto, "Novo modelo: "),
        "2": ("placa", validations.validar_placa, "Nova placa (vazio para remover): "),
        "3": ("ano", validations.validar_ano, "Novo ano (vazio para remover): ")
    }
    escolha = pedir_opcao("1-Modelo\n2-Placa\n3-Ano\nQual informação deseja alterar? ", opcoes)
    if escolha == "sair":
        return "sair"
    coluna, validador, mensagem = escolha
    while True:
        novo_valor = pedir_valor(mensagem, validador)
        if novo_valor == "sair":
            return "sair"
        try:
            alterado = core.alterar_moto(cursor, moto_id, coluna, novo_valor)
        except sq.IntegrityError as erro:
            if coluna == "placa" and "UNIQUE constraint failed: motos.placa" in str(erro):
                print("Já existe uma moto cadastrada com essa placa.")
                continue
            raise
        if not alterado:
            print("Moto não encontrada.")
            return
        print("Moto alterada.")
        return
def deletar_moto(cursor):
    motos = core.listar_motos(cursor)
    if not tabela_motos(motos):
        return
    moto_id = pedir_id_existente(cursor, "ID da moto: ", core.moto_existe, "Moto não encontrada.")
    if moto_id == "sair":
        return "sair"
    confirmacao = pedir_confirmacao("Tem certeza que deseja excluir esta moto? (sim/não): ")
    if confirmacao == "sair":
        return "sair"
    if not confirmacao:
        print("Exclusão cancelada.")
        return
    try:
        deletado = core.deletar_moto(cursor, moto_id)
    except sq.IntegrityError:
        print("Não é possível excluir a moto porque existem manutenções vinculadas a ela.")
        return
    if not deletado:
        print("Moto não encontrada.")
        return
    print("Moto excluída.")

def cadastrar_manutencao(cursor):
    motos = core.listar_motos(cursor)
    if not tabela_motos(motos):
        return
    moto_id = pedir_id_existente(cursor, "Qual o ID da moto? ", core.moto_existe, "Moto não encontrada.")
    if moto_id == "sair":
        return "sair"
    servico = pedir_valor("Serviço realizado: ", validations.validar_manutencao)
    if servico == "sair":
        return "sair"
    data = pedir_valor("Data da manutenção (DD/MM/AAAA): ", validations.validar_data_obrigatoria)
    if data == "sair":
        return "sair"
    quilometragem = pedir_valor("Quilometragem (opcional): ", validations.validar_quilometragem)
    if quilometragem == "sair":
        return "sair"
    valor_centavos = pedir_valor("Valor em reais (opcional): R$ ", validations.validar_valor_reais)
    if valor_centavos == "sair":
        return "sair"
    status = pedir_valor("Status (Pendente/Em andamento/Concluída/Cancelada, opcional): ", validations.validar_status)
    if status == "sair":
        return "sair"
    observacoes = pedir_valor("Observações (opcional): ", validations.validar_observacao)
    if observacoes == "sair":
        return "sair"
    manutencao_id = core.inserir_manutencao(cursor, moto_id, servico, data, quilometragem, valor_centavos, status, observacoes)
    if manutencao_id is None:
        print("Moto não encontrada.")
        return
    print(f"Manutenção cadastrada. ID: {manutencao_id}")
def alterar_manutencao(cursor):
    manutencoes = core.listar_manutencoes(cursor)
    if not tabela_manutencoes(manutencoes):
        return
    manutencao_id = pedir_id_existente(cursor, "ID da manutenção: ", core.manutencao_existe, "Manutenção não encontrada.")
    if manutencao_id == "sair":
        return "sair"
    opcoes = {
        "1": ("servico", validations.validar_manutencao, "Novo serviço: "),
        "2": ("data", validations.validar_data_obrigatoria, "Nova data (DD/MM/AAAA): "),
        "3": ("quilometragem", validations.validar_quilometragem, "Nova quilometragem (vazio para remover): "),
        "4": ("valor_centavos", validations.validar_valor_reais, "Novo valor em reais (vazio para remover): R$ "),
        "5": ("status", validations.validar_status, "Novo status (vazio para remover): "),
        "6": ("observacoes", validations.validar_observacao, "Nova observação (vazio para remover): ")
    }
    escolha = pedir_opcao("1-Serviço\n2-Data\n3-Quilometragem\n4-Valor\n5-Status\n6-Observações\nQual informação deseja alterar? ", opcoes)
    if escolha == "sair":
        return "sair"
    coluna, validador, mensagem = escolha
    novo_valor = pedir_valor(mensagem, validador)
    if novo_valor == "sair":
        return "sair"
    if not core.alterar_manutencao(cursor, manutencao_id, coluna, novo_valor):
        print("Manutenção não encontrada.")
        return
    print("Manutenção alterada.")
def deletar_manutencao(cursor):
    manutencoes = core.listar_manutencoes(cursor)
    if not tabela_manutencoes(manutencoes):
        return
    manutencao_id = pedir_id_existente(cursor, "ID da manutenção: ", core.manutencao_existe, "Manutenção não encontrada.")
    if manutencao_id == "sair":
        return "sair"
    confirmacao = pedir_confirmacao("Tem certeza que deseja excluir esta manutenção? (sim/não): ")
    if confirmacao == "sair":
        return "sair"
    if not confirmacao:
        print("Exclusão cancelada.")
        return
    if not core.deletar_manutencao(cursor, manutencao_id):
        print("Manutenção não encontrada.")
        return
    print("Manutenção excluída.")
    
def pesquisar_registros(cursor):
    filtros = {}
    opcoes = {
        "1": ("nome", "Nome do cliente: ", validations.validar_texto_busca),
        "2": ("telefone", "Telefone: ", validations.validar_texto_busca),
        "3": ("moto", "Modelo da moto: ", validations.validar_texto_busca),
        "4": ("placa", "Placa: ", validations.validar_texto_busca),
        "5": ("ano", "Ano: ", validations.validar_ano),
        "6": ("servico", "Serviço: ", validations.validar_texto_busca),
        "7": ("status", "Status: ", validations.validar_status),
        "8": ("observacoes", "Observação: ", validations.validar_texto_busca),
        "9": ("cliente_id", "ID do cliente: ", validations.validar_id),
        "10": ("moto_id", "ID da moto: ", validations.validar_id),
        "11": ("manutencao_id", "ID da manutenção: ", validations.validar_id)
    }
    while True:
        escolha = input("1-Nome\n2-Telefone\n3-Moto\n4-Placa\n5-Ano\n6-Serviço\n7-Status\n8-Observações\n9-ID do cliente\n10-ID da moto\n11-ID da manutenção\n12-Intervalo de datas\n13-Intervalo de quilometragem\n14-Intervalo de valor\n0-Pesquisar\nQual filtro deseja adicionar? ").strip().lower()
        if escolha == "sair":
            return "sair"
        if escolha == "0":
            try:
                resultados = core.consulta_filtrada(cursor, filtros)
            except ValueError as erro:
                print(f"Erro: {erro}")
                continue
            tabela_registros(resultados)
            return
        if escolha in opcoes:
            chave, mensagem, validador = opcoes[escolha]
            valor = pedir_valor(mensagem, validador)
            if valor == "sair":
                return "sair"
            if valor is None:
                filtros.pop(chave, None)
            else:
                filtros[chave] = valor
            continue
        if escolha == "12":
            data_inicial = pedir_valor("Data inicial (DD/MM/AAAA, opcional): ", validations.validar_data)
            if data_inicial == "sair":
                return "sair"
            data_final = pedir_valor("Data final (DD/MM/AAAA, opcional): ", validations.validar_data)
            if data_final == "sair":
                return "sair"
            if data_inicial is not None:
                filtros["data_inicial"] = data_inicial
            else:
                filtros.pop("data_inicial", None)
            if data_final is not None:
                filtros["data_final"] = data_final
            else:
                filtros.pop("data_final", None)
            continue
        if escolha == "13":
            quilometragem_inicial = pedir_valor("Quilometragem inicial (opcional): ", validations.validar_quilometragem)
            if quilometragem_inicial == "sair":
                return "sair"
            quilometragem_final = pedir_valor("Quilometragem final (opcional): ", validations.validar_quilometragem)
            if quilometragem_final == "sair":
                return "sair"
            if quilometragem_inicial is not None:
                filtros["quilometragem_inicial"] = quilometragem_inicial
            else:
                filtros.pop("quilometragem_inicial", None)
            if quilometragem_final is not None:
                filtros["quilometragem_final"] = quilometragem_final
            else:
                filtros.pop("quilometragem_final", None)
            continue
        if escolha == "14":
            valor_inicial = pedir_valor("Valor inicial em reais (opcional): R$ ", validations.validar_valor_reais)
            if valor_inicial == "sair":
                return "sair"
            valor_final = pedir_valor("Valor final em reais (opcional): R$ ", validations.validar_valor_reais)
            if valor_final == "sair":
                return "sair"
            if valor_inicial is not None:
                filtros["valor_inicial"] = valor_inicial
            else:
                filtros.pop("valor_inicial", None)
            if valor_final is not None:
                filtros["valor_final"] = valor_final
            else:
                filtros.pop("valor_final", None)
            continue
        print("Opção inválida.")

def ver_historico(cursor):
    escolha = pedir_opcao("1-Histórico de um cliente\n2-Todas as manutenções\nQual deseja visualizar? ", {"1": "cliente", "2": "todos"})
    if escolha == "sair":
        return "sair"
    if escolha == "todos":
        registros = core.todas_manutencoes(cursor)
        tabela_registros(registros)
        return
    clientes = core.listar_clientes(cursor)
    if not tabela_clientes(clientes):
        return
    cliente_id = pedir_id_existente(cursor, "ID do cliente: ", core.cliente_existe, "Cliente não encontrado.")
    if cliente_id == "sair":
        return "sair"
    registros = core.historico_cliente(cursor, cliente_id)
    tabela_registros(registros)
    
def cadastro(cursor):
    opcoes = {
        "1": cadastrar_cliente,
        "2": cadastrar_moto,
        "3": cadastrar_manutencao
    }
    return executar_menu(cursor, "1-Cliente\n2-Moto\n3-Manutenção\nO que deseja cadastrar? ", opcoes)
def alterar_dados(cursor):
    opcoes = {
        "1": alterar_cliente,
        "2": alterar_moto,
        "3": alterar_manutencao
    }
    return executar_menu(cursor, "1-Cliente\n2-Moto\n3-Manutenção\nO que deseja alterar? ", opcoes)
def deletar_dados(cursor):
    opcoes = {
        "1": deletar_cliente,
        "2": deletar_moto,
        "3": deletar_manutencao
    }
    return executar_menu(cursor, "1-Cliente\n2-Moto\n3-Manutenção\nO que deseja excluir? ", opcoes)
def pesquisar(cursor):
    opcoes = {
        "1": pesquisar_registros,
        "2": ver_historico
    }
    return executar_menu(cursor, "1-Pesquisar registros\n2-Ver histórico\nO que deseja fazer? ", opcoes)

def resumo(cursor):
    while True:
        escolha = pedir_opcao(
            "1-Todo o período\n2-Escolher período\n0-Voltar\nEscolha: ",
            {"0": "0", "1": "1", "2": "2"}
        )
        if escolha in ("0", "sair"):
            return escolha
        if escolha == "1":
            dados = core.resumo_periodo(cursor)
            exibir_resumo(dados)
            continue
        data_inicial = pedir_valor("Data inicial (DD/MM/AAAA): ", validations.validar_data_obrigatoria)
        if data_inicial == "sair":
            return "sair"
        data_final = pedir_valor("Data final (DD/MM/AAAA): ", validations.validar_data_obrigatoria)
        if data_final == "sair":
            return "sair"
        try:
            dados = core.resumo_periodo(cursor, data_inicial, data_final)
            exibir_resumo(dados)
        except ValueError as erro:
            print(f"Erro: {erro}")