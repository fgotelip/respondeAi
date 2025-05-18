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


def pega_ultimo_print(pasta):
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]

    # Verifica qual tem a data de modificação mais recente
    caminho_ultimo_print = max(arquivos, key=os.path.getmtime)
    
    return caminho_ultimo_print

def extrair_texto_imagem(caminho):
    try:
        imagem = Image.open(caminho)
        texto = pytesseract.image_to_string(imagem, lang='por')
        string_texto = ("\"\"\"" + texto + "\"\"\"")
        return texto
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None
    
def pesquisa_google(questao):
    links = list(search(questao, num_results=10, lang="pt"))

    filtro = [url for url in links if "respondeai" in url]
    if not filtro:
        print("Nenhum link correspondente encontrado.")
        return None
    else:
        url = filtro[0]

        resposta_pagina = requests.get(url)
        
        if resposta_pagina.status_code == 200:
            html = resposta_pagina.text
            return html

        else:
            print("Erro ao acessar a página:", resposta_pagina.status_code)

def tira_blur(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remover todas as tags <style>
    for tag in soup.find_all('style'):
        tag.decompose()

    with open('resposta.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


def abrir_no_navegador():
    # Caminho absoluto do arquivo HTML gerado
    caminho = os.path.abspath("resposta.html")

    # Abrir no navegador padrão (Chrome, Edge, etc.)
    webbrowser.open(f"file://{caminho}")




# Caminho da pasta onde estão os print
pasta_prints = "C:\\Users\\felip\\Pictures\\Screenshots"

caminho_ultimo_print = pega_ultimo_print(pasta_prints)

questao_do_livro = extrair_texto_imagem(caminho_ultimo_print)

if questao_do_livro != None:
    html = pesquisa_google(questao_do_livro)

    if html != None:
        tira_blur(html)

        abrir_no_navegador()
