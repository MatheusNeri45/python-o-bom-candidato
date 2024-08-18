from fastapi import FastAPI
from .crawler import crawler_resources
from .data_processing import consulta_cand, bens_candidato
from .db_operations import insert_basic_info_db, insert_bens_info_db
from .PATHS_AND_URLS import url, path_to_consulta_cand, path_to_consulta_cand_complementar, path_to_bens_candidato
app = FastAPI()

@app.post("/update_candidates_basic_info")
def update_candidates_basic_info():
    # log = crawler_resources(url)
    # documents_info = consulta_cand(path_to_consulta_cand=path_to_consulta_cand, path_to_consulta_cand_complt=path_to_consulta_cand_complementar)
    # log_info_db = insert_basic_info_db(documents_info, 'BA')
    documents_bens = bens_candidato(path_to_bens_candidato=path_to_bens_candidato)
    log_bens_db = insert_bens_info_db(documents_bens, 'BA')
    print(log_bens_db)
    return {
        # "Files info": log,
        # "Db saving basic info": log_info_db,
        "Db saving bens info": log_bens_db
    }
