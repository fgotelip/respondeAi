from shlex import split
from PIL import Image
import pytesseract
import os
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from pathlib import Path

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
    

def procura_texto_google(questao):
    # Adiciona filtro direto na consulta para priorizar resultados do site respondeai
    query = f"{questao} site:respondeai.com.br"

    try:
        for url in search(query, num_results=3, lang="pt"):
            if "respondeai" in url:
                return url
        url = input("Não encontrei a questão automaticamente. Por favor, cole a URL do site RespondeAí: ")
        return url

    except Exception as e:
        print(f"Erro na busca: {e}")
        return None


def extrair_html(url):
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

    pasta = Path(f"respostas/{capitulo}")
    pasta.mkdir(parents=True, exist_ok=True)

    arquivo = Path(f"respostas/{capitulo}/{capitulo}.{questao}.html")

    arquivo.write_text(soup.prettify(), encoding='utf-8')


def abrir_no_navegador(capitulo, questao):
    # Caminho absoluto do arquivo HTML gerado
    caminho = os.path.abspath(os.path.join(f"respostas/{capitulo}", f'{capitulo}.{questao}.html'))

    # Abrir no navegador padrão (Chrome, Edge, etc.)
    webbrowser.open(f"file://{caminho}")


def varias_questoes(capitulo, questoes,pasta_prints):
    quantidade = len(questoes)
    arquivos = reversed(arquivos_mais_recentes(pasta_prints, quantidade))
    i = 0
    for caminho_ultimo_print in arquivos:
        questao_do_livro = extrair_texto_imagem(caminho_ultimo_print)

        if questao_do_livro != None:

            url = procura_texto_google(questao_do_livro)
            html = extrair_html(url)

            if html != None:
                tira_blur(html, capitulo, questoes[i])

                abrir_no_navegador(capitulo, questoes[i])
            i += 1

def questao_por_link(link, capitulo, questao):
    html = extrair_html(link)
    if html != None:
        tira_blur(html, capitulo, questao)
        abrir_no_navegador(capitulo, questao)

def questao_por_texto(texto, capitulo, questao):
    url = procura_texto_google(texto)
    html = extrair_html(url)
    if html != None:
        tira_blur(html, capitulo, questao)
        abrir_no_navegador(capitulo, questao)

# Caminho da pasta onde estão os print
pasta_prints = "C:\\Users\\felip\\Pictures\\Screenshots"


capitulo = "Preparativo TVC2"
questoes = [1]
link = "https://respondeai.com.br/questoes/11-48/"
texto = """Numa indústria deseja-se projetar um dissipador de calor para elementos
transistores em um local onde o coeficiente de transferência de calor por
convecção é 3 Kcal/h.m2.°C. A base do dissipador será uma placa plana, de 10
cm x 10 cm, sobre a qual estarão dispostas 8 aletas, de seção transversal
retangular, com espaçamento constante, de 2 mm de espessura e 40 mm de
altura. Sob a placa deve ser mantida uma temperatura de 80 °C, com
temperatura ambiente de 30 °C. Considerando a condutividade térmica das
aletas igual a 35 Kcal/h.m.°C, pede-se:
a) (15 pontos) a eficiência da aleta;
b) (15 pontos) calor dissipado pela placa aletada;
DADO : 1 KW = 860 kcal/h"""

# varias_questoes(capitulo, questoes, pasta_prints)
# questao_por_link(link, capitulo, questoes[0])
questao_por_texto(texto, capitulo, questoes[0])
