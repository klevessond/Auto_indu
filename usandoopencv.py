import cv2

# Lista de métodos de limiarização
metodos = [
    cv2.THRESH_BINARY,
    cv2.THRESH_BINARY_INV,
    cv2.THRESH_TRUNC,
    cv2.THRESH_TOZERO,
    cv2.THRESH_TOZERO_INV,
]

# Carregar a imagem do disco
imagem = cv2.imread("./captcha_image.png")

# Checar se a imagem foi carregada corretamente
if imagem is None:
    print("Erro ao abrir a imagem. Verifique se o caminho está correto.")
else:
    # Transformar a imagem em escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Inicializar um contador
    i = 0

    # Pasta para salvar as imagens tratadas
    output_folder = "./"

    # Aplicar cada método de limiarização e salvar as imagens resultantes
    for metodo in metodos:
        _, imagem_tratada = cv2.threshold(imagem_cinza, 127, 255, metodo or cv2.THRESH_OTSU)
        cv2.imwrite(f"{output_folder}imagem_tratada_{i}.png", imagem_tratada)
        i += 1
