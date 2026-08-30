import unicodedata
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

def validar_id(valor):
    if valor is None:
        raise ValueError("O ID é obrigatório.")
    if type(valor) not in (str, int):
        raise ValueError("O ID deve ser um número inteiro.")
    if isinstance(valor, str):
        valor = valor.strip()
    if valor == "":
        raise ValueError("O ID é obrigatório.")
    try:
        valor = int(valor)
    except ValueError:
        raise ValueError("O ID deve ser um número inteiro.")
    if valor <= 0:
        raise ValueError("O ID deve ser maior que zero.")
    return valor
def validar_texto_busca(texto):
    if texto is None:
        return None
    if type(texto) is not str:
        raise ValueError("O texto de busca deve ser um texto.") 
    texto = texto.strip()
    if texto == "":
        return None
    return texto
def validar_data_obrigatoria(data):
    data = validar_data(data)
    if data is None:
        raise ValueError("A data da manutenção é obrigatória.")
    return data

def validar_valor_reais(valor):
    valor_centavos = normalizar_valor(valor)
    return validar_valor(valor_centavos)


def validar_nome(nome):
    if nome is None:
        raise ValueError("O nome é obrigatório.")
    if not isinstance(nome, str):
        raise ValueError("O nome deve ser um texto.")
    nome = nome.strip()
    if not nome:
        raise ValueError("O nome é obrigatório.")
    return nome
def validar_telefone(telefone):
    if telefone is None:
        return None
    if not isinstance(telefone, str):
        raise ValueError("O telefone deve ser um texto.")
    telefone = telefone.strip()
    if not telefone:
        return None
    if not telefone.isdigit() or not telefone.isascii():
        raise ValueError("O telefone deve conter apenas números.")
    return telefone

def validar_moto(moto):
    if moto is None:
        raise ValueError("O modelo da moto é obrigatório.")
    if not isinstance(moto, str):
        raise ValueError("O modelo da moto deve ser um texto.")
    moto = moto.strip()
    if not moto:
        raise ValueError("O modelo da moto é obrigatório.")
    return moto
def normalizar_placa(placa):
    if placa is None:
        return None
    if not isinstance(placa, str):
        raise ValueError("A placa deve ser um texto.")
    placa = placa.strip()
    if not placa:
        return None
    placa = unicodedata.normalize("NFD", placa)
    placa = "".join(
    caractere
    for caractere in placa
    if not unicodedata.combining(caractere)
    )
    placa = placa.upper()
    placa = placa.replace("-", "")
    return placa
def validar_placa(placa):
    placa = normalizar_placa(placa)
    if placa is None:
        return None
    if len(placa) != 7:
        raise ValueError("A placa deve conter 7 caracteres.")
    if placa[:3].isalpha() and placa[:3].isascii() and placa[3:].isdigit() and placa[3:].isascii():
        return placa
    if placa[:3].isalpha() and placa[:3].isascii() and placa[4].isalpha() and placa[4].isascii() and placa[3].isdigit() and placa [3].isascii() and placa[5:].isdigit() and placa[5:].isascii():
        return placa
    raise ValueError("A placa informada é inválida.")
def validar_ano(ano):
    if ano is None:
        return None
    if type(ano) not in (str, int):
        raise ValueError("O ano deve ser um número inteiro.")
    if isinstance(ano, str):
        ano = ano.strip()
    if ano == "":
        return None
    try:
        ano = int(ano)
    except (ValueError, TypeError):
        raise ValueError("O ano deve ser um número inteiro.")
    ano_atual = date.today().year
    if ano < 1900 or ano > ano_atual + 1:
        raise ValueError(f"O ano deve estar entre 1900 e {ano_atual + 1}.")
    return ano

def validar_manutencao(servico):
    if servico is None:
        raise ValueError("O serviço é obrigatório.")
    if not isinstance(servico, str):
        raise ValueError("O serviço deve ser um texto.")
    servico = servico.strip()
    if not servico:
        raise ValueError("O serviço é obrigatório.")
    return servico
def validar_data(data):
    if data is None:
        return None
    if isinstance(data, datetime):
        return data.date()
    if isinstance(data, date):
        return data
    if not isinstance(data, str):
        raise ValueError("A data deve ser um texto no formato DD/MM/AAAA.")
    data = data.strip()
    if data == "":
        return None
    try:
        data = datetime.strptime(data, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("A data deve ser válida e estar no formato DD/MM/AAAA.")
    return data
def validar_quilometragem(quilometragem):
    if quilometragem is None:
        return None
    if type(quilometragem) not in (str, int):
        raise ValueError("A quilometragem deve ser um número inteiro.")
    if isinstance(quilometragem, str):
        quilometragem = quilometragem.strip()
    if quilometragem == "":
        return None
    try:
        quilometragem = int(quilometragem)
    except (ValueError, TypeError):
        raise ValueError("A quilometragem deve ser um número inteiro.")
    if quilometragem >= 0:
        return quilometragem
    raise ValueError("A quilometragem não pode ser negativa.")
def normalizar_valor(valor):
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise ValueError("O valor deve ser informado como texto.")
    valor = valor.strip()
    if valor == "":
        return None
    valor = valor.replace(",", ".")
    if "e" in valor.lower():
        raise ValueError("O valor informado é inválido.")
    try:  
        valor = Decimal(valor)
    except InvalidOperation:
        raise ValueError("O valor informado é inválido.")
    if not valor.is_finite():
        raise ValueError("O valor informado é inválido.")
    centavos = valor * 100
    if centavos != centavos.to_integral_value():
        raise ValueError("O valor deve ter no máximo duas casas decimais.")
    centavos = int(centavos)
    return centavos
def validar_valor(valor_centavos):
    if valor_centavos is None:
        return None
    if type(valor_centavos) is not int:
        raise ValueError("O valor deve estar representado em centavos.")
    if valor_centavos < 0:
        raise ValueError("O valor não pode ser negativo.")
    return valor_centavos
def validar_status(status):
    valido = {
    "pendente": "Pendente",
    "em andamento": "Em andamento",
    "concluída": "Concluída",
    "cancelada": "Cancelada"
    }
    if status is None:
        return None
    if not isinstance(status, str):
        raise ValueError("O status deve ser um texto.")
    status = status.strip().lower()
    if status == "":
        return None
    if status not in valido:
        raise ValueError("O status deve ser: Pendente, Em andamento, Concluída ou Cancelada.")
    return valido[status]
def validar_observacao(observacao):
    if observacao is None:
        return None
    if not isinstance(observacao, str):
        raise ValueError("A observação deve ser um texto.")
    observacao = observacao.strip()
    if observacao == "":
        return None
    return observacao