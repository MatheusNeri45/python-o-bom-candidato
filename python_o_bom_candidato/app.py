from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .db_operations import look_for_candidate_information
# from crawler import crawler_resources
# from data_processing import consulta_cand, bens_candidato
# from db_operations import insert_basic_info_db, insert_bens_info_db
# from PATHS_AND_URLS import url, path_to_consulta_cand, path_to_consulta_cand_complementar, path_to_bens_candidato

app = FastAPI()

templates = Jinja2Templates(directory="../frontend")

@app.get("/search", response_class=HTMLResponse)
def search_candidates(request:Request, candidate_to_search:str):
    candidate = look_for_candidate_information(candidate_to_search)
    return templates.TemplateResponse("candidate_info.html", {"request":request, "candidate":candidate})


@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

# @app.post("/update_candidates_basic_info/")
# def update_candidates_basic_info():
#     log = crawler_resources(url)
#     documents_info = consulta_cand(path_to_consulta_cand=path_to_consulta_cand, path_to_consulta_cand_complt=path_to_consulta_cand_complementar)
#     log_info_db = insert_basic_info_db(documents_info, 'BA')
#     documents_bens = bens_candidato(path_to_bens_candidato=path_to_bens_candidato)
#     log_bens_db = insert_bens_info_db(documents_bens, 'BA')
#     return {
#         "Files info": log,
#         "Db saving basic info": log_info_db,
#         "Db saving bens info": log_bens_db
#     }
