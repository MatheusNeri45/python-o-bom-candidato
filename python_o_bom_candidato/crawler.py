from bs4 import BeautifulSoup
import requests
import os
from zipfile import ZipFile
from io import BytesIO

def get_resource_urls(url:str) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all('a',class_= "heading")
    resource_urls = [f'https://dadosabertos.tse.jus.br/{tag.get('href')}' for tag in tags] 
    return resource_urls

def download_resources(url:str) -> list[str]:
    log = []
    sub_directory = url[url.find('dataset')+8::]
    directory = f'/Users/matheusneri/Documents/o_bom_candidato_files/{sub_directory}'
    os.makedirs(directory, exist_ok=True)
    response = requests.get(url)
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
        


# url = "https://dadosabertos.tse.jus.br/dataset/candidatos-2022"
# get_resource_urls(url)
resource_path = 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/rede_social_candidato_2022_AP.zip'
log = download_resources(resource_path)
print(log)