"""
Sistema de Detecção de Vagas de Estacionamento
Detecta se as vagas estão ocupadas ou livres usando visão computacional
"""

import cv2
import pickle
import numpy as np
import os

# Dimensões padrão de uma vaga (mesmas do marcar_vagas.py)
LARGURA_VAGA = 107
ALTURA_VAGA = 48

# Limiar para considerar vaga livre (quantidade de pixels brancos)
LIMIAR_VAGA_LIVRE = 900

def processar_frame(img):
    """
    Pré-processa o frame para melhor detecção
    Converte para escala de cinza, aplica blur e threshold
    """
    # Converte para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplica blur gaussiano para reduzir ruído
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    
    # Aplica threshold adaptativo
    img_thresh = cv2.adaptiveThreshold(
        img_blur, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 
        25, 
        16
    )
    
    # Aplica medianBlur para reduzir ruídos
    img_median = cv2.medianBlur(img_thresh, 5)
    
    # Dilata a imagem para preencher buracos
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)
    
    return img_dilate

def verificar_vaga(img_processada, x, y):
    """
    Verifica se uma vaga específica está livre ou ocupada
    Retorna True se livre, False se ocupada
    """
    # Extrai a região da vaga
    vaga_roi = img_processada[y:y + ALTURA_VAGA, x:x + LARGURA_VAGA]
    
    # Conta pixels brancos (possível presença de carro)
    count = cv2.countNonZero(vaga_roi)
    
    # Se a quantidade de pixels brancos for menor que o limiar, vaga está livre
    return count < LIMIAR_VAGA_LIVRE

def desenhar_vagas(img, vagas_lista, img_processada):
    """
    Desenha as vagas na imagem e mostra status (livre/ocupada)
    """
    vagas_livres = 0
    
    for i, (x, y) in enumerate(vagas_lista):
        # Verifica se a vaga está livre
        vaga_livre = verificar_vaga(img_processada, x, y)
        
        if vaga_livre:
            cor = (0, 255, 0)  # Verde para livre
            espessura = 2
            vagas_livres += 1
        else:
            cor = (0, 0, 255)  # Vermelho para ocupada
            espessura = 2
        
        # Desenha retângulo
        cv2.rectangle(img, (x, y), (x + LARGURA_VAGA, y + ALTURA_VAGA), cor, espessura)
        
        # Adiciona número da vaga
        cv2.putText(img, str(i+1), (x + 5, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return vagas_livres

def main():
    # Caminho para o vídeo
    caminho_video = "../videos/estacionamento.mp4"
    caminho_dados = "../data/vagas.pkl"
    
    # Verifica se o arquivo de vagas existe
    if not os.path.exists(caminho_dados):
        print(f"ERRO: Arquivo de vagas não encontrado: {caminho_dados}")
        print(f"Execute primeiro o script 'marcar_vagas.py' para definir as posições das vagas")
        return
    
    # Carrega as posições das vagas
    with open(caminho_dados, 'rb') as arquivo:
        vagas = pickle.load(arquivo)
    print(f"[OK] {len(vagas)} vagas carregadas")
    
    # Verifica se o vídeo existe
    if not os.path.exists(caminho_video):
        print(f"ERRO: Vídeo não encontrado: {caminho_video}")
        print(f"Coloque um vídeo chamado 'estacionamento.mp4' na pasta 'videos/'")
        return
    
    # Abre o vídeo
    video = cv2.VideoCapture(caminho_video)
    
    if not video.isOpened():
        print("Erro ao abrir o vídeo!")
        return
    
    print("\n=== SISTEMA INICIADO ===")
    print("Pressione 'q' para sair")
    print("Pressione 'ESPAÇO' para pausar/continuar")
    print("========================\n")
    
    pausado = False
    
    while True:
        if not pausado:
            ret, frame = video.read()
            
            # Se chegou ao fim do vídeo, reinicia
            if not ret:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
        
        # Processa o frame
        frame_processado = processar_frame(frame)
        
        # Desenha as vagas e conta as livres
        vagas_livres = desenhar_vagas(frame, vagas, frame_processado)
        vagas_ocupadas = len(vagas) - vagas_livres
        
        # Adiciona informações na tela
        cv2.rectangle(frame, (10, 10), (250, 90), (0, 0, 0), -1)
        cv2.putText(frame, f"Vagas Livres: {vagas_livres}/{len(vagas)}", 
                   (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Vagas Ocupadas: {vagas_ocupadas}/{len(vagas)}", 
                   (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Mostra o frame
        cv2.imshow("Detecção de Vagas", frame)
        
        # Mostra o frame processado (para debug)
        cv2.imshow("Processado (Debug)", frame_processado)
        
        # Aguarda tecla
        key = cv2.waitKey(30 if not pausado else 1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):
            pausado = not pausado
            print("PAUSADO" if pausado else "REPRODUZINDO")
    
    # Libera recursos
    video.release()
    cv2.destroyAllWindows()
    print("\nSistema encerrado")

if __name__ == "__main__":
    main()
