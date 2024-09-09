from pymongo import MongoClient
import re
import os
client = MongoClient()

db = client["2024_Elections"]
collection = db["BA"]
bahia_collection = db.BA


def insert_basic_info_db(documents, state) -> str:
    try: 
        db[state].insert_many(documents)
    except Exception:
        return "Error inserting candidates information in the DB."
    else:
        return "The candidates information were inserted in the DB."

def insert_bens_info_db(all_candidates_bens_info, state) -> list[str]:
    log = {
        "Updated":0,
        "Not updated":0,
        "Log not updated":[],
    }
    for candidate_bens_info in all_candidates_bens_info:
        try:
            query = {"Número único": candidate_bens_info.get("Número único")}
            bens = {"$set": {"Bens": candidate_bens_info.get("Bens")}}
            db[state].update_one(query, bens)
        except Exception as e:  # noqa: E722
            log["Not updated"]+=1
            log["Log not updated"].append(f'Error updating {candidate_bens_info.get("Número único")}: {str(e)}.')
        else:
            log["Updated"]+=1
    return log

def search_candidate(candidato_buscado:str) -> list:
    regex = f".*{candidato_buscado}.*"
    information = list(bahia_collection.find({"Nome completo": {"$regex": re.compile(regex, re.IGNORECASE)}}))
    return information

def search_unique_number(unique_number:str) -> list:
    print(unique_number)
    information = bahia_collection.find_one({"Número único": int(unique_number) })
    return information

def get_picture_from_server(candidates:list) -> list[str]:
    if type(candidates) is list:
        for candidate in candidates:
            numero_unico = candidate.get("Número único")
            path_system_jpg = f'./o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpg'
            path_system_jpeg = f'./o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpeg'
            path_jpg = f'/o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpg'
            path_jpeg = f'/o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpeg'
            check_file_jpg = os.path.isfile(path_system_jpg)
            check_file_jpeg = os.path.isfile(path_system_jpeg)
            if check_file_jpg:
                path = path_jpg
            elif check_file_jpeg:
                path = path_jpeg
            else:
                path = None
            candidate['Foto URL'] = path
    else:
        
        numero_unico = candidates.get("Número único")
        path_system_jpg = f'./o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpg'
        path_system_jpeg = f'./o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpeg'
        path_jpg = f'/o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpg'
        path_jpeg = f'/o_bom_candidato_files/candidatos-2024/BA/FBA{numero_unico}_div.jpeg'
        check_file_jpg = os.path.isfile(path_system_jpg)
        check_file_jpeg = os.path.isfile(path_system_jpeg)
        if check_file_jpg:
            path = path_jpg
        elif check_file_jpeg:
            path = path_jpeg
        else:
            path = None
        candidates['Foto URL'] = path

    return candidates