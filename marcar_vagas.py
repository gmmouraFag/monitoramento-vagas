"""
Script para marcar manualmente as posições das vagas de estacionamento
Clique com o botão esquerdo para adicionar uma vaga
Clique com o botão direito para remover a última vaga
Pressione 'q' para salvar e sair
"""

import cv2
import pickle
import os

# Lista para armazenar as posições das vagas
vagas = []

# Dimensões padrão de uma vaga (largura, altura)
LARGURA_VAGA = 107
ALTURA_VAGA = 48

def mouse_callback(event, x, y, flags, param):
    """
    Callback para eventos do mouse
    """
    global vagas
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Adiciona uma nova vaga
        vagas.append((x, y))
        print(f"Vaga adicionada: ({x}, {y}) | Total: {len(vagas)}")
    
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Remove a última vaga
        if vagas:
            vaga_removida = vagas.pop()
            print(f"Vaga removida: {vaga_removida} | Total: {len(vagas)}")

def desenhar_vagas(img, vagas_lista):
    """
    Desenha retângulos nas posições das vagas
    """
    for i, (x, y) in enumerate(vagas_lista):
        cv2.rectangle(img, (x, y), (x + LARGURA_VAGA, y + ALTURA_VAGA), (255, 0, 255), 2)
        cv2.putText(img, str(i+1), (x + 5, y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def main():
    global vagas
    
    # Caminho para o vídeo ou imagem
    caminho_video = "../videos/estacionamento.mp4"
    caminho_imagem = "../images/estacionamento.jpg"
    caminho_dados = "../data/vagas.pkl"
    
    # Verifica se existe arquivo de configuração salvo
    if os.path.exists(caminho_dados):
        with open(caminho_dados, 'rb') as arquivo:
            vagas = pickle.load(arquivo)
            print(f"Carregadas {len(vagas)} vagas salvas anteriormente")
    
    # Tenta abrir imagem primeiro, se não existir, usa o primeiro frame do vídeo
    if os.path.exists(caminho_imagem):
        img = cv2.imread(caminho_imagem)
        print(f"Usando imagem: {caminho_imagem}")
    elif os.path.exists(caminho_video):
        video = cv2.VideoCapture(caminho_video)
        ret, img = video.read()
        video.release()
        if not ret:
            print("Erro ao ler o vídeo!")
            return
        print(f"Usando primeiro frame do vídeo: {caminho_video}")
    else:
        print(f"ERRO: Coloque um vídeo em '{caminho_video}' ou uma imagem em '{caminho_imagem}'")
        print(f"Diretório atual: {os.getcwd()}")
        return
    
    # Cria janela e configura callback do mouse
    cv2.namedWindow("Marcar Vagas")
    cv2.setMouseCallback("Marcar Vagas", mouse_callback)
    
    print("\n=== INSTRUÇÕES ===")
    print("- Clique com BOTÃO ESQUERDO para adicionar uma vaga")
    print("- Clique com BOTÃO DIREITO para remover a última vaga")
    print("- Pressione 'q' para SALVAR e sair")
    print("- Pressione 'ESC' para sair SEM salvar")
    print("==================\n")
    
    while True:
        # Cria uma cópia da imagem para não modificar o original
        img_display = img.copy()
        
        # Desenha todas as vagas
        desenhar_vagas(img_display, vagas)
        
        # Mostra a imagem
        cv2.imshow("Marcar Vagas", img_display)
        
        # Aguarda tecla
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            # Salva as vagas
            with open(caminho_dados, 'wb') as arquivo:
                pickle.dump(vagas, arquivo)
            print(f"\n[OK] {len(vagas)} vagas salvas em '{caminho_dados}'")
            break
        elif key == 27:  # ESC
            print("\nSaindo sem salvar...")
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
