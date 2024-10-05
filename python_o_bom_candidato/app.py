import locale

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .crawler import crawler_resources
from .data_processing import consulta_cand, bens_candidato
from .db_operations import search_candidate, insert_basic_info_db, insert_bens_info_db, get_picture_from_server, search_unique_number
from .PATHS_AND_URLS import url, path_to_consulta_cand, path_to_consulta_cand_complementar, path_to_bens_candidato

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = FastAPI()
templates = Jinja2Templates(directory="./frontend")
templates.env.globals["currency"] = locale.currency

app = FastAPI()
app.mount("/o_bom_candidato_files", StaticFiles(directory="./o_bom_candidato_files"), name="o_bom_candidato_files")

@app.get("/search", response_class=HTMLResponse)
def search_candidates(request:Request, candidate_to_search:str):
    if not candidate_to_search.strip():
        context = {'request': request}
        return templates.TemplateResponse("candidate_info.html", context)

    candidates = search_candidate(candidate_to_search)
    candidates_with_picture = get_picture_from_server(candidates)
    return templates.TemplateResponse("candidate_info.html", {"request":request, "candidates":candidates_with_picture})


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)


@app.get('/candidate_page/{unique_number}', response_class=HTMLResponse)
def candidate_page(request:Request, unique_number:str):
    candidate = get_picture_from_server(dict(search_unique_number(unique_number=unique_number)))
    print(candidate)
    return templates.TemplateResponse("candidate_card.html", {"request":request, "candidate":candidate})


@app.post("/crawl_candidates_basic_info/")
def update_candidates_basic_info():
    log = crawler_resources(url)
    documents_info = consulta_cand(path_to_consulta_cand=path_to_consulta_cand, path_to_consulta_cand_complt=path_to_consulta_cand_complementar)
    log_info_db = insert_basic_info_db(documents_info, 'BA')
    documents_bens = bens_candidato(path_to_bens_candidato=path_to_bens_candidato)
    log_bens_db = insert_bens_info_db(documents_bens, 'BA')
    return {
        "Files info": log,
        "Db saving basic info": log_info_db,
        "Db saving bens info": log_bens_db
    }

# @app.put("/update_candidates_basic_info")
# def update_candidates_info_db():
#     documents_info = consulta_cand(path_to_consulta_cand=path_to_consulta_cand, path_to_consulta_cand_complt=path_to_consulta_cand_complementar)
#     # atualizar documentos
#     documents_bens = bens_candidato(path_to_bens_candidato=path_to_bens_candidato)
#     #atualizar documentos
#     return {
#         "Db saving basic info": log_info_db,
#         "Db saving bens info": log_bens_db
#     }

@app.put("/candidates_info_updated/")
def insert_info_in_db():
    log = crawler_resources(url)
    return {
        "Files info": log,
    }
