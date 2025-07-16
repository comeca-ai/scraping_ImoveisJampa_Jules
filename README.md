# Projeto de Scraping e Dashboard de Imóveis em João Pessoa

Este projeto realiza o scraping de dados de imóveis do site `imoveisjoaopessoa.com.br`, salva os dados em formatos JSON e CSV, e apresenta um dashboard interativo com visualizações dos dados coletados.

## Estrutura do Projeto

- `scraper.py`: Script Python responsável por fazer o scraping dos dados do site.
- `imoveis.json`: Arquivo com os dados dos imóveis em formato JSON.
- `imoveis.csv`: Arquivo com os dados dos imóveis em formato CSV.
- `dashboard.html`: Página HTML que exibe os dashboards com os dados dos imóveis.
- `README.md`: Este arquivo, com a documentação do projeto.

## Como Executar

1. **Instale as dependências:**

   ```bash
   pip install requests beautifulsoup4 pandas
   ```

2. **Execute o script de scraping:**

   ```bash
   python scraper.py
   ```

   Este comando irá extrair os dados e criar os arquivos `imoveis.json` e `imoveis.csv`.

3. **Visualize o dashboard:**

   Abra o arquivo `dashboard.html` em seu navegador de preferência. É recomendado o uso de um servidor web local para evitar problemas com a política de mesma origem (CORS) ao carregar o arquivo JSON. Você pode usar o módulo `http.server` do Python para isso:

   ```bash
   python -m http.server
   ```

   E então acesse `http://localhost:8000/dashboard.html` no seu navegador.
