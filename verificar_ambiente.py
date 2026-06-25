"""
Script de verificação do ambiente
Verifica se todas as dependências estão instaladas corretamente
"""

import sys
import os

def verificar_python():
    """Verifica versão do Python"""
    print("[VERIFICANDO] Python...")
    version = sys.version_info
    print(f"   Versão: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("   [OK] Versão do Python OK")
        return True
    else:
        print("   [ERRO] Python 3.7+ necessário")
        return False

def verificar_opencv():
    """Verifica OpenCV"""
    print("\n[VERIFICANDO] OpenCV...")
    try:
        import cv2
        print(f"   Versão: {cv2.__version__}")
        print("   [OK] OpenCV instalado")
        return True
    except ImportError:
        print("   [ERRO] OpenCV não encontrado")
        print("   Execute: pip install opencv-python")
        return False

def verificar_numpy():
    """Verifica NumPy"""
    print("\n[VERIFICANDO] NumPy...")
    try:
        import numpy as np
        print(f"   Versão: {np.__version__}")
        print("   [OK] NumPy instalado")
        return True
    except ImportError:
        print("   [ERRO] NumPy não encontrado")
        print("   Execute: pip install numpy")
        return False

def verificar_estrutura():
    """Verifica estrutura de pastas"""
    print("\n[VERIFICANDO] estrutura de pastas...")
    
    pastas = ['videos', 'images', 'data', 'src']
    todas_ok = True
    
    for pasta in pastas:
        caminho = os.path.join('..', pasta)
        if os.path.exists(caminho):
            print(f"   [OK] {pasta}/")
        else:
            print(f"   [ERRO] {pasta}/ não encontrada")
            todas_ok = False
    
    return todas_ok

def verificar_arquivos():
    """Verifica arquivos importantes"""
    print("\n[VERIFICANDO] arquivos principais...")
    
    arquivos = {
        '../src/marcar_vagas.py': 'Script de marcação',
        '../src/detector_vagas.py': 'Detector principal',
        '../requirements.txt': 'Dependências'
    }
    
    todos_ok = True
    
    for arquivo, descricao in arquivos.items():
        if os.path.exists(arquivo):
            print(f"   [OK] {descricao}")
        else:
            print(f"   [ERRO] {descricao} não encontrado")
            todos_ok = False
    
    return todos_ok

def testar_opencv_basico():
    """Testa funcionalidades básicas do OpenCV"""
    print("\n[VERIFICANDO] funcionalidades do OpenCV...")
    
    try:
        import cv2
        import numpy as np
        
        # Cria uma imagem de teste
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Testa algumas operações
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        
        print("   [OK] Conversão de cores: OK")
        print("   [OK] Blur gaussiano: OK")
        print("   [OK] Funcionalidades básicas: OK")
        return True
        
    except Exception as e:
        print(f"   [ERRO] Erro ao testar: {e}")
        return False

def verificar_dados():
    """Verifica se há dados configurados"""
    print("\n[VERIFICANDO] configuração...")
    
    caminho_vagas = '../data/vagas.pkl'
    caminho_video = '../videos/estacionamento.mp4'
    caminho_imagem = '../images/estacionamento.jpg'
    
    if os.path.exists(caminho_vagas):
        import pickle
        with open(caminho_vagas, 'rb') as f:
            vagas = pickle.load(f)
        print(f"   [OK] Vagas configuradas: {len(vagas)} vagas")
    else:
        print(f"   [AVISO] Vagas não configuradas ainda")
        print(f"      Execute 'marcar_vagas.py' para configurar")
    
    if os.path.exists(caminho_video):
        print(f"   [OK] Vídeo encontrado")
    elif os.path.exists(caminho_imagem):
        print(f"   [OK] Imagem encontrada")
    else:
        print(f"   [AVISO] Vídeo/imagem não encontrados")
        print(f"      Adicione 'estacionamento.mp4' em videos/")

def main():
    """Função principal"""
    print("╔════════════════════════════════════════════════╗")
    print("║  VERIFICAÇÃO DO AMBIENTE - DETECTOR DE VAGAS  ║")
    print("╚════════════════════════════════════════════════╝\n")
    
    resultados = []
    
    # Executa todas as verificações
    resultados.append(("Python", verificar_python()))
    resultados.append(("OpenCV", verificar_opencv()))
    resultados.append(("NumPy", verificar_numpy()))
    resultados.append(("Estrutura", verificar_estrutura()))
    resultados.append(("Arquivos", verificar_arquivos()))
    
    # Testa funcionalidades se tudo estiver OK
    if all(r[1] for r in resultados[:3]):  # Python, OpenCV, NumPy
        resultados.append(("Funcionalidades", testar_opencv_basico()))
    
    # Verifica configuração
    verificar_dados()
    
    # Resumo
    print("\n" + "="*50)
    print("RESUMO")
    print("="*50)
    
    for nome, status in resultados:
        status_str = "[OK]" if status else "[ERRO]"
        print(f"{nome:20s} {status_str}")
    
    print("="*50)
    
    # Resultado final
    if all(r[1] for r in resultados):
        print("\n[OK] TUDO PRONTO! Sistema configurado corretamente!")
        print("\n[OK] Próximos passos:")
        print("   1. Adicione um vídeo em 'videos/estacionamento.mp4'")
        print("   2. Execute 'python marcar_vagas.py' para marcar as vagas")
        print("   3. Execute 'python detector_vagas.py' para iniciar a detecção")
    else:
        print("\n[AVISO] ATENÇÃO: Alguns componentes precisam ser corrigidos")
        print("\nPara instalar as dependências, execute:")
        print("   pip install -r ../requirements.txt")

if __name__ == "__main__":
    main()
