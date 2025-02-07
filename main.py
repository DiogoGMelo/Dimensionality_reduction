import tkinter as tk
from tkinter import PhotoImage
import matplotlib.pyplot as plt
from PIL import Image

def carregar_png(original):
    """Carrega um arquivo PNG e retorna pixels no formato (R, G, B)"""

    root = tk.Tk()  
    root.withdraw()
    img = PhotoImage(file=original)
    largura = img.width()
    altura = img.height()
    
    pixels = []
    for y in range(altura):
        linha_pixels = []
        for x in range(largura):
            r, g, b = img.get(x, y)  # Obtém a cor RGB do pixel
            linha_pixels.append((r, g, b))
        pixels.append(linha_pixels)
    
    root.destroy()
    return pixels, largura, altura

def salvar_ppm(nome_arquivo, pixels, largura, altura):
    """Salva uma imagem no formato PPM P3"""

    with open(nome_arquivo, 'w') as f:
        f.write("P3\n")
        f.write(f"{largura} {altura}\n")
        f.write("255\n")
        for linha in pixels:
            f.write(" ".join(f"{r} {g} {b}" for r, g, b in linha) + "\n")

imagem, largura, altura = carregar_png("original.png")
salvar_ppm("imagem.ppm", imagem, largura, altura)



def carregar_imagem_ppm(nome_arquivo):
    """Carrega uma imagem PPM (P3) e retorna os pixels e dimensões."""

    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    
    assert linhas[0].strip() == 'P3', "Formato de imagem não suportado!"
    
    idx = 1
    while linhas[idx].startswith("#"):
        idx += 1
    
    largura, altura = map(int, linhas[idx].split())
    idx += 1
    max_val = int(linhas[idx])
    idx += 1
    
    # Processar os valores RGB 
    pixels = []
    valores = " ".join(linhas[idx:]).split()  # Une todas as linhas restantes e divide em valores individuais
    pos = 0
    for i in range(altura):
        linha_pixels = []
        for j in range(largura):
            r = int(valores[pos])  # Obtém o próximo valor R
            g = int(valores[pos + 1])  # Obtém o próximo valor G
            b = int(valores[pos + 2])  # Obtém o próximo valor B
            linha_pixels.append((r, g, b))
            pos += 3
        pixels.append(linha_pixels)
    
    return pixels, largura, altura, max_val




def converter_para_cinza(pixels):
    """Converte a imagem colorida para tons de cinza."""

    return [[int(0.2989*r + 0.5870*g + 0.1140*b) for r, g, b in linha] for linha in pixels]



def binarizar_imagem(pixels_cinza, limiar=128):
    """Binariza a imagem com base em um limiar."""

    return [[255 if p >= limiar else 0 for p in linha] for linha in pixels_cinza]



def salvar_imagem_pgm(nome_arquivo, pixels, largura, altura):
    """Salva uma imagem PGM (P2 - Portable Graymap) a partir da matriz de pixels."""

    with open(nome_arquivo, 'w') as f:
        f.write("P2\n")
        f.write(f"{largura} {altura}\n")
        f.write("255\n")
        for linha in pixels:
            f.write(" ".join(map(str, linha)) + "\n")


imagem, largura, altura, max_val = carregar_imagem_ppm("imagem.ppm")
imagem_cinza = converter_para_cinza(imagem)
salvar_imagem_pgm("imagem_cinza.pgm", imagem_cinza, largura, altura)

imagem_bin = binarizar_imagem(imagem_cinza, limiar=128)
salvar_imagem_pgm("imagem_bin.pgm", imagem_bin, largura, altura)


def exibir_imagens():
    """Exibe as 3 imagens (Original, Cinza, Binarizada) no formato desejado"""
   
    img_original = Image.open("original.png")
    img_cinza = Image.open("imagem_cinza.pgm")
    img_bin = Image.open("imagem_bin.pgm")

    # Criar o layout para exibição
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Mostrar a imagem original
    axs[0].imshow(img_original)
    axs[0].set_title("Imagem Original")
    axs[0].axis("off")

    # Mostrar a imagem em tons de cinza
    axs[1].imshow(img_cinza, cmap="gray")
    axs[1].set_title("Imagem em Cinza")
    axs[1].axis("off")

    #
    axs[2].imshow(img_bin, cmap="gray")
    axs[2].set_title("Imagem Binária")
    axs[2].axis("off")

    # Ajustar o layout e exibir
    plt.tight_layout()
    plt.show()

exibir_imagens()

