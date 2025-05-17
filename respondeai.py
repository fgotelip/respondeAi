from PIL import Image
import pytesseract
import os
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import webbrowser
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        texto = pytesseract.image_to_string(imagem, lang='por')  # 'por' para português
        return texto
    except Exception as e:
        return f"Erro ao processar imagem: {e}"

# Caminho da pasta onde estão os arquivos
pasta = "C:\\Users\\felip\\Pictures\\Screenshots"
# Pega todos os arquivos da pasta (com caminho completo)
arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]

# Verifica qual tem a data de modificação mais recente
caminho = max(arquivos, key=os.path.getmtime)

texto_extraido = ("\"\"\"" + extrair_texto(caminho) + "\"\"\"")

links = list(search(texto_extraido, num_results=10, lang="pt"))

# Etapa 3: Filtrar o link que você quer (exemplo: o primeiro link que contém 'openai')
filtro = [url for url in links if "respondeai" in url]
if not filtro:
    print("Nenhum link correspondente encontrado.")
else:
    url = filtro[0]

    # Etapa 4: Baixar o código-fonte HTML
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        html = resposta.text

    else:
        print("Erro ao acessar a página:", resposta.status_code)

soup = BeautifulSoup(html, 'html.parser')  # ou 'lxml' se tiver instalado

# Remover todas as tags <style>
for tag in soup.find_all('style'):
    tag.decompose()

with open('resposta.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

# Caminho absoluto do arquivo HTML gerado
caminho = os.path.abspath("resposta.html")

# Abrir no navegador padrão (Chrome, Edge, etc.)
webbrowser.open(f"file://{caminho}")
