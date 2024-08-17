import pandas as pd
from db_operations import insert_many_db
# Informações que eu quero
# INFORMAÇÕES GERAIS
#CONSULTA CAND
# NM_TIPO_ELEICAO, NR_TURNO, DT_ELEICAO, TP_ABRANGENCIA_ELEICAO (MUN., EST. FED.)
# SG_UE (UNIDADE ELEITORAL OU MUNICIPIO, CIDADE)
# INFORMAÇÕES DO CANDIDATO
# NM_UE, CD_CARGO (CODIGO DO CARGO EM NUMERO), DS_CARGO (DESCRIÇÃO DO CARGO)
# SQ_CANDIDATO (NÚMERO DE SERIE DO CANDIDATO), NR_CANDIDATO (NUMERO DO CANDIDATO NA URNA), NM_URNA_CANDIDATO (NOME DO CANDIDATO NA URNA), NM_SOCIAL_CANDIDATO (NOME SOCIAL DO CANDIDATO)
# NR_CPF_CANDIDATO, DS_EMAIL, NR_PARTIDO, SG_PARTIDO (SIGLA), NM_PARTIDO, SQ_COLIGACAO (NUMERO DE SERIE DO PARTIDO), SG_UF_NASCIMENTO, 
# DS_GENERO, DS_GRAU_INSTRUCAO, DS_ESTADO_CIVIL, DS_COR_RACA, DS_OCUPACAO
# DS_GRAU_INSTRUCAO, CD_ESTADO_CIVIL, DR_ESTADO_CIVIL
#CONSULT CAND COMPLEMENTAR
# DS_NACIONALIDADE, ST_QUILOMBOLA, CD_ETNIA_INDIGENA, DS_ETNIA_INDIGENA, VR_DESPESA_MAX_CAMPANHA, ST_DECLARAR_BENS, ST_PRESTACAO DE CONTAS
#BEM CANDIDATO
# DS_TIPO_BEM_CANDIDATO, DS_BEM_CANDIDATO, VR_BEM_CANDIDATO
#CONSULTA_VAGAS
# INFOS SOBRE VAGAS DO ESTADO
#REDES SOCIAIS
# DS_URL
#FOTOS
# FBASQ_CANDIDATO_div.jpg
#PROPOSTA
# 2024BASQ_CANDIDATO_01.pdf

election_year = 2024
state = 'BA'
path_to_consulta_cand = '../o_bom_candidato_files/candidatos-2024/BA/consulta_cand_2024_BA.csv'
path_to_consulta_cand_complementar = '../o_bom_candidato_files/candidatos-2024/BA/consulta_cand_complementar_2024_BA.csv'

def consulta_cand(path_to_consulta_cand, path_to_consulta_cand_complt) -> list[dict]:
    consulta_cand = pd.read_csv(path_to_consulta_cand, encoding='latin1', sep=";")
    consulta_cand_complement = pd.read_csv(path_to_consulta_cand_complt, encoding='latin1', sep=';')
    consulta_cand = pd.merge(consulta_cand, consulta_cand_complement, how="inner", on="SQ_CANDIDATO")
    consulta_cand_salvador = consulta_cand[consulta_cand["NM_UE"] == 'SALVADOR']
    info = consulta_cand_salvador[['NM_CANDIDATO','DS_CARGO', 'SQ_CANDIDATO', 'NR_CANDIDATO',  'NM_URNA_CANDIDATO', 
                                   'NM_SOCIAL_CANDIDATO', 'NR_CPF_CANDIDATO', 'NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO', 'SQ_COLIGACAO',
                                   'SG_UF_NASCIMENTO', 'DS_GENERO', 'DS_GRAU_INSTRUCAO', 'CD_ESTADO_CIVIL', 'DS_COR_RACA', 'DS_OCUPACAO',
                                   'DS_ESTADO_CIVIL', 'DS_NACIONALIDADE', 'ST_QUILOMBOLA', 'CD_ETNIA_INDIGENA', 'DS_ETNIA_INDIGENA', 
                                   'VR_DESPESA_MAX_CAMPANHA', 'ST_DECLARAR_BENS', 'ST_PREST_CONTAS']]
    documents = [{
        "Nome completo": row.NM_CANDIDATO,
        "Nome na urna":row.NM_URNA_CANDIDATO,
        "Número do candidato":row.NR_CANDIDATO,
        "Número do partido":row.NR_PARTIDO,
        "Sigla do partido":row.SG_PARTIDO,
        "Nome do partido":row.NM_PARTIDO,
        "UF de nascimento":row.SG_UF_NASCIMENTO,
        "Gênero":row.DS_GENERO,
        "Grau de instrução":row.DS_GRAU_INSTRUCAO,
        "Estado civil":match_marital_status(row.CD_ESTADO_CIVIL),
        "Raça":row.DS_COR_RACA,
        "Ocupação":row.DS_OCUPACAO,
        "Nacionalidade":row.DS_NACIONALIDADE,
        "Quilombola":row.ST_QUILOMBOLA,
        "Indígena":[row.CD_ETNIA_INDIGENA, row.DS_ETNIA_INDIGENA],
        "Despesa máxima da campanha":row.VR_DESPESA_MAX_CAMPANHA,
        "Declarou bens":row.ST_DECLARAR_BENS,
        "Prestou contas":row.ST_PREST_CONTAS,
        "CPF":row.NR_CPF_CANDIDATO,
        "Número único":row.SQ_CANDIDATO,
        "Concorrendo a":row.DS_CARGO,
                }for index, row in info.iterrows()]
    
    return documents

def process_data():
    pass
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
        
documents = consulta_cand(path_to_consulta_cand=path_to_consulta_cand, path_to_consulta_cand_complt=path_to_consulta_cand_complementar)
log = insert_many_db(documents)
print(log)