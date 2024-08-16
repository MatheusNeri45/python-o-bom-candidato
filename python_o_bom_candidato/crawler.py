from bs4 import BeautifulSoup
import requests
import os
from zipfile import ZipFile
from io import BytesIO
from STATES import STATES as states

def get_resource_urls(url:str) -> list[str]:
    #Returns the resource URLS for the year of 2024 and only for the state of Bahia (you can change by changing the main URL) from the main page of website
    resources_bahia_useful = []
    print("The code is getting the resource urls")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all('li',class_= "resource-item")
    #I need 3 pieces of information, the title of the resource (if it is for a specific state, the state's abbreviature will be shown ex; "BA"), the paragraph ->
    #-> information which shows if the resource is from all states or a specific one (empty for specific one) and the link to the resource.
    resources = [[tag.p.string, tag.a.get('title'), tag.find('a',class_= "resource-url-analytics").get('href')] for tag in tags]
    #I take out all urls that do not contain information about the state of Bahia and the criminal records due to being too large of a file
    resources_bahia_useful = [resource[2] for resource in resources if resource[0].find('Todas as UFs') !=-1 or resource[1].find('BA')!=-1 and resource[1].find('Certi') == -1]
    print("Got all files")
    return resources_bahia_useful

def filename_in_folder(file_name:str) -> str:
    #Some files are inside a folder, this function removes the folder name that is on the original zip filename
    print(f"{file_name}")

    f = file_name[::-1]
    print(f"{f}")
    position = f.find("/")
    print(position)
    if position == -1:
        filename_in_folder = file_name
    else:
        filename_in_folder = f[:position]
        filename_in_folder = filename_in_folder[::-1]
    print(filename_in_folder)
    return filename_in_folder

def make_folders(directory:str, election_year: str):
    #creates the needed folders
    os.makedirs(directory, exist_ok=True)
    for key in states.keys():
        folder = f'../o_bom_candidato_files/{election_year}/{key}/'
        os.makedirs(folder, exist_ok=True)

def decide_directory(file_name: str, directory: str) -> str:
    #decides which directory each file is going to
    for key in states.keys():
        if key in file_name:
            file_directory = f'{directory}/{key}/{file_name}'
            return file_directory
    
    return f'{directory}/{file_name}'


def download_resources(resource_urls:list[str], url:str) -> dict:
    #downloads the resources to
    log = {
        "Downloaded":0,
        "Not Downloaded":0,
        "Log not downloaded":[],
    }
    print(resource_urls)
    election_year = url[url.find("candidatos")::]
    directory = f'../o_bom_candidato_files/{election_year}/'
    make_folders(url, election_year)
    for resource_url in resource_urls:
        print("Getting resource")
        response = requests.get(resource_url)
        zip_file = BytesIO(response.content)
        print("Opening zip file")
        with ZipFile (zip_file, 'r') as z:
            files_name_list = z.namelist()
            print("The code got the files name list inside the specific zip file")
            for fname in files_name_list:
                file_name = filename_in_folder(fname)
                if file_name.find('leiame.pdf')!=-1 or file_name.find('BA')!=-1 or file_name.find('BR')!=-1:
                    try:
                        print(f"The code just started savin the file: {file_name}")
                        with z.open(fname) as f:
                            content = f.read()
                            file_directory = decide_directory(file_name=file_name, directory=directory)
                            with open(file_directory, 'wb') as out_f:
                                out_f.write(content)

                    except Exception as e:  # noqa: E722
                        log["Not Downloaded"]+=1
                        log["Log not downloaded"].append(f'Error writing {file_name}: {str(e)}.')
                    else:
                        log["Downloaded"]+=1
    
    return log
        
def crawler_resources(url:str) -> dict:
    resource_urls = get_resource_urls(url)
    LOG = download_resources(resource_urls,url)
    return LOG

def crawler_criminal_records(url:str):
    pass