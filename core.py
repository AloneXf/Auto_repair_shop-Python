import validations

###>>TABELAS<<###

def criar_tabelas(cursor):
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        telefone TEXT)
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS motos(
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        modelo TEXT NOT NULL,
        placa TEXT UNIQUE,
        ano INTEGER,
        FOREIGN KEY (cliente_id)
            REFERENCES clientes(id))
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manutencoes(
            id INTEGER PRIMARY KEY,
            moto_id INTEGER NOT NULL,
            servico TEXT NOT NULL,
            data TEXT NOT NULL,
            quilometragem INTEGER CHECK (quilometragem IS NULL OR quilometragem >= 0),
            valor_centavos INTEGER CHECK (valor_centavos IS NULL OR valor_centavos >= 0),
            status TEXT,
            observacoes TEXT,
            FOREIGN KEY (moto_id)
                REFERENCES motos(id))
        """)

###>>CLIENTES<<###

def inserir_cliente(cursor, nome, telefone):
    nome = validations.validar_nome(nome)
    telefone = validations.validar_telefone(telefone)
    cursor.execute("""
    INSERT INTO clientes (nome, telefone)
    VALUES (?, ?)
    """, (nome, telefone))
    return cursor.lastrowid

def cliente_existe(cursor, cliente_id):
    cliente_id = validations.validar_id(cliente_id)
    cursor.execute("""
    SELECT id FROM clientes
    WHERE id = ?
    """, (cliente_id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return False
    return True

def alterar_cliente(cursor, cliente_id, coluna, novo_valor):
    cliente_id = validations.validar_id(cliente_id)
    validadores = {
    "nome": validations.validar_nome,
    "telefone": validations.validar_telefone
    }
    if not cliente_existe(cursor, cliente_id):
        return False
    if coluna not in validadores:
        return False
    novo_valor = validadores[coluna](novo_valor)
    cursor.execute(f"""
        UPDATE clientes
        SET {coluna} = ?
        WHERE id = ?
        """, (novo_valor, cliente_id))
    return cursor.rowcount > 0

def deletar_cliente(cursor, cliente_id):
    cliente_id = validations.validar_id(cliente_id)
    cursor.execute("""
    DELETE FROM clientes
    WHERE id = ?
    """, (cliente_id,))
    return cursor.rowcount > 0

def listar_clientes(cursor):
    cursor.execute("""
    SELECT id, nome, telefone
     FROM clientes
     ORDER BY nome
    """)
    return cursor.fetchall()

###>>MOTOS<<###       

def inserir_moto(cursor, cliente_id, moto, placa, ano):
    cliente_id = validations.validar_id(cliente_id)
    moto = validations.validar_moto(moto)
    placa = validations.validar_placa(placa)
    ano = validations.validar_ano(ano)
    if not cliente_existe(cursor, cliente_id):
        return None
    cursor.execute("""
    INSERT INTO motos (cliente_id, modelo, placa, ano)
    VALUES (?, ?, ?, ?)
    """, (cliente_id, moto, placa, ano))
    return cursor.lastrowid

def moto_existe(cursor, moto_id):
    moto_id = validations.validar_id(moto_id)
    cursor.execute("""
    SELECT id FROM motos
    WHERE id = ?
    """, (moto_id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return False
    return True

def alterar_moto(cursor, moto_id, coluna, novo_valor):
    moto_id = validations.validar_id(moto_id)
    validadores = {
    "modelo": validations.validar_moto,
    "placa": validations.validar_placa,
    "ano": validations.validar_ano
    }
    if not moto_existe(cursor, moto_id):
        return False
    if coluna not in validadores:
        return False
    novo_valor = validadores[coluna](novo_valor)
    cursor.execute(f"""
    UPDATE motos
    SET {coluna} = ?
    WHERE id = ?
    """, (novo_valor, moto_id))
    return cursor.rowcount > 0

def deletar_moto(cursor, moto_id):
    moto_id = validations.validar_id(moto_id)
    cursor.execute("""
    DELETE FROM motos
    WHERE id = ?
    """, (moto_id,))
    return cursor.rowcount > 0

def listar_motos(cursor):
    cursor.execute("""
    SELECT motos.id, clientes.nome, motos.modelo, motos.placa, motos.ano             
    FROM motos
    JOIN clientes
    ON motos.cliente_id = clientes.id
    ORDER BY clientes.nome, motos.modelo
    """)
    return cursor.fetchall()

###>>MANUTENÇÕES<<###

def inserir_manutencao(cursor, moto_id, servico, data, quilometragem, valor_centavos, status, observacoes):
    moto_id = validations.validar_id(moto_id)
    servico = validations.validar_manutencao(servico)
    data = validations.validar_data_obrigatoria(data)
    quilometragem = validations.validar_quilometragem(quilometragem)
    valor_centavos = validations.validar_valor(valor_centavos)
    status = validations.validar_status(status)
    observacoes = validations.validar_observacao(observacoes)
    
    if not moto_existe(cursor, moto_id):
        return None
    data = data.isoformat()
    cursor.execute("""
    INSERT INTO manutencoes (moto_id, servico, data, quilometragem, valor_centavos, status, observacoes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (moto_id, servico, data, quilometragem, valor_centavos, status, observacoes))
    return cursor.lastrowid

def manutencao_existe(cursor, manutencao_id):
    manutencao_id = validations.validar_id(manutencao_id)
    cursor.execute("""
    SELECT id FROM manutencoes
    WHERE id = ?
    """, (manutencao_id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return False
    return True

def alterar_manutencao(cursor, manutencao_id, coluna, novo_valor):
    manutencao_id = validations.validar_id(manutencao_id)
    validadores = {
        "servico": validations.validar_manutencao,
        "data": validations.validar_data_obrigatoria,
        "quilometragem": validations.validar_quilometragem,
        "valor_centavos": validations.validar_valor,
        "status": validations.validar_status,
        "observacoes": validations.validar_observacao
    }
    if not manutencao_existe(cursor, manutencao_id):
        return False
    if coluna not in validadores:
        return False
    novo_valor = validadores[coluna](novo_valor)
    if coluna == "data":
        novo_valor = novo_valor.isoformat()
    cursor.execute(f"""
        UPDATE manutencoes
        SET {coluna} = ?
        WHERE id = ?
        """, (novo_valor, manutencao_id))
    return cursor.rowcount > 0

def deletar_manutencao(cursor, manutencao_id):
    manutencao_id = validations.validar_id(manutencao_id)
    cursor.execute("""
    DELETE FROM manutencoes
    WHERE id = ?
    """, (manutencao_id,))
    return cursor.rowcount > 0

def listar_manutencoes(cursor):
    cursor.execute("""
    SELECT manutencoes.id, clientes.nome, motos.modelo, manutencoes.servico, manutencoes.data,
    manutencoes.quilometragem, manutencoes.valor_centavos, manutencoes.status          
    FROM manutencoes
    JOIN motos
    ON manutencoes.moto_id = motos.id
    JOIN clientes
    ON motos.cliente_id = clientes.id
    ORDER BY manutencoes.data DESC
    """)
    return cursor.fetchall()

###>>>CONSULTAS<<###

def _consultar_registros(cursor, condicao="", parametros=()):
    sql = """
    SELECT clientes.id, clientes.nome, clientes.telefone, motos.id, motos.modelo, motos.placa,
        motos.ano, manutencoes.id, manutencoes.servico, manutencoes.data, manutencoes.quilometragem,
        manutencoes.valor_centavos, manutencoes.status, manutencoes.observacoes         
    FROM clientes
    LEFT JOIN motos
    ON clientes.id = motos.cliente_id
    LEFT JOIN manutencoes
    ON motos.id = manutencoes.moto_id
    """
    if condicao:
        sql += f"\nWHERE {condicao}"
    sql += "\nORDER BY manutencoes.data DESC"
    cursor.execute(sql, parametros)
    return cursor.fetchall()

def consulta_filtrada(cursor, filtros):
    if not isinstance(filtros, dict):
        raise ValueError("Os filtros devem ser informados em um dicionário.")
    filtros_permitidos = {
    "nome",
    "telefone",
    "moto",
    "placa",
    "servico",
    "observacoes",
    "ano",
    "status",
    "data_inicial",
    "data_final",
    "valor_inicial",
    "valor_final",
    "quilometragem_inicial",
    "quilometragem_final",
    "cliente_id",
    "moto_id",
    "manutencao_id"
    }
    for filtro in filtros:
        if filtro not in filtros_permitidos:
            raise ValueError(f"Filtro inválido: {filtro}.")
    condicoes = []
    parametros = []
    nome = validations.validar_texto_busca(filtros.get("nome"))
    if nome is not None:
        condicoes.append("clientes.nome LIKE ?")
        parametros.append(f"%{nome}%")
    telefone = validations.validar_texto_busca(filtros.get("telefone"))
    if telefone is not None:
        condicoes.append("clientes.telefone LIKE ?")
        parametros.append(f"%{telefone}%")
    moto = validations.validar_texto_busca(filtros.get("moto"))
    if moto is not None:
        condicoes.append("motos.modelo LIKE ?")
        parametros.append(f"%{moto}%")
    placa = validations.normalizar_placa(filtros.get("placa"))
    if placa is not None:
        condicoes.append("motos.placa LIKE ?")
        parametros.append(f"%{placa}%")
    servico = validations.validar_texto_busca(filtros.get("servico"))
    if servico is not None:
        condicoes.append("manutencoes.servico LIKE ?")
        parametros.append(f"%{servico}%")
    observacoes = validations.validar_texto_busca(filtros.get("observacoes"))
    if observacoes is not None:
        condicoes.append("manutencoes.observacoes LIKE ?")
        parametros.append(f"%{observacoes}%")
    ano = validations.validar_ano(filtros.get("ano"))   
    if ano is not None:
        condicoes.append("motos.ano = ?")
        parametros.append(ano)
    status = validations.validar_status(filtros.get("status"))
    if status is not None:
        condicoes.append("manutencoes.status = ?")
        parametros.append(status)     
    data_inicial = validations.validar_data(filtros.get("data_inicial"))
    data_final = validations.validar_data(filtros.get("data_final"))
    if data_inicial is not None and data_final is not None and data_inicial > data_final:
        raise ValueError("A data inicial não pode ser maior que a data final.")
    if data_inicial is not None:
        condicoes.append("manutencoes.data >= ?")
        parametros.append(data_inicial.isoformat())
    if data_final is not None:
        condicoes.append("manutencoes.data <= ?")
        parametros.append(data_final.isoformat()) 
    valor_inicial = validations.validar_valor(filtros.get("valor_inicial"))
    valor_final = validations.validar_valor(filtros.get("valor_final"))
    if (
        valor_inicial is not None
        and valor_final is not None
        and valor_inicial > valor_final):
        raise ValueError("O valor inicial não pode ser maior que o valor final.")
    if valor_inicial is not None:
        condicoes.append("manutencoes.valor_centavos >= ?")
        parametros.append(valor_inicial)
    if valor_final is not None:
        condicoes.append("manutencoes.valor_centavos <= ?")
        parametros.append(valor_final)  
    quilometragem_inicial = validations.validar_quilometragem(
        filtros.get("quilometragem_inicial"))
    quilometragem_final = validations.validar_quilometragem(
        filtros.get("quilometragem_final"))
    if (
        quilometragem_inicial is not None
        and quilometragem_final is not None
        and quilometragem_inicial > quilometragem_final):
        raise ValueError("A quilometragem inicial não pode ser maior que a quilometragem final.")
    if quilometragem_inicial is not None:
        condicoes.append("manutencoes.quilometragem >= ?")
        parametros.append(quilometragem_inicial)
    if quilometragem_final is not None:
        condicoes.append("manutencoes.quilometragem <= ?")
        parametros.append(quilometragem_final)
    cliente_id = validations.validar_id(filtros.get("cliente_id")) if filtros.get("cliente_id") is not None else None
    if cliente_id is not None:
        condicoes.append("clientes.id = ?")
        parametros.append(cliente_id)
    moto_id = validations.validar_id(filtros.get("moto_id")) if filtros.get("moto_id") is not None else None
    if moto_id is not None:
        condicoes.append("motos.id = ?")
        parametros.append(moto_id)
    manutencao_id = validations.validar_id(filtros.get("manutencao_id")) if filtros.get("manutencao_id") is not None else None
    if manutencao_id is not None:
        condicoes.append("manutencoes.id = ?")
        parametros.append(manutencao_id)
    condicao = " AND ".join(condicoes)
    return _consultar_registros(cursor, condicao, tuple(parametros))

def historico_cliente(cursor, cliente_id):
    cliente_id = validations.validar_id(cliente_id)
    condicao = "clientes.id = ? AND manutencoes.id IS NOT NULL"
    parametros = (cliente_id,)
    return _consultar_registros(cursor, condicao, parametros)

def todas_manutencoes(cursor):
    condicao = "manutencoes.id IS NOT NULL"
    return _consultar_registros(cursor, condicao)

###>>>RELATÓRIOS<<###

def resumo_periodo(cursor, data_inicial=None, data_final=None):
    data_inicial = validations.validar_data(data_inicial)
    data_final = validations.validar_data(data_final)
    if data_inicial is not None and data_final is not None and data_inicial > data_final:
        raise ValueError("A data inicial não pode ser maior que a data final.")
    condicoes = []
    parametros = []
    if data_inicial is not None:
        condicoes.append("data >= ?")
        parametros.append(data_inicial.isoformat())
    if data_final is not None:
        condicoes.append("data <= ?")
        parametros.append(data_final.isoformat())
    sql = """
    SELECT
        COUNT(*),
        SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status = 'Em andamento' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status = 'Concluída' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status = 'Cancelada' THEN 1 ELSE 0 END),
        COALESCE(SUM(valor_centavos), 0),
        COALESCE(SUM(CASE WHEN status = 'Concluída' THEN valor_centavos ELSE 0 END), 0)
    FROM manutencoes
    """
    if condicoes:
        sql += "\nWHERE " + " AND ".join(condicoes)
    cursor.execute(sql, tuple(parametros))
    resultado = cursor.fetchone()
    return {
        "total": resultado[0],
        "pendentes": resultado[1] or 0,
        "em_andamento": resultado[2] or 0,
        "concluidas": resultado[3] or 0,
        "canceladas": resultado[4] or 0,
        "valor_total": resultado[5],
        "valor_concluido": resultado[6]
    }
        

    
