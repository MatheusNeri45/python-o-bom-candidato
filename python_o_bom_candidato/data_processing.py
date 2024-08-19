import pandas as pd
from collections import defaultdict

def consulta_cand(path_to_consulta_cand, path_to_consulta_cand_complt) -> list[dict]:
    consulta_cand = pd.read_csv(path_to_consulta_cand, encoding='latin1', sep=";")
    consulta_cand_complement = pd.read_csv(path_to_consulta_cand_complt, encoding='latin1', sep=';')
    consulta_cand = pd.merge(consulta_cand, consulta_cand_complement, how="inner", on="SQ_CANDIDATO")
    consulta_cand_salvador = consulta_cand[consulta_cand["NM_UE"] == 'SALVADOR']

    info = consulta_cand_salvador[['NM_CANDIDATO','DS_CARGO', 'SQ_CANDIDATO', 'NR_CANDIDATO',  'NM_URNA_CANDIDATO', 
                                   'NM_SOCIAL_CANDIDATO', 'NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO', 'SQ_COLIGACAO',
                                   'SG_UF_NASCIMENTO', 'DS_GENERO', 'DS_GRAU_INSTRUCAO', 'CD_ESTADO_CIVIL', 'DS_COR_RACA', 'DS_OCUPACAO',
                                   'DS_ESTADO_CIVIL', 'DS_NACIONALIDADE', 'ST_QUILOMBOLA', 'CD_ETNIA_INDIGENA', 'DS_ETNIA_INDIGENA', 
                                   'VR_DESPESA_MAX_CAMPANHA', 'ST_DECLARAR_BENS', 'ST_PREST_CONTAS']]
    
    documents = [{
        "Nome completo": row.NM_CANDIDATO.title(),
        "Nome na urna":row.NM_URNA_CANDIDATO.title(),
        "Número do candidato":row.NR_CANDIDATO,
        "Número do partido":row.NR_PARTIDO,
        "Sigla do partido":row.SG_PARTIDO,
        "Nome do partido":row.NM_PARTIDO,
        "UF de nascimento":row.SG_UF_NASCIMENTO,
        "Gênero":row.DS_GENERO.title(),
        "Grau de instrução":row.DS_GRAU_INSTRUCAO.title(),
        "Estado civil":match_marital_status(row.CD_ESTADO_CIVIL),
        "Raça":row.DS_COR_RACA.title(),
        "Ocupação":row.DS_OCUPACAO.title(),
        "Nacionalidade":row.DS_NACIONALIDADE.title(),
        "Quilombola":False if row.ST_QUILOMBOLA == "N" else True,
        "Indígena":False if row.CD_ETNIA_INDIGENA == -1 else [row.CD_ETNIA_INDIGENA, row.DS_ETNIA_INDIGENA],
        "Despesa máxima da campanha":row.VR_DESPESA_MAX_CAMPANHA,
        "Declarou bens":False if row.ST_DECLARAR_BENS == "N" else True,
        "Prestou contas":False if row.ST_PREST_CONTAS == "N" else True,
        "Número único":row.SQ_CANDIDATO,
        "Concorrendo a":row.DS_CARGO.title(),
                }for index, row in info.iterrows()]

    return documents

def comma_to_dot(number:str) -> float:
    return float(number.replace(',','.')) if number is not None else 0.0

def bens_candidato(path_to_bens_candidato):
    consulta_cand = pd.read_csv(path_to_bens_candidato, encoding='latin1', sep=";")
    consulta_cand_salvador = consulta_cand[consulta_cand["NM_UE"] == 'SALVADOR']
    bens = consulta_cand_salvador[['SQ_CANDIDATO','DS_TIPO_BEM_CANDIDATO', 'VR_BEM_CANDIDATO']]
    bens_dict = defaultdict(lambda: defaultdict(float))

    for index, row in bens.iterrows():
        bens_dict[row.SQ_CANDIDATO][row.DS_TIPO_BEM_CANDIDATO] += comma_to_dot(row.VR_BEM_CANDIDATO)

    bens_documents = [{
        "Número único": sq_candidato,
        "Bens": dict(bens_dict)
    } for sq_candidato, bens_dict in bens_dict.items()]
    return bens_documents

def match_marital_status(marital_status_code) -> str:
    match marital_status_code:
        case 1:
            return "Solteiro(a)"
        case 3:
            return "Casado(a)"
        case 5:
            return "Viúvo(a)"
        case 7:
            return "Separado(a) judicialmente"
        case 9:
            return "Divorciado(a)"
        case _:
            return "Não informado"
