import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_property_details(property_url):
    """
    Extrai detalhes de um único imóvel.
    """
    try:
        response = requests.get(property_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        details = {}

        # Título e Bairro
        title_tag = soup.find('h1', class_='titulo-pagina')
        if title_tag:
            title_text = title_tag.text.strip()
            details['titulo'] = title_text
            # Extrair bairro do título
            parts = title_text.split()
            if len(parts) > 1:
                details['bairro'] = parts[-1]
            else:
                details['bairro'] = None
        else:
            details['titulo'] = None
            details['bairro'] = None

        # Preço
        price_tag = soup.find('div', class_='preco')
        details['preco'] = price_tag.text.strip() if price_tag else None

        # Descrição
        description_tag = soup.find('div', class_='texto-descricao')
        details['descricao'] = description_tag.text.strip() if description_tag else None

        # Características
        caracteristicas = {}
        items = soup.select('ul.caracteristicas li')
        for item in items:
            text = item.text.strip()
            parts = text.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                caracteristicas[key] = value
        details['caracteristicas'] = caracteristicas

        return details
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {property_url}: {e}")
        return None

def scrape_site():
    """
    Raspa o site imoveisjoaopessoa.com.br para extrair dados de imóveis.
    """
    base_url = "https://www.imoveisjoaopessoa.com.br"
    all_properties = []

    # Itera através das páginas de bairros (exemplo)
    # Uma implementação mais robusta seguiria todos os links de paginação
    page = 1
    while True:
        # Itera sobre as páginas de bairros, uma abordagem mais confiável
        bairros = ['altiplano', 'bessa', 'cabo-branco', 'manaira', 'tambau'] # Exemplo
        for bairro in bairros:
            page = 1
            while True:
                search_url = f"{base_url}/pt/bairro/{bairro}/venda/pagina/{page}"
                try:
                    response = requests.get(search_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')

                    property_cards = soup.select('div.card-imovel a')
                    if not property_cards:
                        break

                    for link_tag in property_cards:
                        property_url = link_tag['href']
                        if not property_url.startswith('http'):
                            property_url = base_url + property_url

                        details = get_property_details(property_url)
                        if details:
                            all_properties.append(details)

                    print(f"Página {page} do bairro {bairro} processada.")
                    page += 1
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao acessar {search_url}: {e}")
                    break

    return all_properties

if __name__ == "__main__":
    properties = scrape_site()

    # Salvar em JSON
    with open('imoveis.json', 'w', encoding='utf-8') as f:
        json.dump(properties, f, ensure_ascii=False, indent=4)

    # Salvar em CSV
    df = pd.DataFrame(properties)
    df.to_csv('imoveis.csv', index=False)

    print(f"{len(properties)} imóveis extraídos e salvos em imoveis.json e imoveis.csv")
