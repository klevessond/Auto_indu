import logging
from pyzbar.pyzbar import decode
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def select_image():
    """Abre um diálogo para o usuário escolher uma imagem de QR Code."""
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    file_path = filedialog.askopenfilename()
    root.destroy()  # Destroi a janela do Tkinter após a seleção
    return file_path

def extract_table_data(driver):
    """Extrai e imprime dados da tabela de itens da página."""
    rows = driver.find_elements(By.CSS_SELECTOR, "#tbItensList tr")
    for row in rows[1:]:  # Pular cabeçalho da tabela
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 1:  # Verifica se há colunas suficientes
            descricao = columns[2].text
            quantidade = columns[1].text
            unidade = columns[4].text
            valor_unitario = columns[5].text
            valor_total = columns[7].text
            print(f"Descrição: {descricao}, Quantidade: {quantidade}, Unidade: {unidade}, Valor Unitário: {valor_unitario}, Valor Total: {valor_total}")

# Selecionar a imagem através da interface gráfica
file_path = select_image()
if file_path:
    try:
        imagem = Image.open(file_path)
        qrcodes = decode(imagem)
        logging.info("QR Code(s) decodificado(s) com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao carregar ou decodificar imagem: {e}")
        exit()

    # Configuração do WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    for qrcode in qrcodes:
        url = qrcode.data.decode("utf-8")
        print(f"Conteúdo do QR Code: {url}")  # Exibe o conteúdo do QR Code
        logging.info(f"Acessando URL: {url}")

        try:
            driver.get(url)
            logging.info("Página carregada com sucesso.")
            # Solicitar ao usuário para inserir o captcha
            input("Por favor, insira o captcha na página e pressione Enter aqui após concluir...")
            
            # Exemplo de extração de informações da página
            razao_social = driver.find_element(By.ID, "lblRazaoSocialEmitente").text
            nome_fantasia = driver.find_element(By.ID, "lblNomeFantasia").text
            cnpj = driver.find_element(By.ID, "lblCPFCNPJEmitente").text

            print(f"Razão Social: {razao_social}")
            print(f"Nome Fantasia: {nome_fantasia}")
            print(f"CNPJ: {cnpj}")

            # Extrair dados da tabela de itens
            extract_table_data(driver)

        except Exception as e:
            logging.error(f"Erro ao acessar a URL ou ao processar a página: {e}")
        finally:
            driver.quit()
else:
    logging.info("Nenhuma imagem selecionada.")
