"""
Utilitários para o sistema de detecção de vagas
"""

import cv2
import pickle
import os

def extrair_frame_video(caminho_video, numero_frame=0, caminho_saida="../images/estacionamento.jpg"):
    """
    Extrai um frame específico do vídeo e salva como imagem
    """
    video = cv2.VideoCapture(caminho_video)
    
    if not video.isOpened():
        print("Erro ao abrir o vídeo!")
        return False
    
    # Pula para o frame desejado
    video.set(cv2.CAP_PROP_POS_FRAMES, numero_frame)
    ret, frame = video.read()
    
    if ret:
        cv2.imwrite(caminho_saida, frame)
        print(f"[OK] Frame {numero_frame} salvo em: {caminho_saida}")
        return True
    else:
        print("Erro ao ler o frame!")
        return False
    
    video.release()

def info_video(caminho_video):
    """
    Mostra informações sobre o vídeo
    """
    video = cv2.VideoCapture(caminho_video)
    
    if not video.isOpened():
        print("Erro ao abrir o vídeo!")
        return
    
    # Obtém propriedades do vídeo
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duracao = frame_count / fps if fps > 0 else 0
    
    print("\n=== INFORMAÇÕES DO VÍDEO ===")
    print(f"Arquivo: {caminho_video}")
    print(f"Resolução: {width}x{height}")
    print(f"FPS: {fps:.2f}")
    print(f"Total de frames: {frame_count}")
    print(f"Duração: {duracao:.2f} segundos")
    print("============================\n")
    
    video.release()

def visualizar_vagas_salvas(caminho_dados="../data/vagas.pkl"):
    """
    Mostra informações sobre as vagas salvas
    """
    if not os.path.exists(caminho_dados):
        print(f"Arquivo não encontrado: {caminho_dados}")
        return
    
    with open(caminho_dados, 'rb') as arquivo:
        vagas = pickle.load(arquivo)
    
    print(f"\n=== VAGAS SALVAS ===")
    print(f"Total: {len(vagas)} vagas")
    print("\nPosições:")
    for i, (x, y) in enumerate(vagas, 1):
        print(f"  Vaga {i:2d}: ({x:4d}, {y:4d})")
    print("====================\n")

def limpar_dados():
    """
    Remove o arquivo de vagas salvas
    """
    caminho = "../data/vagas.pkl"
    if os.path.exists(caminho):
        os.remove(caminho)
        print(f"[OK] Arquivo removido: {caminho}")
    else:
        print(f"Arquivo não existe: {caminho}")

def menu():
    """
    Menu interativo de utilitários
    """
    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║   UTILITÁRIOS - DETECTOR DE VAGAS     ║")
        print("╠════════════════════════════════════════╣")
        print("║ 1. Extrair frame de vídeo              ║")
        print("║ 2. Informações do vídeo                ║")
        print("║ 3. Visualizar vagas salvas             ║")
        print("║ 4. Limpar dados de vagas               ║")
        print("║ 5. Sair                                ║")
        print("╚════════════════════════════════════════╝")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            video = input("Caminho do vídeo [../videos/estacionamento.mp4]: ").strip()
            if not video:
                video = "../videos/estacionamento.mp4"
            frame = input("Número do frame [0]: ").strip()
            frame = int(frame) if frame else 0
            extrair_frame_video(video, frame)
            
        elif opcao == "2":
            video = input("Caminho do vídeo [../videos/estacionamento.mp4]: ").strip()
            if not video:
                video = "../videos/estacionamento.mp4"
            info_video(video)
            
        elif opcao == "3":
            visualizar_vagas_salvas()
            
        elif opcao == "4":
            confirma = input("Tem certeza? (s/n): ").strip().lower()
            if confirma == 's':
                limpar_dados()
            else:
                print("Operação cancelada")
                
        elif opcao == "5":
            print("\nAté logo!")
            break
        else:
            print("\n[ERRO] Opção inválida!")

if __name__ == "__main__":
    menu()
