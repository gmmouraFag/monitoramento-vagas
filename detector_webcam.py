"""
Versão simplificada para testar com webcam ou outra fonte de vídeo
"""

import cv2
import pickle
import numpy as np
import os

LARGURA_VAGA = 107
ALTURA_VAGA = 48
LIMIAR_VAGA_LIVRE = 900

def processar_frame(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)
    return img_dilate

def verificar_vaga(img_processada, x, y):
    vaga_roi = img_processada[y:y + ALTURA_VAGA, x:x + LARGURA_VAGA]
    count = cv2.countNonZero(vaga_roi)
    return count < LIMIAR_VAGA_LIVRE

def main():
    caminho_dados = "../data/vagas.pkl"
    
    if not os.path.exists(caminho_dados):
        print("ERRO: Execute 'marcar_vagas.py' primeiro!")
        return
    
    with open(caminho_dados, 'rb') as arquivo:
        vagas = pickle.load(arquivo)
    
    # Use 0 para webcam, ou caminho de arquivo/URL
    video = cv2.VideoCapture(0)  # Altere aqui para usar webcam
    
    print("Sistema iniciado - Pressione 'q' para sair")
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        frame_processado = processar_frame(frame)
        vagas_livres = 0
        
        for i, (x, y) in enumerate(vagas):
            vaga_livre = verificar_vaga(frame_processado, x, y)
            cor = (0, 255, 0) if vaga_livre else (0, 0, 255)
            if vaga_livre:
                vagas_livres += 1
            cv2.rectangle(frame, (x, y), (x + LARGURA_VAGA, y + ALTURA_VAGA), cor, 2)
        
        cv2.putText(frame, f"Livres: {vagas_livres}/{len(vagas)}", 
                   (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Detector Webcam", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
