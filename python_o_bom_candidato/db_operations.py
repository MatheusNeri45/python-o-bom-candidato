from pymongo import MongoClient

client = MongoClient()

db = client["2024_Elections"]

collection = db["BA"]


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
