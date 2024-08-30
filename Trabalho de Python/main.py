import requests

api_key = "92c1bd82a83a4ac8a2c6af2613378686"
pesquisa = "Tesla"


def obter_noticias():
    """
    Obtém notícias da API do NewsAPI com base na pesquisa fornecida.
    Retorna uma lista de títulos e URLs dos artigos.
    """
    try:
        news_url = f"https://newsapi.org/v2/everything?q={pesquisa}&apiKey={api_key}"
        response = requests.get(news_url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        json_data = response.json()

        # Verifica se há artigos na resposta
        if "articles" not in json_data:
            print("Nenhum artigo encontrado na resposta.")
            return [], []

        articles = json_data["articles"][:5]  # Limitar a 5 artigos

        titles = [article.get("title", "Sem título") for article in articles]
        urls = [article.get("url", "Sem URL") for article in articles]

        return titles, urls
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter notícias: {e}")
        return [], []


def exibir_noticias():
    """
    Exibe os títulos e URLs das notícias obtidas.
    """
    titulos, urls = obter_noticias()

    if not titulos:
        print("Nenhuma notícia encontrada.")
        return

    for i, titulo in enumerate(titulos):
        print(f"{i + 1}. {titulo}")
        print(f"Link: {urls[i]}\n")


if __name__ == "__main__":
    exibir_noticias()
