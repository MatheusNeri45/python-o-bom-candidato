from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .crawler import crawler_resources
from .data_processing import consulta_cand, bens_candidato
from .db_operations import search_candidate, insert_basic_info_db, insert_bens_info_db, get_picture_from_server
from .PATHS_AND_URLS import url, path_to_consulta_cand, path_to_consulta_cand_complementar, path_to_bens_candidato

app = FastAPI()
templates = Jinja2Templates(directory="./frontend")

app = FastAPI()
app.mount("/o_bom_candidato_files", StaticFiles(directory="/Users/matheusneri/Documents/python-projects/o_bom_candidato_files"), name="o_bom_candidato_files")

@app.get("/search", response_class=HTMLResponse)
def search_candidates(request:Request, candidate_to_search:str):
    if not candidate_to_search.strip():
        context = {'request': request}
        return templates.TemplateResponse("candidate_info.html", context)
    candidates = get_picture_from_server(search_candidate(candidate_to_search))
    print(candidates)
    return templates.TemplateResponse("candidate_info.html", {"request":request, "candidates":candidates})

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

@app.post("/update_candidates_basic_info/")
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
