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
                    continue
        print("Nenhum link válido encontrado.")
        return None
    except Exception as e:
        print(f"Erro na busca: {e}")
        return None

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

# modo manual caso não encontre a questão automaticamente
# url = '''https://www.respondeai.com.br/conteudo/fen-trans-mec-flu-trans-cal-e-trans-massa/livro/exercicios/placa-retangular-bidimensional-submetida-condicoes-contorno-temperatura-especificada-tres-lados-75583'''
# resposta_pagina = requests.get(url, timeout=5)
# html = resposta_pagina.text
# tira_blur(html)
# abrir_no_navegador()