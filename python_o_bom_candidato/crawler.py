from bs4 import BeautifulSoup
import requests
import os
from zipfile import ZipFile
from io import BytesIO

def get_resource_urls(url:str) -> list[list]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all('a',class_= "heading")
    resources_info = [[f'https://dadosabertos.tse.jus.br/{tag.get('href')}', tag.get("title")] for tag in tags]
    return resources_info

def get_resource_paths(resources_info: list[list]):
    resource_paths = []
    #Not working with pictures
    resources = [resource[0] for resource in resources_info if resource[1].find('Fotos')==-1]
    print(resources)
    for r in resources:
        response = requests.get(r)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('a', class_="resource-url-analytics"):
            resource_paths.append(tag.get('href'))
            print(tag.get('href'))
    return resource_paths

def download_resources(resource_paths:list[str], url:str) -> list[str]:
    log = []
    election_year = url[url.find("candidatos")::]
    directory = f'/Users/matheusneri/Documents/o_bom_candidato_files/{election_year}/'
    os.makedirs(directory, exist_ok=True)
    for resource_path in resource_paths:
        response = requests.get(resource_path)
        zip_file = BytesIO(response.content)

        with ZipFile (zip_file, 'r') as z:
            files_name_list = z.namelist()

            for file_name in files_name_list:

                if file_name != 'leiame.pdf':

                    with z.open(file_name) as f:
                        content = f.read()
                        file_directory = f'{directory}/{file_name}'
                        with open(file_directory, 'wb') as out_f:
                            try:
                                out_f.write(content)
                            except:  # noqa: E722
                                log.append(f'Resource {file_name} not downloaded.')
                            else:
                                log.append(f'Resource {file_name} downloaded.')
    return log
        
def crawler(url:str) -> str:
    resource_urls = get_resource_urls(url)
    resource_paths = get_resource_paths(resource_urls)
    LOG = download_resources(resource_paths,url)
    return f'{LOG}'

#
url = "https://dadosabertos.tse.jus.br/dataset/candidatos-2022"
crawler(url)

