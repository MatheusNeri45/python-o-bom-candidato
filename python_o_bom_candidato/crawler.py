from bs4 import BeautifulSoup
import requests
import os
from zipfile import ZipFile
from io import BytesIO
from STATES import STATES as states
def get_resource_urls(url:str) -> list[list]:
    print("The code is getting the resource urls")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all('a',class_= "heading")
    resources_info = [[f'https://dadosabertos.tse.jus.br/{tag.get('href')}', tag.get("title")] for tag in tags]
    return resources_info

def get_resource_paths(resources_info: list[list]):
    resource_paths = []
    #Not working with pictures
    resources = [resource[0] for resource in resources_info if resource[1].find('Fotos')==-1]
    print("The code is getting the resource paths")
    for r in resources:
        response = requests.get(r)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('a', class_="resource-url-analytics"):
            resource_paths.append(tag.get('href'))
    return resource_paths


def filename_in_folder(file_name:str) -> str:
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
    os.makedirs(directory, exist_ok=True)
    for key in states.keys():
        folder = f'/Users/matheusneri/Documents/o_bom_candidato_files/{election_year}/{key}/'
        os.makedirs(folder, exist_ok=True)

def decide_directory(file_name: str, directory: str) -> str:
    for key in states.keys():
        if key in file_name:
            file_directory = f'{directory}/{key}/{file_name}'
            return file_directory
    
    return f'{directory}/{file_name}'


def download_resources(resource_paths:list[str], url:str) -> list[str]:
    log = []
    election_year = url[url.find("candidatos")::]
    directory = f'/Users/matheusneri/Documents/o_bom_candidato_files/{election_year}/'
    make_folders(url, election_year)
    for resource_path in resource_paths:
        response = requests.get(resource_path)
        zip_file = BytesIO(response.content)
        print("The code is requesting the zip file")
        with ZipFile (zip_file, 'r') as z:
            files_name_list = z.namelist()
            print("The code got the files name list inside the specific zip file")
            for fname in files_name_list:
                file_name = filename_in_folder(fname)
                if file_name != 'leiame.pdf':
                    try:
                        print(f"The code just started savin the files: {file_name}")
                        with z.open(fname) as f:
                            content = f.read()
                            file_directory = decide_directory(file_name=file_name, directory=directory)
                            with open(file_directory, 'wb') as out_f:
                                out_f.write(content)

                    except Exception as e:  # noqa: E722
                         log.append(f'Error writing {file_name}: {str(e)}.')
                    else:
                         log.append(f'Resource {file_name} downloaded.')
    
    return log
        
def crawler(url:str) -> str:
    resource_urls = get_resource_urls(url)
    resource_paths = get_resource_paths(resource_urls)
    LOG = download_resources(resource_paths,url)
    return f'{LOG}'


url = "https://dadosabertos.tse.jus.br/dataset/candidatos-2022"
log = crawler(url)
print(log)

