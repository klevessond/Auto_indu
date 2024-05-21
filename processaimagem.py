import os
import pytesseract
from PIL import Image

# Verifique se o arquivo de imagem existe
image_path = './imagem_tratada_0.png'
if os.path.exists(image_path):
    print("Arquivo encontrado.")
else:
    print("Arquivo não encontrado. Verifique o caminho.")
    exit()  # Saia do script se a imagem não for encontrada

# Carregue a imagem do arquivo
try:
    image = Image.open(image_path)
    print("Imagem carregada com sucesso.")
except IOError:
    print("Erro ao carregar a imagem.")
    exit()

# Configuração do caminho do executável do Tesseract
tesseract_cmd_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_cmd_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
    print("Caminho do Tesseract configurado corretamente.")
else:
    print("Executável do Tesseract não encontrado. Verifique o caminho.")
    exit()

# Use o Tesseract para extrair texto
try:
    text = pytesseract.image_to_string(image)
    print("OCR realizado com sucesso.")
except Exception as e:
    print(f"Erro durante o OCR: {e}")
    exit()

# Imprima o texto extraído
print("Texto extraído:")
print(text)
