from shlex import split
from PIL import Image
import pytesseract
import os
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import webbrowser
import os

# caminho do executável do tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def arquivos_mais_recentes(pasta, quantidade):
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
    arquivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return arquivos[:quantidade]


def extrair_texto_imagem(caminho):
    try:
        imagem = Image.open(caminho)
        texto = pytesseract.image_to_string(imagem, lang='por')
        string_texto = ("\"\"\"" + texto + "\"\"\"")
        with open('questao.txt', 'w', encoding='utf-8') as f:
            f.write(string_texto)
        return texto
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None
    

def pesquisa_google(questao):
    # Adiciona filtro direto na consulta para priorizar resultados do site respondeai
    query = f"{questao} site:respondeai.com.br"

    try:
        for url in search(query, num_results=3, lang="pt"):
            if "respondeai" in url:
                try:
                    resposta_pagina = requests.get(url, timeout=5)
                    if resposta_pagina.status_code == 200:
                        return resposta_pagina.text
                except requests.exceptions.RequestException:
                    print("Erro ao acessar a URL fornecida. Verifique se está correta.")
                    return None
        url = input("Não encontrei a questão automaticamente. Por favor, cole a URL do site RespondeAí: ")
        if "respondeai" in url:
            try:
                resposta_pagina = requests.get(url, timeout=5)
                if resposta_pagina.status_code == 200:
                    return resposta_pagina.text
            except requests.exceptions.RequestException:
                print("Erro ao acessar a URL fornecida. Verifique se está correta.")
                return None
        else:
            print("A URL fornecida não é do site RespondeAí.")
            return None
    except Exception as e:
        print(f"Erro na busca: {e}")
        return None


def tira_blur(html,capitulo,questao):
    soup = BeautifulSoup(html, 'html.parser')
    # Remover todas as tags <style>
    for tag in soup.find_all('style'):
        tag.decompose()

    # Título da página
    soup.title.string = (f"{capitulo}.{questao}")

    # Título da questão
    h1_tag = soup.new_tag('h1')
    h1_tag.string = (f"{capitulo}.{questao}")
    soup.body.insert(0, h1_tag)


    with open('resposta.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


def abrir_no_navegador():
    # Caminho absoluto do arquivo HTML gerado
    caminho = os.path.abspath("resposta.html")

    # Abrir no navegador padrão (Chrome, Edge, etc.)
    webbrowser.open(f"file://{caminho}")




# Caminho da pasta onde estão os print
pasta_prints = "C:\\Users\\felip\\Pictures\\Screenshots"

# quantidade = int(input("Quantas questões você quer pesquisar? "))
# capitulo = int(input("Qual o capítulo? "))
# questoes = split(input("Digite as questões separadas por vírgula (ex: 1,2,3): "))
# questoes = [int(q.strip()) for q in questoes if q.strip().isdigit()]

quantidade = 12
arquivos = reversed(arquivos_mais_recentes(pasta_prints, quantidade))

capitulo = 6
questoes = [4, 5, 6, 7, 8, 9, 10, 11, 13, 1, 2, 3]
i = 0
for caminho_ultimo_print in arquivos:
    questao_do_livro = extrair_texto_imagem(caminho_ultimo_print)

    if questao_do_livro != None:
        html = pesquisa_google(questao_do_livro)

        if html != None:
            tira_blur(html, capitulo, questoes[i])

            abrir_no_navegador()
        i += 1

