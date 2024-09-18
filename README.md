Funções do projeto “O bom candidato"

crawler.py
def get_resource_urls(url:str, target:str = 'BA') -> list[str]:

	Essa função recebe a url do site do TSE que contém os links de download dos recursos procurados (informações dos candidatos), também recebe um target, que se refere ao estado de busca das informações (ignora-se os criminal records).
	O retorno é uma lista com o caminho para cada resource desejado.
def filename_in_folder(file_name:str) -> str:

	Recebe o nome de um file que foi baixado (alguns files estão dentro de subpastas e por isso o caminho das subpastas aparece no nome, o objetivo dessa função é receber esse caminho completo e retornar apenas o nome do file.
def make_folders(directory:str, election_year: str):

	Esse função cria os diretórios necessários para salvar os arquivos, separando por estado.
def decide_directory(file_name: str, directory: str) -> str:

	Recebe o nome do arquivo e o diretório “raiz” e decide para onde vai cada arquivo com a execução do código.
def download_resources(resource_urls:list[str], url:str) -> dict:

	Recebe a lista do caminho para os resources que foram obtidos por get_resources_url e a url do site do TSE que foi utilizada para encontrar o link dos resources, baixa todos os arquivos nos diretórios corretos e retorna um log informado quais arquivos não foram baixados.
def crawler_resources(url:str) -> dict:

	É a função que junta tudo e que vai para a API.
data_processing.py
def consulta_cand(path_to_consulta_cand:str, path_to_consulta_cand_complt:str) -> list[dict]:

	A maioria dos dados dos candidatos está em arquivos .csv, essa função recebe o caminho para os arquivos buscados, acessa os arquivos e extrai as informações pertinentes, retornando-as em formato de list de dicionários, para serem inseridos no banco de dados.
def bens_candidato(path_to_bens_candidato:str):

	Faz o mesmo que a função acima mas para a planilha de bens de candidato.
def comma_to_dot(number:str) -> float:

	Os números da planilha seguem o padrão brasileiro de usar vírgula para separar o que é decimal. A função recebe o número e converte no modelo americano, o qual python usa e segue o padrão de ponto para separar o decimal.
def match_marital_status(marital_status_code) -> str:

	Recebe o código do estado civil de uma candidato e retorna como nome.








db_operations.py
def insert_basic_info_db(documents:list[dict], state:str) -> str:

	Insere as informações vindas de consulta_cand() no banco de dados.
def insert_bens_info_db(all_candidates_bens_info, state) -> list[str]:

	Insere as informações vindas de bens_candidato() no banco de dados.
def search_candidate(candidato_buscado:str) -> list:

	Recebe um nome ou pedaço de nome de um candidato e retorna todos os candidatos que possuam estes caracteres no nome, usando pattern matching.
def search_unique_number(unique_number:str) -> list:

	Busca um número único de candidato no banco de dados.
def get_picture_from_server(candidates:list) -> list[str]:

	Busca as fotos de uma lista de candidatos no server e retorna o caminho para as fotos dos candidatos buscados.










app.py
@app.get("/search", response_class=HTMLResponse):

	Rota relacionada à barra de busca (na qual digita-se o nome do candidato buscado), retorna informações básicas do candidato em um div com link para a página do candidato, com mais informações.
@app.get('/', response_class=HTMLResponse):

	Root, retorna a página inicial.
@app.get('/candidate_page/{unique_number}', response_class=HTMLResponse):

	Se relaciona com o link no div com as informações básicas do candidato, retorna a página detalhada.
@app.post(“/crawl_candidates_basic_info/"):

	Rota que baixa todas as informações, trata e insere no banco de dados pela primeira vez (supostamente).
@app.post(“/insert_candidates_info_in_db/“):


	Rota que trata as informações já baixadas e insere no banco de dados. (Col
@app.put(“/update_candidates_basic_info”):


	Rota que atualiza as informações já baixadas e insere no banco de dados.


@app.get(“/candidates_info_updated/“):

	Rota que baixa as informações do site do TSE.
